from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.utils import timezone
from .forms import PendaftaranAK1Form
from .models import PendaftaranAK1
from PIL import Image
import pytesseract
import re
import base64
import io
import google.generativeai as genai
import cv2
import numpy as np
import requests
import json
import time
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

# Define Tesseract Page Segmentation Modes (PSM) for retry logic
TESSERACT_CONFIGS = [
    '--psm 6',
    '--psm 3',
    '--psm 11',
]

# Gemini Structured Output Schema
KTP_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "NIK": {"type": "STRING", "description": "The 16-digit National Identity Number. Must be exactly 16 digits."},
        "Nama": {"type": "STRING", "description": "Full name of the cardholder."},
        "Tempat/Tgl_Lahir": {"type": "STRING", "description": "Place and date of birth in 'Kota, DD-MM-YYYY' format."},
        "Jenis_Kelamin": {"type": "STRING", "description": "Gender: LAKI-LAKI or PEREMPUAN."},
        "Agama": {"type": "STRING", "description": "Religion."},
        "Status_Perkawinan": {"type": "STRING", "description": "Marital status: KAWIN, BELUM KAWIN, etc."},
        "Pekerjaan": {"type": "STRING", "description": "Occupation."},
        "Kewarganegaraan": {"type": "STRING", "description": "Nationality, typically WNI."},
        "Alamat": {"type": "STRING", "description": "Street address."},
        "RT/RW": {"type": "STRING", "description": "RT/RW number combination."},
        "Kelurahan/Desa": {"type": "STRING", "description": "Kelurahan or Desa."},
        "Kecamatan": {"type": "STRING", "description": "Kecamatan (Sub-district)."},
    },
    "required": ["NIK", "Nama"]
}

@login_required
def pendaftaran_ak1(request):
    # Check if user already has a registration
    existing = PendaftaranAK1.objects.filter(user=request.user).first()
    if existing:
        messages.info(request, "Anda sudah mendaftar AK1.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = PendaftaranAK1Form(request.POST, request.FILES)
        if form.is_valid():
            pendaftaran = form.save(commit=False)
            pendaftaran.user = request.user

            # Handle file uploads
            if 'ktp' in request.FILES:
                pendaftaran.ktp_data = base64.b64encode(request.FILES['ktp'].read()).decode('utf-8')
            if 'photo' in request.FILES:
                pendaftaran.photo_data = base64.b64encode(request.FILES['photo'].read()).decode('utf-8')
            if 'ijazah' in request.FILES:
                pendaftaran.ijazah_data = base64.b64encode(request.FILES['ijazah'].read()).decode('utf-8')

            pendaftaran.save()
            messages.success(request, "Pendaftaran AK1 berhasil dikirim!")
            return redirect('status_pendaftaran')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = PendaftaranAK1Form()

    return render(request, 'pendaftaran/pendaftaran_ak1.html', {'form': form})

@login_required
def status_pendaftaran(request):
    try:
        pendaftaran = PendaftaranAK1.objects.get(user=request.user)
        status = pendaftaran.status
    except PendaftaranAK1.DoesNotExist:
        pendaftaran = None
        status = None

    context = {
        'pendaftaran': pendaftaran,
        'status': status,
    }
    return render(request, 'pendaftaran/status_pendaftaran.html', context)

@login_required
def kartu_ak1(request):
    try:
        pendaftaran = PendaftaranAK1.objects.get(user=request.user, status='diverifikasi')
    except PendaftaranAK1.DoesNotExist:
        messages.error(request, "Pendaftaran belum diverifikasi atau tidak ditemukan.")
        return redirect('status_pendaftaran')

    context = {
        'pendaftaran': pendaftaran,
    }
    return render(request, 'pendaftaran/kartu_ak1.html', context)

def call_gemini_parser(ocr_text):
    """
    Sends raw OCR text to the Gemini API for structured JSON extraction.
    Uses exponential backoff for robustness against transient errors.
    """
    system_prompt = (
        "You are an Indonesian KTP (Kartu Tanda Penduduk) Data Extractor. "
        "Your task is to parse the raw, messy OCR text provided below, identify the required KTP fields, "
        "and return the data in a clean, strictly defined JSON format. "
        "Correct common OCR errors (like 'I' for '1' or missing colons) during parsing. "
        "If a field cannot be reliably found, return an empty string for that field."
    )

    payload = {
        "contents": [{"parts": [{"text": ocr_text}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": KTP_RESPONSE_SCHEMA
        }
    }

    # Implement basic exponential backoff
    MAX_RETRIES = 3
    base_delay = 1

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                settings.GEMINI_API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload)
            )
            response.raise_for_status()

            result = response.json()

            # Extract and parse the JSON string from the response
            json_string = result['candidates'][0]['content']['parts'][0]['text']
            parsed_data = json.loads(json_string)

            # Convert keys to match the desired output format for display
            final_data = {}
            for k, v in parsed_data.items():
                final_data[k.replace('_', ' ')] = v

            return final_data

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                return None
        except (KeyError, json.JSONDecodeError):
            return None

    return None


def preprocess_image(image_data):
    """
    Reads, decodes, and preprocesses the image data for better OCR accuracy.
    Preprocessing steps: Grayscale, Thresholding (Otsu's method).
    """
    # Convert uploaded bytes to a numpy array, then to an OpenCV image
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding (best for variable lighting)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert OpenCV image (numpy array) back to PIL Image format for pytesseract
    return Image.fromarray(thresh)


def extract_ktp_fields(raw_text):
    """
    (Legacy RegEx Extractor - kept as a reliable fallback/preliminary NIK check)
    Uses regular expressions and string manipulation to extract key KTP fields
    from the raw OCR text.
    """
    # Clean up common OCR errors specific to KTPs
    cleaned_text = raw_text.replace(":", ": ").replace(":", ":").replace("|", "I").replace("'", "'").replace("—", "-").replace("O", "0")
    cleaned_text = re.sub(r'(\w+)\s*:\s*(\w+)', r'\1: \2', cleaned_text)

    # Initialize dictionary with empty NIK
    temp_data = {'NIK': ''}

    # NIK pattern check
    nik_pattern = re.compile(r'(?:NIK\s*[:I]?\s*)?(\d{16})')
    nik_match = nik_pattern.search(cleaned_text)
    if nik_match:
        temp_data['NIK'] = nik_match.group(1).replace('I', '1').replace('O', '0')

    return temp_data


def retry_ocr_and_extract(processed_image, file_name):
    """
    Performs multi-attempt Tesseract OCR and feeds the best result to the Gemini API.
    """
    best_raw_text = ""

    # --- Phase 1: Standard PSM Iteration (3 Attempts) ---
    for i, config in enumerate(TESSERACT_CONFIGS):
        attempt = i + 1
        try:
            raw_text = pytesseract.image_to_string(processed_image, lang='ind', config=config)
            # Use the legacy RegEx extractor to quickly check for a valid NIK
            preliminary_data = extract_ktp_fields(raw_text)

            # If NIK is found, we consider this raw text the best for parsing
            if preliminary_data.get('NIK') and len(preliminary_data['NIK']) == 16:
                best_raw_text = raw_text
                break

            # If NIK is not found, but we have text, keep the text from the most recent attempt
            if raw_text and not best_raw_text:
                 best_raw_text = raw_text

        except Exception as e:
            pass

    if not best_raw_text:
        return {'NIK': 'OCR Failed'}, ""

    # --- Phase 2: Gemini AI Parsing ---
    extracted_data = call_gemini_parser(best_raw_text)

    # If Gemini parsing fails, fall back to the raw text for display
    if not extracted_data:
        return {'NIK': 'AI Parsing Failed', 'Status': 'Check Raw Text Above'}, best_raw_text

    return extracted_data, best_raw_text

@csrf_exempt
@require_POST
def process_ktp_ocr(request):
    """
    Process KTP image for OCR and return extracted data
    """
    try:
        if 'ktp_image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)

        image_file = request.FILES['ktp_image']

        # Validate file type
        if not image_file.content_type in ['image/jpeg', 'image/jpg', 'image/png']:
            return JsonResponse({'error': 'Invalid file type. Only JPG and PNG are allowed.'}, status=400)

        # Validate file size (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'File size too large. Maximum 5MB allowed.'}, status=400)

        # Read image data
        image_data = image_file.read()

        # Preprocess the image
        processed_image = preprocess_image(image_data)

        if processed_image is None:
            return JsonResponse({'error': 'Image preprocessing failed'}, status=500)

        # Run the multi-check OCR and Gemini parsing
        extracted_data, raw_text = retry_ocr_and_extract(processed_image, image_file.name)

        # Map extracted data to model fields
        mapped_data = {
            'nik': extracted_data.get('NIK', ''),
            'nama': extracted_data.get('Nama', ''),
            'ttl': extracted_data.get('Tempat/Tgl Lahir', ''),
            'jk': extracted_data.get('Jenis Kelamin', ''),
            'status_perkawinan': extracted_data.get('Status Perkawinan', ''),
            'alamat': extracted_data.get('Alamat', ''),
            # Add other fields as needed
        }

        return JsonResponse({
            'success': True,
            'data': mapped_data,
            'raw_text': raw_text
        })

    except Exception as e:
        return JsonResponse({'error': f'OCR processing failed: {str(e)}'}, status=500)


@login_required
def list_pendaftaran(request):
    """
    Admin-only list of registrations with links to review.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("Forbidden")

    items = PendaftaranAK1.objects.all().order_by('-created_at')
    
    # Get counts by status
    pending_count = PendaftaranAK1.objects.filter(status='pending').count()
    approved_count = PendaftaranAK1.objects.filter(status='diverifikasi').count()
    rejected_count = PendaftaranAK1.objects.filter(status='ditolak').count()
    
    context = {
        'items': items,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'pendaftaran/list_pendaftaran.html', context)


@login_required
def review_pendaftaran(request, pk):
    """
    Admin review page: allow approve/reject with optional comment.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("Forbidden")

    try:
        obj = PendaftaranAK1.objects.get(pk=pk)
    except PendaftaranAK1.DoesNotExist:
        messages.error(request, "Pendaftaran tidak ditemukan.")
        return redirect('list_pendaftaran')

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        comment = request.POST.get('comment', '').strip()

        # Log the action for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Review POST received: action={action}, pk={pk}, user={request.user}")

        if action == 'approve':
            try:
                obj.status = 'diverifikasi'
                obj.verified_at = timezone.now()
                obj.reviewed_at = timezone.now()
                obj.reviewed_by = request.user
                obj.review_comment = comment if comment else ''
                obj.save()
                messages.success(request, f'✓ Pendaftaran atas nama {obj.nama} telah DISETUJUI. Kartu AK1 dapat diunduh.')
                logger.info(f"Approval saved successfully for pendaftaran {pk}")
                return redirect('list_pendaftaran')
            except Exception as e:
                logger.error(f"Error approving: {str(e)}", exc_info=True)
                messages.error(request, f'Terjadi kesalahan saat menyetujui: {str(e)}')
        
        elif action == 'reject':
            try:
                obj.status = 'ditolak'
                obj.reviewed_at = timezone.now()
                obj.reviewed_by = request.user
                obj.review_comment = comment if comment else 'Ditolak oleh petugas'
                obj.save()
                messages.success(request, f'✓ Pendaftaran atas nama {obj.nama} telah DITOLAK.')
                logger.info(f"Rejection saved successfully for pendaftaran {pk}")
                return redirect('list_pendaftaran')
            except Exception as e:
                logger.error(f"Error rejecting: {str(e)}", exc_info=True)
                messages.error(request, f'Terjadi kesalahan saat menolak: {str(e)}')
        
        else:
            messages.error(request, f'Aksi tidak valid. Silakan gunakan tombol SETUJUI atau TOLAK.')
            logger.warning(f"Invalid action received: '{action}'")

    context = {'obj': obj}
    return render(request, 'pendaftaran/review_pendaftaran.html', context)


@login_required
def download_kartu_pdf(request, pk):
    """
    Generate a professional landscape PDF card for AK1 registration.
    Creates a beautiful card-like design with all registration data.
    """
    try:
        obj = PendaftaranAK1.objects.get(pk=pk)
    except PendaftaranAK1.DoesNotExist:
        messages.error(request, "Pendaftaran tidak ditemukan.")
        return redirect('status_pendaftaran')

    # Permission: owner or staff
    if not (request.user.is_staff or obj.user == request.user):
        return HttpResponseForbidden("Forbidden")

    if obj.status != 'diverifikasi':
        messages.error(request, "Kartu hanya dapat diunduh setelah pendaftaran diverifikasi.")
        return redirect('status_pendaftaran')

    # Import PDF utilities
    from reportlab.lib import colors
    from reportlab.lib.units import cm, mm
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.pdfgen import canvas as pdf_canvas
    
    # Create PDF in memory with LANDSCAPE orientation
    buffer = io.BytesIO()
    width, height = landscape(A4)  # Landscape: 29.7cm x 21cm
    p = pdf_canvas.Canvas(buffer, pagesize=landscape(A4))

    # ===== BACKGROUND =====
    # Yellow background (AK1 Kartu Kuning style)
    p.setFillColor(colors.HexColor('#FED602'))  # Bright yellow
    p.rect(0, 0, width, height, fill=1, stroke=0)

    # White card area with rounded corners effect
    margin = 0.4 * cm
    card_x = margin
    card_y = margin
    card_width = width - (2 * margin)
    card_height = height - (2 * margin)
    p.setFillColor(colors.white)
    p.setLineWidth(2)
    p.setStrokeColor(colors.HexColor('#FED602'))
    p.rect(card_x, card_y, card_width, card_height, fill=1, stroke=1)

    # ===== HEADER SECTION =====
    header_y = height - 1.2 * cm
    p.setFont('Helvetica-Bold', 13)
    p.setFillColor(colors.HexColor('#1a472a'))  # Dark green
    p.drawString(1.2 * cm, header_y, 'KARTU PENCARI KERJA AK-1')
    
    p.setFont('Helvetica', 9)
    p.setFillColor(colors.HexColor('#666666'))
    p.drawString(1.2 * cm, header_y - 0.35 * cm, 'Dinas Tenaga Kerja Kabupaten Minahasa')

    # Right side header - AK1 Logo area
    p.setFont('Helvetica-Bold', 40)
    p.setFillColor(colors.HexColor('#FED602'))
    p.drawCentredString(width - 1.5 * cm, header_y - 0.3 * cm, 'AK-1')
    
    # Divider line
    p.setLineWidth(1.5)
    p.setStrokeColor(colors.HexColor('#1a472a'))
    p.line(1.2 * cm, header_y - 0.8 * cm, width - 1.2 * cm, header_y - 0.8 * cm)

    # ===== LEFT COLUMN - DATA =====
    left_col = 1.5 * cm
    right_col = 11 * cm
    data_y = header_y - 1.3 * cm
    line_height = 0.42 * cm

    # Define fields
    fields = [
        ('NIK', obj.nik or '-'),
        ('Nama Lengkap', obj.nama or '-'),
        ('Tempat Lahir', obj.ttl[:10] if obj.ttl else '-'),  # Just date part
        ('Tanggal Lahir', obj.ttl[10:] if obj.ttl and len(obj.ttl) > 10 else '-'),
        ('Jenis Kelamin', obj.jk or '-'),
        ('Status Perkawinan', obj.status_perkawinan or '-'),
        ('Pendidikan', obj.pendidikan or '-'),
        ('Agama', obj.agama or '-'),
    ]

    # Draw left column data
    p.setFont('Helvetica-Bold', 9)
    p.setFillColor(colors.HexColor('#1a472a'))
    
    for i, (label, value) in enumerate(fields[:8]):
        y = data_y - (i * line_height)
        # Label
        p.setFont('Helvetica-Bold', 9)
        p.drawString(left_col, y, label)
        # Separator
        p.setFont('Helvetica', 9)
        p.drawString(left_col + 2.8 * cm, y, ':')
        # Value
        p.setFont('Helvetica', 9)
        p.setFillColor(colors.black)
        value_str = str(value)[:35]  # Truncate long values
        p.drawString(left_col + 3.0 * cm, y, value_str)
        p.setFillColor(colors.HexColor('#1a472a'))

    # ===== RIGHT COLUMN - ADDITIONAL INFO =====
    right_data_y = data_y
    # Safely obtain email from related user (PendaftaranAK1 has no direct email field)
    email_value = '-'
    try:
        if getattr(obj, 'user', None):
            email_value = getattr(obj.user, 'email', None) or getattr(obj.user, 'username', '-')
    except Exception:
        email_value = '-'

    right_fields = [
        ('Keahlian', obj.keahlian or '-'),
        ('Pengalaman', obj.pengalaman or '-'),
        ('Email', email_value),
        ('Alamat', (obj.alamat or '-')[:40]),
        ('Tgl Pendaftaran', obj.created_at.strftime('%d-%m-%Y') if obj.created_at else '-'),
        ('Status', 'DIVERIFIKASI' if obj.status == 'diverifikasi' else obj.status),
    ]

    p.setFillColor(colors.HexColor('#1a472a'))
    
    for i, (label, value) in enumerate(right_fields):
        y = right_data_y - (i * line_height)
        # Label
        p.setFont('Helvetica-Bold', 9)
        p.drawString(right_col, y, label)
        # Separator
        p.setFont('Helvetica', 9)
        p.drawString(right_col + 2.5 * cm, y, ':')
        # Value
        p.setFont('Helvetica', 9)
        p.setFillColor(colors.black)
        value_str = str(value)[:35]
        p.drawString(right_col + 2.7 * cm, y, value_str)
        p.setFillColor(colors.HexColor('#1a472a'))

    # ===== MIDDLE SECTION - PHOTO AREA =====
    photo_x = width - 4 * cm
    photo_y = data_y - 2.5 * cm
    photo_size = 2.5 * cm
    
    # Photo frame
    p.setLineWidth(1.5)
    p.setStrokeColor(colors.HexColor('#1a472a'))
    p.setFillColor(colors.HexColor('#f0f0f0'))
    p.rect(photo_x, photo_y - photo_size, photo_size, photo_size, fill=1, stroke=1)
    
    # Try to draw photo if exists (use base64 `photo_data` or fallback)
    try:
        photo_drawn = False
        from reportlab.lib.utils import ImageReader
        # If model stores base64 image bytes in `photo_data`, decode and draw
        if getattr(obj, 'photo_data', None):
            import base64 as _base64
            from io import BytesIO as _BytesIO
            try:
                img_bytes = _base64.b64decode(obj.photo_data)
                img_buf = _BytesIO(img_bytes)
                img_reader = ImageReader(img_buf)
                p.drawImage(img_reader, photo_x + 0.05 * cm, photo_y - photo_size + 0.05 * cm,
                            width=photo_size - 0.1 * cm, height=photo_size - 0.1 * cm, preserveAspectRatio=True)
                photo_drawn = True
            except Exception:
                photo_drawn = False

        # Optional: fallback to a user-stored file path if available (custom attribute)
        if not photo_drawn and getattr(obj, 'user', None):
            user = obj.user
            user_photo_path = getattr(user, 'photo_path', None) or getattr(user, 'profile_photo_path', None)
            if user_photo_path:
                try:
                    img_reader = ImageReader(user_photo_path)
                    p.drawImage(img_reader, photo_x + 0.05 * cm, photo_y - photo_size + 0.05 * cm,
                                width=photo_size - 0.1 * cm, height=photo_size - 0.1 * cm, preserveAspectRatio=True)
                    photo_drawn = True
                except Exception:
                    photo_drawn = False

        if not photo_drawn:
            p.setFont('Helvetica', 8)
            p.setFillColor(colors.HexColor('#999999'))
            p.drawCentredString(photo_x + photo_size / 2, photo_y - photo_size / 2, '[FOTO]')
    except Exception:
        p.setFont('Helvetica', 8)
        p.setFillColor(colors.HexColor('#999999'))
        p.drawCentredString(photo_x + photo_size / 2, photo_y - photo_size / 2, '[FOTO]')

    # ===== BOTTOM SECTION - SIGNATURE & DATE =====
    bottom_y = 1.2 * cm
    
    # Left: Tanggal Terbit
    p.setFont('Helvetica-Bold', 9)
    p.setFillColor(colors.HexColor('#1a472a'))
    p.drawString(1.5 * cm, bottom_y + 0.3 * cm, 'Tanggal Terbit:')
    
    p.setFont('Helvetica', 9)
    issued_date = obj.verified_at.strftime('%d-%m-%Y') if obj.verified_at else '-'
    p.drawString(1.5 * cm, bottom_y - 0.2 * cm, issued_date)

    # Center: QR Code / Registration Number
    p.setFont('Helvetica-Bold', 9)
    p.drawCentredString(width / 2, bottom_y + 0.3 * cm, 'NOMOR REGISTRASI')
    p.setFont('Helvetica', 11)
    p.setFillColor(colors.HexColor('#1a472a'))
    p.drawCentredString(width / 2, bottom_y - 0.2 * cm, f"AK1-{obj.id:06d}")

    # Right: Signature area
    p.setFont('Helvetica-Bold', 9)
    p.setFillColor(colors.HexColor('#1a472a'))
    p.drawCentredString(width - 2.5 * cm, bottom_y + 0.3 * cm, 'Petugas Verifikasi')
    
    # Signature line
    p.setLineWidth(0.5)
    p.setStrokeColor(colors.black)
    p.line(width - 3.5 * cm, bottom_y - 0.5 * cm, width - 1.5 * cm, bottom_y - 0.5 * cm)
    
    # Signature name
    reviewer_name = obj.reviewed_by.get_full_name() if obj.reviewed_by else '_______________'
    p.setFont('Helvetica', 8)
    p.setFillColor(colors.HexColor('#666666'))
    p.drawCentredString(width - 2.5 * cm, bottom_y - 0.8 * cm, reviewer_name)

    # ===== FOOTER =====
    p.setFont('Helvetica', 7)
    p.setFillColor(colors.HexColor('#999999'))
    footer_text = 'Kartu ini adalah bukti resmi pendaftaran pencari kerja dan berlaku tanpa batas waktu'
    p.drawCentredString(width / 2, 0.4 * cm, footer_text)

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=AK1_Card_{obj.nik}.pdf'
    return response
