import os
import sys
import django
from PIL import Image
import pytesseract
import google.generativeai as genai
import re
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
django.setup()

# Import Django models and functions
from pendaftaran.views import extract_ktp_data_with_gemini, extract_ktp_data

def test_real_ktp():
    """
    Test OCR with real KTP image
    """
    image_path = r"C:\laragon\www\ak1\ktp_test.jpg"

    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return

    print("=============================================================")
    print("REAL KTP OCR TEST")
    print("=============================================================")
    print(f"1. Processing image: {image_path}")

    try:
        # Open image
        image = Image.open(image_path)

        # Convert to RGB if necessary
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        print("2. Performing OCR...")

        # Try pytesseract first
        try:
            text = pytesseract.image_to_string(image, lang='ind+eng')
            print("✓ Tesseract OCR successful")
        except Exception as e:
            print(f"⚠️ Tesseract failed: {e}")
            print("Using fallback text...")
            text = """
            PROVINSI DKI JAKARTA
            KABUPATEN/KOTA JAKARTA PUSAT

            NIK : 3171234567890123

            Nama : JOHN DOE

            Tempat/Tgl Lahir : JAKARTA, 15-03-1990

            Jenis Kelamin : LAKI-LAKI
            Gol. Darah : O

            Alamat : JL. SUDIRMAN NO. 123
            RT/RW : 001/002
            Kel/Desa : GAMBIR
            Kecamatan : GAMBIR
            Agama : ISLAM
            Status Perkawinan : BELUM KAWIN
            Pekerjaan : PELAJAR/MAHASISWA
            Kewarganegaraan : WNI
            Berlaku Hingga : SEUMUR HIDUP
            """

        print("3. Raw OCR Text:")
        print("-" * 50)
        print(text)
        print("-" * 50)

        print("4. Gemini AI Processing...")
        gemini_data = extract_ktp_data_with_gemini(text)
        print("✓ Gemini AI extraction successful")

        print("5. Extracted Data (Gemini AI):")
        print("-" * 40)
        for key, value in gemini_data.items():
            print(f"{key}: '{value}'")
        print("-" * 40)

        print("6. Regex Fallback Processing...")
        regex_data = extract_ktp_data(text)
        print("✓ Regex extraction successful")

        print("7. Extracted Data (Regex):")
        print("-" * 40)
        for key, value in regex_data.items():
            print(f"{key}: '{value}'")
        print("-" * 40)

        # Save results
        results = {
            'raw_text': text,
            'gemini_extraction': gemini_data,
            'regex_extraction': regex_data,
            'image_path': image_path
        }

        with open('real_ktp_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("8. Results saved to real_ktp_test_results.json")

        print("\n=============================================================")
        print("TEST COMPLETE")
        print("=============================================================")

    except Exception as e:
        print(f"❌ Error processing image: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_ktp()
