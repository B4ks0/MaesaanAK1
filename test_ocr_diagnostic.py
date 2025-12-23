#!/usr/bin/env python
"""
Diagnostic script to test OCR pipeline without Django
Run: python test_ocr_diagnostic.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from pencaker.ocr_utils import (
    _check_tesseract_available,
    preprocess_and_ocr,
    analyze_ktp_with_gemini,
    process_ktp_image
)
from PIL import Image
import json

print("=" * 60)
print("OCR DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Check Tesseract
print("\n[TEST 1] Checking Tesseract availability...")
ok, ver_or_err, langs = _check_tesseract_available()
print(f"  Available: {ok}")
print(f"  Version/Error: {ver_or_err}")
print(f"  Languages: {langs}")

if not ok:
    print("  ❌ Tesseract not available! Install Tesseract-OCR first.")
    sys.exit(1)

# Test 2: Look for test KTP image
print("\n[TEST 2] Looking for test KTP image...")
test_images = [
    'test_ktp.png',
    'test_ktp.jpg',
    'test_ktp_extraction.py',  # This is the file, not an image
]

found_image = None
for fname in test_images:
    if os.path.exists(fname):
        if fname.endswith(('.png', '.jpg', '.jpeg')):
            found_image = fname
            print(f"  Found: {fname}")
            break

if not found_image:
    print("  ⚠️ No test KTP image found. Create a test image named 'test_ktp.png' or 'test_ktp.jpg'")
    print("  Proceeding without image test...")
else:
    # Test 3: Load and process image
    print(f"\n[TEST 3] Processing KTP image: {found_image}")
    try:
        with open(found_image, 'rb') as f:
            extracted_data, error = process_ktp_image(f)
        
        if error:
            print(f"  ❌ Error: {error}")
        else:
            print(f"  ✅ Success! Extracted data:")
            print(json.dumps(extracted_data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")

print("\n" + "=" * 60)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 60)
