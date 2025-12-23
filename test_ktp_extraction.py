#!/usr/bin/env python3
"""
Test script for KTP data extraction
"""

def extract_ktp_data(text):
    """
    Extract relevant data from KTP OCR text
    """
    data = {
        'nik': '',
        'nama': '',
        'tempat_lahir': '',
        'tanggal_lahir': '',
        'jk': '',
        'status_perkawinan': '',
        'alamat': ''
    }

    # Clean and normalize text
    text = text.upper().replace('\n', ' ').replace('\r', ' ')

    # Extract NIK (16 digits)
    nik_match = re.search(r'\b(\d{16})\b', text)
    if nik_match:
        data['nik'] = nik_match.group(1)

    # Extract Nama (usually after "NAMA" or similar)
    nama_match = re.search(r'NAMA\s*[:\-]?\s*([A-Z\s]+?)(?=TEMPAT|LAHIR|JENIS|ALAMAT|STATUS|$)', text, re.IGNORECASE)
    if nama_match:
        data['nama'] = nama_match.group(1).strip()

    # Extract Tempat Lahir (place of birth)
    tempat_lahir_match = re.search(r'TEMPAT\s*LAHIR\s*[:\-]?\s*([A-Z\s]+?)(?=,\s*\d|\d{1,2}|\s*\d{1,2})', text, re.IGNORECASE)
    if tempat_lahir_match:
        data['tempat_lahir'] = tempat_lahir_match.group(1).strip()

    # Extract Tanggal Lahir (date of birth)
    tanggal_lahir_match = re.search(r'(\d{1,2}\s*(?:JANUARI|FEBRUARI|MARET|APRIL|MEI|JUNI|JULI|AGUSTUS|SEPTEMBER|OKTOBER|NOVEMBER|DESEMBER)\s*\d{4})', text, re.IGNORECASE)
    if tanggal_lahir_match:
        data['tanggal_lahir'] = tanggal_lahir_match.group(1).strip()
    else:
        # Fallback: extract date pattern like DD-MM-YYYY or DD/MM/YYYY
        date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})', text)
        if date_match:
            data['tanggal_lahir'] = date_match.group(1)

    # Combine tempat and tanggal lahir for ttl field (backward compatibility)
    if data['tempat_lahir'] and data['tanggal_lahir']:
        data['ttl'] = f"{data['tempat_lahir']}, {data['tanggal_lahir']}"
    elif data['tempat_lahir'] or data['tanggal_lahir']:
        data['ttl'] = data['tempat_lahir'] or data['tanggal_lahir']

    # Extract Jenis Kelamin
    if 'LAKI-LAKI' in text or 'LAKI LAKI' in text:
        data['jk'] = 'LAKI-LAKI'
    elif 'PEREMPUAN' in text:
        data['jk'] = 'PEREMPUAN'

    # Extract Status Perkawinan (marital status)
    status_patterns = [
        r'STATUS\s*(?:PERKAWINAN)?\s*[:\-]?\s*(BELUM\s*KAWIN|KAWIN|CERAI\s*HIDUP|CERAI\s*MATI)',
        r'(BELUM\s*KAWIN|KAWIN|CERAI\s*HIDUP|CERAI\s*MATI)',
    ]
    for pattern in status_patterns:
        status_match = re.search(pattern, text, re.IGNORECASE)
        if status_match:
            data['status_perkawinan'] = status_match.group(1).upper().replace(' ', '')
            break

    # Extract Alamat Lengkap (full address) - improved pattern
    alamat_match = re.search(r'ALAMAT\s*[:\-]?\s*([A-Z0-9\s,\.\-\(\)]+?)(?=RT|RW|KELURAHAN|KECAMATAN|KABUPATEN|KOTA|PROVINSI|KODE\s*POS|AGAMA|STATUS|GOL\.?\s*DARAH|$)', text, re.IGNORECASE)
    if alamat_match:
        data['alamat'] = alamat_match.group(1).strip()
    else:
        # Fallback: broader address pattern
        alamat_fallback = re.search(r'ALAMAT\s*[:\-]?\s*(.+?)(?=AGAMA|STATUS|GOL\.?\s*DARAH|NIK|$)', text, re.IGNORECASE)
        if alamat_fallback:
            data['alamat'] = alamat_fallback.group(1).strip()

    return data

if __name__ == "__main__":
    import re

    # Sample KTP text for testing
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

    print("Testing KTP data extraction...")
    print("Sample KTP text:")
    print(sample_ktp_text)
    print("\nExtracted data:")
    extracted = extract_ktp_data(sample_ktp_text)
    for key, value in extracted.items():
        print(f"{key}: '{value}'")
