#!/usr/bin/env python
"""Test what Gemini actually returns for KTP data extraction"""

import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
sys.path.insert(0, r'c:\laragon\www\ak1')

django.setup()

from pencaker.ocr_utils import analyze_ktp_with_gemini, format_extracted_data

sample_ocr = """
NO. INDUK KEPENDUDUKAN
3520451234567890

NAMA
JOHN DOE

TEMPAT/TGL.LAHIR
JAKARTA 15 MEI 1990

JENIS KELAMIN
LAKI-LAKI

STATUS PERKAWINAN
KAWIN

ALAMAT
JL MERDEKA NO 123
JAKARTA 12345

AGAMA
ISLAM

PEKERJAAN
PEGAWAI NEGERI SIPIL

KEWARGANEGARAAN
WNI
"""

print("=" * 60)
print("Testing Gemini Response...")
print("=" * 60)

data, error = analyze_ktp_with_gemini(sample_ocr.strip())

print("\n[RAW GEMINI OUTPUT]")
print("Keys returned:", list(data.keys()) if data else "EMPTY")
print("Full data:")
print(json.dumps(data, indent=2, ensure_ascii=False))

if error:
    print(f"\nERROR: {error}")
else:
    print("\n[AFTER FORMAT_EXTRACTED_DATA]")
    formatted = format_extracted_data(data)
    print("Keys after formatting:", list(formatted.keys()))
    print("Formatted data:")
    print(json.dumps(formatted, indent=2, ensure_ascii=False))
    
    print("\n[TEMPLATE COMPATIBILITY CHECK]")
    print(f"nik: '{formatted.get('nik', '')}'")
    print(f"nama: '{formatted.get('nama', '')}'")
    print(f"tempat_lahir: '{formatted.get('tempat_lahir', '')}'")
    print(f"tanggal_lahir: '{formatted.get('tanggal_lahir', '')}'")
    print(f"ttl: '{formatted.get('ttl', '')}'")
    print(f"jenis_kelamin: '{formatted.get('jenis_kelamin', '')}'")
    print(f"status_perkawinan: '{formatted.get('status_perkawinan', '')}'")
    print(f"alamat: '{formatted.get('alamat', '')}'")
