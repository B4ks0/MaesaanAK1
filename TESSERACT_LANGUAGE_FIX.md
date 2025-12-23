# OCR Tesseract Language Pack Issue

## Current Status
✅ Tesseract 5.5.0.20241111 is installed
❌ Indonesian language pack (`ind`) is NOT installed
📦 Only available languages: `eng`, `osd`

## Problem
The Indonesian KTP OCR is failing because Tesseract doesn't have the Indonesian language data.

## Solution

### Option 1: Download Indonesian Language Pack (Recommended)
Tesseract language data files are stored in the `tessdata` folder. 

For your Tesseract installation, find the folder:
- If Tesseract is in `C:\Program Files\Tesseract-OCR`, look for `C:\Program Files\Tesseract-OCR\tessdata\`
- If Tesseract is in Laragon, look for the tessdata folder in the Laragon bin directory

Then download the Indonesian language file:
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download `ind.traineddata` from the v5.x releases
3. Place it in the tessdata folder

Or download directly:
```
https://github.com/UB-Mannheim/tesseract/raw/main/tessdata/ind.traineddata
```

After adding the file, restart the Django server.

### Option 2: Install Full Tesseract Package
If you have Visual C++ Build Tools installed, you can rebuild with all languages using:
```
pip install pytesseract --upgrade
```

But this typically doesn't install language data automatically.

### Option 3: Use English Only (Temporary)
The system is already configured to fall back to English if Indonesian is not available.
However, OCR accuracy will be lower on Indonesian KTPs with English-only training data.

## Verify Installation
After adding the Indonesian language pack, run:
```
tesseract --list-langs
```

You should see `ind` in the list.

Then test the OCR again:
```
python test_ocr_diagnostic.py
```
