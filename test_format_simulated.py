#!/usr/bin/env python
import os, sys, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ak1.settings')
sys.path.insert(0, r'c:\laragon\www\ak1')
import django
django.setup()
from pencaker.ocr_utils import format_extracted_data

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

fmt = format_extracted_data(simulated)
print(json.dumps(fmt, indent=2, ensure_ascii=False))
