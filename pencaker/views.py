from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
import json
import base64
import io
from PIL import Image

from pendaftaran.models import PendaftaranAK1
from .forms import KTPUploadForm, PendaftaranAK1KTPForm
from .ocr_utils import process_ktp_image, preprocess_and_ocr, analyze_ktp_with_gemini


@login_required
def dashboard(request):
    """Dashboard pencaker - lihat data pendaftaran"""
    try:
        pendaftaran = PendaftaranAK1.objects.get(user=request.user)
    except PendaftaranAK1.DoesNotExist:
        pendaftaran = None
    
    context = {
        'pendaftaran': pendaftaran,
    }
    return render(request, 'pencaker/dashboard.html', context)


@login_required
def upload_ktp(request):
    """Upload KTP dan auto-fill data pendaftaran"""
    if request.method == 'POST':
        form = KTPUploadForm(request.POST, request.FILES)
        if form.is_valid():
            ktp_image = request.FILES['ktp_image']
            
            try:
                # Process KTP image
                extracted_data, error = process_ktp_image(ktp_image)
                
                # If OCR/Gemini failed, show error and reload form
                if error or not extracted_data:
                    error_msg = error if error else "Gagal mengekstrak data KTP. Data kosong atau tidak valid."
                    messages.error(request, f"❌ {error_msg}")
                    # Reset form - do NOT pre-fill with error data
                    form = KTPUploadForm()
                    return render(request, 'pencaker/upload_ktp.html', {'form': form})
                
                # Validate extracted data has key fields
                if not extracted_data.get('nik') or not extracted_data.get('nama'):
                    messages.error(request, "❌ Gagal mengekstrak NIK atau Nama dari KTP. Coba gambar yang lebih jelas.")
                    form = KTPUploadForm()
                    return render(request, 'pencaker/upload_ktp.html', {'form': form})
                
                # Success - store in session and redirect
                ktp_image.seek(0)  # Reset file pointer
                request.session['ktp_data'] = {
                    'extracted': extracted_data,
                    'ktp_image_data': base64.b64encode(ktp_image.read()).decode('utf-8'),
                }
                
                messages.success(request, "✅ KTP berhasil diproses! Verifikasi data di bawah.")
                return redirect('pencaker:review_ktp')
            
            except Exception as e:
                messages.error(request, f"❌ Terjadi kesalahan saat memproses KTP: {str(e)}")
                form = KTPUploadForm()
                return render(request, 'pencaker/upload_ktp.html', {'form': form})
    else:
        form = KTPUploadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pencaker/upload_ktp.html', context)


@login_required
def review_ktp(request):
    """Review extracted KTP data sebelum disimpan"""
    ktp_data = request.session.get('ktp_data', {})
    
    if not ktp_data:
        messages.warning(request, "⚠️ Tidak ada data KTP. Silakan upload KTP terlebih dahulu.")
        return redirect('pencaker:upload_ktp')
    
    extracted = ktp_data.get('extracted', {})
    
    # Extra validation - make sure we have actual data, not error messages
    if not extracted or not isinstance(extracted, dict):
        messages.error(request, "❌ Data KTP tidak valid. Silakan upload ulang.")
        return redirect('pencaker:upload_ktp')
    
    if request.method == 'POST':
        # Ambil data dari form (user bisa mengedit)
        nik = request.POST.get('nik', '').strip()
        nama = request.POST.get('nama', '').strip()
        ttl = request.POST.get('ttl', '').strip()  # Tempat, DD-MM-YYYY
        jk = request.POST.get('jk', '').strip()
        status_perkawinan = request.POST.get('status_perkawinan', '').strip()
        alamat = request.POST.get('alamat', '').strip()
        
        # Validasi field penting
        if not all([nik, nama, ttl, jk, alamat]):
            messages.error(request, "❌ NIK, Nama, TTL, Jenis Kelamin, dan Alamat harus diisi!")
            return render(request, 'pencaker/review_ktp.html', {'extracted': extracted})
        
        # Reject obviously invalid data (like error messages)
        if 'gagal' in nama.lower() or 'error' in nama.lower():
            messages.error(request, "❌ Nama terlihat seperti pesan error. Silakan upload KTP yang lebih jelas.")
            return redirect('pencaker:upload_ktp')
        
        try:
            # Create or update PendaftaranAK1
            pendaftaran, created = PendaftaranAK1.objects.update_or_create(
                user=request.user,
                defaults={
                    'nik': nik,
                    'nama': nama,
                    'ttl': ttl,
                    'jk': jk,
                    'status_perkawinan': status_perkawinan,
                    'alamat': alamat,
                    'ktp_data': ktp_data.get('ktp_image_data', ''),
                }
            )
            
            # Clear session
            if 'ktp_data' in request.session:
                del request.session['ktp_data']
            
            messages.success(request, "✅ Data KTP berhasil disimpan! Silakan lengkapi data tambahan.")
            return redirect('pencaker:isi_data_diri')
        
        except Exception as e:
            messages.error(request, f"❌ Error menyimpan data: {str(e)}")
            return render(request, 'pencaker/review_ktp.html', {'extracted': extracted})
    
    context = {
        'extracted': extracted,
        'ktp_image_data': ktp_data.get('ktp_image_data', ''),
    }
    return render(request, 'pencaker/review_ktp.html', context)


@login_required
def isi_data_diri(request):
    """Form pengisian data diri lengkap"""
    try:
        pendaftaran = PendaftaranAK1.objects.get(user=request.user)
    except PendaftaranAK1.DoesNotExist:
        messages.warning(request, "Silakan upload KTP terlebih dahulu.")
        return redirect('pencaker:upload_ktp')
    
    if request.method == 'POST':
        form = PendaftaranAK1KTPForm(request.POST, request.FILES, instance=pendaftaran)
        if form.is_valid():
            # Handle file uploads
            if 'ktp' in request.FILES:
                ktp_file = request.FILES['ktp']
                pendaftaran.ktp_data = base64.b64encode(ktp_file.read()).decode('utf-8')
            
            if 'photo' in request.FILES:
                photo_file = request.FILES['photo']
                pendaftaran.photo_data = base64.b64encode(photo_file.read()).decode('utf-8')
            
            if 'ijazah' in request.FILES:
                ijazah_file = request.FILES['ijazah']
                pendaftaran.ijazah_data = base64.b64encode(ijazah_file.read()).decode('utf-8')
            
            form.save()
            messages.success(request, "Data berhasil disimpan!")
            return redirect('pencaker:dashboard')
    else:
        form = PendaftaranAK1KTPForm(instance=pendaftaran)
    
    context = {
        'form': form,
        'pendaftaran': pendaftaran,
    }
    return render(request, 'pencaker/isi_data_diri.html', context)


@login_required
@require_http_methods(["POST"])
def preview_ktp_ajax(request):
    """AJAX endpoint untuk preview KTP yang di-upload"""
    if 'ktp_image' not in request.FILES:
        return JsonResponse({'error': 'Tidak ada file KTP'}, status=400)
    
    ktp_image = request.FILES['ktp_image']
    
    try:
        # Convert to base64 untuk preview
        image_data = base64.b64encode(ktp_image.read()).decode('utf-8')
        return JsonResponse({
            'success': True,
            'preview': f'data:image/jpeg;base64,{image_data}'
        })
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=400)


@login_required
@require_http_methods(["POST"])
def extract_ktp_ajax(request):
    """AJAX endpoint untuk extract KTP tanpa upload form"""
    if 'ktp_image' not in request.FILES:
        return JsonResponse({'error': 'Tidak ada file KTP'}, status=400)
    
    ktp_image = request.FILES['ktp_image']
    
    try:
        # Process KTP
        extracted_data, error = process_ktp_image(ktp_image)
        
        if error:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({
            'success': True,
            'data': extracted_data
        })
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=400)


@login_required
def test_ocr(request):
    """Debug page untuk test OCR (hanya untuk development)"""
    if not settings.DEBUG:
        return HttpResponse("Not available in production", status=403)
    
    if request.method == 'POST' and 'ktp_image' in request.FILES:
        ktp_image = request.FILES['ktp_image']
        
        try:
            # Step 1: Basic OCR
            image = Image.open(ktp_image)
            if image.mode not in ('L', 'RGB', 'RGBA'):
                image = image.convert('RGB')
            
            ocr_text, metadata = preprocess_and_ocr(image)
            
            # Step 2: Gemini extraction
            extracted_data, error = analyze_ktp_with_gemini(ocr_text)
            
            context = {
                'ocr_text': ocr_text,
                'metadata': json.dumps(metadata, indent=2, ensure_ascii=False),
                'extracted_data': json.dumps(extracted_data, indent=2, ensure_ascii=False),
                'error': error,
            }
            return render(request, 'pencaker/test_ocr.html', context)
        except Exception as e:
            context = {
                'error': f'Error: {str(e)}',
            }
            return render(request, 'pencaker/test_ocr.html', context)
    
    return render(request, 'pencaker/test_ocr.html', {})
