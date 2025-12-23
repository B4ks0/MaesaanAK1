#!/usr/bin/env python
"""
Debug script to inspect what process_ktp_image returns
Uses a mock Gemini response to avoid quota issues
"""

import os
import sys
import django
import json
from unittest.mock import patch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
sys.path.insert(0, r'c:\laragon\www\ak1')

django.setup()

from pencaker.ocr_utils import format_extracted_data

# Simulate what Gemini should return
mock_gemini_response = {
    "nik": "3520451234567890",
    "nama": "JOHN DOE",
    "tempat_lahir": "Jakarta",
    "tanggal_lahir": "15-05-1990",
    "jenis_kelamin": "LAKI-LAKI",
    "status_perkawinan": "KAWIN",
    "alamat": "JL MERDEKA NO 123 JAKARTA 12345",
    "agama": "Islam",
    "pekerjaan": "Pegawai Negeri Sipil",
    "kewarganegaraan": "WNI"
}

print("=" * 70)
print("MOCK GEMINI RESPONSE (what should be returned)")
print("=" * 70)
print(json.dumps(mock_gemini_response, indent=2, ensure_ascii=False))

print("\n" + "=" * 70)
print("AFTER format_extracted_data()")
print("=" * 70)

formatted = format_extracted_data(mock_gemini_response)
print(json.dumps(formatted, indent=2, ensure_ascii=False))

print("\n" + "=" * 70)
print("TEMPLATE FIELD CHECKS")
print("=" * 70)

print(f"\n✓ NIK field: '{formatted.get('nik', '')}'")
print(f"  → Will populate: <input name='nik' value='...'>")

print(f"\n✓ Nama field: '{formatted.get('nama', '')}'")
print(f"  → Will populate: <input name='nama' value='...'>")

print(f"\n✓ TTL field: '{formatted.get('ttl', '')}'")
print(f"  → Will populate: <input name='ttl' value='...'>")

jk = formatted.get('jenis_kelamin', '')
print(f"\n✓ Jenis Kelamin field: '{jk}'")
print(f"  → Will select: LAKI-LAKI" if jk == 'LAKI-LAKI' else f"  → Will select: PEREMPUAN" if jk == 'PEREMPUAN' else f"  → ⚠️ NO MATCH - might not select anything!")

status = formatted.get('status_perkawinan', '')
valid_statuses = ['BELUM KAWIN', 'KAWIN', 'CERAI HIDUP', 'CERAI MATI']
status_display = status if status in valid_statuses else f"❌ '{status}' (not in valid options)"
print(f"\n✓ Status Perkawinan field: '{status_display}'")
print(f"  → Valid options: {', '.join(valid_statuses)}")

print(f"\n✓ Alamat field: '{formatted.get('alamat', '')}'")
print(f"  → Will populate: <textarea name='alamat'>...</textarea>")

print("\n" + "=" * 70)
print("KEY ISSUES TO CHECK")
print("=" * 70)

issues = []

if not formatted.get('ttl'):
    issues.append("⚠️  TTL field is EMPTY - won't populate TTL input")

if not formatted.get('jenis_kelamin'):
    issues.append("⚠️  Jenis Kelamin field is EMPTY - dropdown won't select")
elif formatted.get('jenis_kelamin') not in ['LAKI-LAKI', 'PEREMPUAN']:
    issues.append(f"⚠️  Jenis Kelamin has unexpected value: '{formatted.get('jenis_kelamin')}' - dropdown won't select")

if not formatted.get('status_perkawinan'):
    issues.append("⚠️  Status Perkawinan field is EMPTY - dropdown won't select")
elif formatted.get('status_perkawinan') not in ['BELUM KAWIN', 'KAWIN', 'CERAI HIDUP', 'CERAI MATI']:
    issues.append(f"⚠️  Status Perkawinan has unexpected value: '{formatted.get('status_perkawinan')}' - dropdown won't select")

if not formatted.get('alamat'):
    issues.append("⚠️  Alamat field is EMPTY - won't populate alamat textarea")

if not issues:
    print("✅ No issues found - all fields should auto-fill correctly!")
else:
    print("Found issues:")
    for issue in issues:
        print(f"  {issue}")
