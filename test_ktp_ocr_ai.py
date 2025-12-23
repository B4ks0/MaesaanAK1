import os
import sys
import django
from PIL import Image
import pytesseract
import google.generativeai as genai
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
django.setup()

# Configure Gemini AI
genai.configure(api_key='AIzaSyDUMMY_KEY')  # Replace with actual API key

def extract_text_with_tesseract(image_path):
    """
    Extract text from image using Tesseract OCR
    """
    try:
        image = Image.open(image_path)
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        # Extract text with Indonesian and English languages
        text = pytesseract.image_to_string(image, lang='ind+eng')
        return text.strip()
    except Exception as e:
        print(f"❌ Tesseract OCR failed: {e}")
        return None

def extract_form_data_with_ai(ocr_text):
    """
    Use Gemini AI to extract form-fillable data from OCR text
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Extract the following information from this Indonesian KTP (Identity Card) text.
        Return ONLY a JSON object with these exact keys:
        - nik: The 16-digit NIK number
        - nama: Full name
        - tempat_lahir: Place of birth
        - tanggal_lahir: Date of birth (DD-MM-YYYY format)
        - jenis_kelamin: Gender (LAKI-LAKI or PEREMPUAN)
        - status_perkawinan: Marital status
        - alamat: Complete address
        - agama: Religion
        - pekerjaan: Occupation
        - kewarganegaraan: Nationality

        If a field is not found, use null.
        KTP Text:
        {ocr_text}
        """

        response = model.generate_content(prompt)
        result_text = response.text.strip()

        # Clean up the response (remove markdown code blocks if present)
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
        result_text = result_text.strip()

        # Parse JSON
        data = json.loads(result_text)
        return data

    except Exception as e:
        print(f"❌ Gemini AI extraction failed: {e}")
        return None

def test_ktp_ocr_ai():
    """
    Test KTP OCR with AI data extraction
    """
    image_path = r"C:\laragon\www\ak1\ktp_test.jpg"

    print("=" * 60)
    print("KTP OCR AI TEST")
    print("=" * 60)

    if not os.path.exists(image_path):
        print(f"❌ KTP image not found: {image_path}")
        return

    print(f"📁 Testing image: {image_path}")
    print()

    # Step 1: OCR with Tesseract
    print("🔍 Step 1: Tesseract OCR Processing...")
    ocr_text = extract_text_with_tesseract(image_path)

    if ocr_text:
        print("✅ Tesseract OCR successful!")
        print()
        print("📄 Raw OCR Text (Pool of Texts):")
        print("-" * 50)
        print(ocr_text)
        print("-" * 50)
        print()
    else:
        print("❌ OCR failed, cannot proceed")
        return

    # Step 2: AI Data Extraction
    print("🤖 Step 2: Gemini AI Data Extraction...")
    form_data = extract_form_data_with_ai(ocr_text)

    if form_data:
        print("✅ AI extraction successful!")
        print()
        print("📋 Extracted Form Data:")
        print("-" * 50)
        for key, value in form_data.items():
            print(f"{key}: {value}")
        print("-" * 50)
        print()

        # Save results
        results = {
            'image_path': image_path,
            'ocr_text': ocr_text,
            'extracted_data': form_data
        }

        with open('ktp_ocr_ai_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("💾 Results saved to ktp_ocr_ai_results.json")
        print()

        # Form fill simulation
        print("📝 Form Auto-Fill Simulation:")
        print("-" * 50)
        print("NIK:", form_data.get('nik', 'Not found'))
        print("Nama Lengkap:", form_data.get('nama', 'Not found'))
        print("Tempat Lahir:", form_data.get('tempat_lahir', 'Not found'))
        print("Tanggal Lahir:", form_data.get('tanggal_lahir', 'Not found'))
        print("Jenis Kelamin:", form_data.get('jenis_kelamin', 'Not found'))
        print("Status Perkawinan:", form_data.get('status_perkawinan', 'Not found'))
        print("Alamat Lengkap:", form_data.get('alamat', 'Not found'))
        print("Agama:", form_data.get('agama', 'Not found'))
        print("Pekerjaan:", form_data.get('pekerjaan', 'Not found'))
        print("Kewarganegaraan:", form_data.get('kewarganegaraan', 'Not found'))
        print("-" * 50)

    else:
        print("❌ AI extraction failed")
        return

    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_ktp_ocr_ai()
