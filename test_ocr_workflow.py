#!/usr/bin/env python3
"""
Comprehensive test script for OCR workflow with Gemini AI
Shows the complete flow: OCR -> AI Processing -> Form Filling
"""

import os
import json
import google.generativeai as genai
from PIL import Image
import pytesseract
import re

# Configure Gemini AI
genai.configure(api_key="AIzaSyDmChM8Onm2y065nhcxE1DgmORH1KFdbzk")

def extract_ktp_data_with_gemini(text):
    """
    Extract KTP data using Gemini AI
    """
    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Extract the following information from this Indonesian KTP (Identity Card) OCR text.
        Return ONLY a valid JSON object with these exact keys:
        - nik: 16-digit NIK number
        - nama: Full name
        - tempat_lahir: Place of birth
        - tanggal_lahir: Date of birth (DD Month YYYY format)
        - jk: Gender (LAKI-LAKI or PEREMPUAN)
        - status_perkawinan: Marital status (BELUM KAWIN, KAWIN, CERAI HIDUP, or CERAI MATI)
        - alamat: Full address

        If any field is not found, use empty string "".
        Do not include any explanation or additional text, just the JSON.

        KTP Text:
        {text}
        """

        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Clean response (remove markdown code blocks if present)
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        # Parse JSON
        data = json.loads(response_text)

        # Ensure all required keys exist
        required_keys = ['nik', 'nama', 'tempat_lahir', 'tanggal_lahir', 'jk', 'status_perkawinan', 'alamat']
        for key in required_keys:
            if key not in data:
                data[key] = ''

        # Combine tempat and tanggal lahir for ttl field (backward compatibility)
        if data.get('tempat_lahir') and data.get('tanggal_lahir'):
            data['ttl'] = f"{data['tempat_lahir']}, {data['tanggal_lahir']}"
        elif data.get('tempat_lahir') or data.get('tanggal_lahir'):
            data['ttl'] = data['tempat_lahir'] or data['tanggal_lahir']
        else:
            data['ttl'] = ''

        return data

    except Exception as e:
        print(f"Gemini AI extraction failed: {e}")
        # Fallback to regex extraction
        return extract_ktp_data_fallback(text)

def extract_ktp_data_fallback(text):
    """
    Fallback extraction using regex patterns
    """
    data = {
        'nik': '',
        'nama': '',
        'tempat_lahir': '',
        'tanggal_lahir': '',
        'jk': '',
        'status_perkawinan': '',
        'alamat': '',
        'ttl': ''
    }

    # Clean and normalize text
    text = text.upper().replace('\n', ' ').replace('\r', ' ')

    # Extract NIK (16 digits)
    nik_match = re.search(r'\b(\d{16})\b', text)
    if nik_match:
        data['nik'] = nik_match.group(1)

    # Extract Nama
    nama_match = re.search(r'NAMA\s*[:\-]?\s*([A-Z\s]+?)(?=TEMPAT|LAHIR|JENIS|ALAMAT|STATUS|$)', text, re.IGNORECASE)
    if nama_match:
        data['nama'] = nama_match.group(1).strip()

    # Extract Tempat Lahir
    tempat_lahir_match = re.search(r'TEMPAT\s*LAHIR\s*[:\-]?\s*([A-Z\s]+?)(?=,\s*\d|\d{1,2}|\s*\d{1,2})', text, re.IGNORECASE)
    if tempat_lahir_match:
        data['tempat_lahir'] = tempat_lahir_match.group(1).strip()

    # Extract Tanggal Lahir
    tanggal_lahir_match = re.search(r'(\d{1,2}\s*(?:JANUARI|FEBRUARI|MARET|APRIL|MEI|JUNI|JULI|AGUSTUS|SEPTEMBER|OKTOBER|NOVEMBER|DESEMBER)\s*\d{4})', text, re.IGNORECASE)
    if tanggal_lahir_match:
        data['tanggal_lahir'] = tanggal_lahir_match.group(1).strip()

    # Combine for ttl
    if data['tempat_lahir'] and data['tanggal_lahir']:
        data['ttl'] = f"{data['tempat_lahir']}, {data['tanggal_lahir']}"

    # Extract Jenis Kelamin
    if 'LAKI-LAKI' in text or 'LAKI LAKI' in text:
        data['jk'] = 'LAKI-LAKI'
    elif 'PEREMPUAN' in text:
        data['jk'] = 'PEREMPUAN'

    # Extract Status Perkawinan
    status_patterns = [
        r'STATUS\s*(?:PERKAWINAN)?\s*[:\-]?\s*(BELUM\s*KAWIN|KAWIN|CERAI\s*HIDUP|CERAI\s*MATI)',
        r'(BELUM\s*KAWIN|KAWIN|CERAI\s*HIDUP|CERAI\s*MATI)',
    ]
    for pattern in status_patterns:
        status_match = re.search(pattern, text, re.IGNORECASE)
        if status_match:
            data['status_perkawinan'] = status_match.group(1).upper().replace(' ', '')
            break

    # Extract Alamat
    alamat_match = re.search(r'ALAMAT\s*[:\-]?\s*([A-Z0-9\s,\.\-\(\)]+?)(?=RT|RW|KELURAHAN|KECAMATAN|KABUPATEN|KOTA|PROVINSI|KODE\s*POS|AGAMA|STATUS|GOL\.?\s*DARAH|$)', text, re.IGNORECASE)
    if alamat_match:
        data['alamat'] = alamat_match.group(1).strip()

    return data

def simulate_ocr_workflow(image_path=None):
    """
    Simulate the complete OCR workflow
    """
    print("=" * 60)
    print("OCR WORKFLOW TEST")
    print("=" * 60)

    # Sample KTP text (simulating OCR output)
    sample_ktp_text = """
    PROVINSI DKI JAKARTA
    KABUPATEN/KOTA JAKARTA PUSAT
    NIK 3171234567890123
    Nama JOHN DOE
    Tempat Lahir JAKARTA
    15 MARET 1990
    Jenis Kelamin LAKI-LAKI
    Alamat JL. SUDIRMAN NO. 123, RT 001 RW 002
    KELURAHAN TANAH ABANG
    KECAMATAN TANAH ABANG
    Status Perkawinan BELUM KAWIN
    """

    if image_path and os.path.exists(image_path):
        print(f"1. Processing image: {image_path}")
        try:
            image = Image.open(image_path)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')

            custom_config = r'--oem 3 --psm 6 -l ind+eng'
            ocr_text = pytesseract.image_to_string(image, config=custom_config)
            print("2. Raw OCR Text:")
            print("-" * 40)
            print(ocr_text)
            print("-" * 40)
        except Exception as e:
            print(f"OCR failed: {e}")
            print("Using sample text instead...")
            ocr_text = sample_ktp_text
    else:
        print("1. No image provided, using sample KTP text")
        ocr_text = sample_ktp_text
        print("2. Raw OCR Text:")
        print("-" * 40)
        print(ocr_text)
        print("-" * 40)

    # Step 3: Gemini AI Processing
    print("\n3. Gemini AI Processing...")
    try:
        gemini_data = extract_ktp_data_with_gemini(ocr_text)
        print("✓ Gemini AI extraction successful")
        print("4. Extracted Data (Gemini AI):")
        print("-" * 40)
        for key, value in gemini_data.items():
            print(f"{key}: '{value}'")
        print("-" * 40)
    except Exception as e:
        print(f"✗ Gemini AI extraction failed: {e}")
        gemini_data = None

    # Step 4: Fallback Processing
    if not gemini_data:
        print("\n4. Using fallback regex extraction...")
        fallback_data = extract_ktp_data_fallback(ocr_text)
        print("Extracted Data (Regex Fallback):")
        print("-" * 40)
        for key, value in fallback_data.items():
            print(f"{key}: '{value}'")
        print("-" * 40)

    # Step 5: Form Filling Simulation
    print("\n5. Form Auto-Fill Simulation:")
    print("-" * 40)
    form_data = gemini_data if gemini_data else fallback_data

    print("Registration Form Fields:")
    print(f"NIK: {form_data.get('nik', '')}")
    print(f"Nama Lengkap: {form_data.get('nama', '')}")
    print(f"Tempat/Tanggal Lahir: {form_data.get('ttl', '')}")
    print(f"Jenis Kelamin: {form_data.get('jk', '')}")
    print(f"Status Perkawinan: {form_data.get('status_perkawinan', '')}")
    print(f"Alamat Lengkap: {form_data.get('alamat', '')}")

    print("\n" + "=" * 60)
    print("WORKFLOW COMPLETE")
    print("=" * 60)

    return form_data

if __name__ == "__main__":
    # Test with sample image if available
    image_path = "image.png"  # Change this to your KTP image path

    result = simulate_ocr_workflow(image_path)

    # Save results to file for inspection
    with open('ocr_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\nResults saved to ocr_test_results.json")
