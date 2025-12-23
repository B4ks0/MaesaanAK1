#!/usr/bin/env python
import os, sys, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ak1.settings')
sys.path.insert(0, r'c:\laragon\www\ak1')
import django
django.setup()
from pencaker.ocr_utils import preprocess_and_ocr, _local_parse_ocr_text, format_extracted_data
from PIL import Image

ktp_path = r'C:\laragon\www\ak1\ktp_test.jpg'
print('Opening image:', ktp_path)
img = Image.open(ktp_path)
ocr_text, meta = preprocess_and_ocr(img, lang='ind+eng')
print('\n--- OCR TEXT (first 800 chars) ---')
print(ocr_text[:800])
print('--- END OCR PREVIEW ---')
parsed = _local_parse_ocr_text(ocr_text)
print('\n--- LOCAL PARSER OUTPUT ---')
print(json.dumps(parsed, indent=2, ensure_ascii=False))
print('\n--- FORMATTED ---')
print(json.dumps(format_extracted_data(parsed), indent=2, ensure_ascii=False))
