#!/usr/bin/env python
"""Run process_ktp_image on a given KTP file and print the result and any error."""
import os
import sys
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
sys.path.insert(0, r'c:\laragon\www\ak1')

import django
django.setup()

from pencaker.ocr_utils import process_ktp_image, format_extracted_data

ktp_path = r'C:\laragon\www\ak1\ktp_test.jpg'
print('Running KTP pipeline on:', ktp_path)

# Try to run full pipeline (may call Gemini and hit quota errors)
data, error = process_ktp_image(ktp_path)

print('\n=== PIPELINE RESULT ===')
print('Error:', error)
print('Data keys:', list(data.keys()) if isinstance(data, dict) else data)
print(json.dumps(data, indent=2, ensure_ascii=False))

# If pipeline failed due to Gemini, simulate using provided 'real inside' content
if error:
    print('\nPipeline returned error; constructing simulated extraction from provided values...')
    simulated = {
        'nik': '3579010502850003',
        'nama': 'Muhammad Anwar',
        'tempat_lahir': '',
        'tanggal_lahir': '05/02/1985',
        'jenis_kelamin': 'LAKI-LAKI',
        'status_perkawinan': 'KAWIN',
        'alamat': 'JL. HASANUDIN GG.VII NO.28 RT/RW 003/009 PESANGGRAHAN BATU',
        'agama': '',
        'pekerjaan': '',
        'kewarganegaraan': 'WNI'
    }
    formatted = format_extracted_data(simulated)
    print('\n=== SIMULATED FORMATTED DATA ===')
    print(json.dumps(formatted, indent=2, ensure_ascii=False))
    sys.exit(0)

print('\nPipeline succeeded; no fallback needed.')
