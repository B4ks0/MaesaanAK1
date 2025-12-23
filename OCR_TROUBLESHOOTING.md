# OCR Quick Troubleshooting Guide

## If OCR is Still Not Working

### Step 1: Check Tesseract Status
```bash
python test_ocr_diagnostic.py
```

**Expected output:**
```
Languages: ['eng', 'ind', 'osd']
```

If Indonesian ('ind') is NOT in the list:
- Go to `c:\laragon\www\ak1\tessdata\`
- Verify `ind.traineddata` file exists (should be ~8 MB)
- If missing, download it again from GitHub tesseract-ocr repository

### Step 2: Check Gemini API Key
```python
python manage.py shell
from django.conf import settings
print(settings.GEMINI_API_KEY)
```

If empty or "None":
- Edit `ak1/settings.py`
- Find `GEMINI_API_KEY` setting
- Verify it has a valid Google Gemini API key
- Key should start with "AIza..."

### Step 3: Check Django Server Logs
When you upload a KTP, watch the console where Django is running. Look for:
- `[OCR]` messages - show OCR progress
- `[Gemini]` messages - show AI analysis progress
- `[Error]` messages - show what failed

Example good log:
```
[OCR] Using language: ind+eng, available: ['eng', 'ind', 'osd']
[OCR] Extracted 250 characters
[Gemini] Using model: gemini-2.5-flash
[Gemini] JSON parsed successfully: ['nik', 'nama', 'tempat_lahir', ...]
[Success] Extracted KTP data successfully
```

Example bad log:
```
[Error] Tesseract tidak tersedia: ...
```

### Step 4: Test OCR with Debug Page
- Go to: `http://localhost:8000/pencaker/test-ocr/`
- Upload an image
- This page shows detailed OCR output, not auto-fill
- Useful for diagnosing OCR quality

---

## Common Issues & Fixes

### Issue: "Tesseract tidak tersedia"
**Cause:** Tesseract executable not found

**Fix:**
1. Verify Tesseract is installed:
   ```bash
   dir "C:\Program Files\Tesseract-OCR\"
   ```
2. If not installed, download from: https://github.com/UB-Mannheim/tesseract/wiki
3. After install, verify `ak1/settings.py` has correct path

### Issue: Indonesian language not found
**Cause:** `ind.traineddata` missing

**Fix:**
1. Check if file exists:
   ```bash
   dir c:\laragon\www\ak1\tessdata\ind.traineddata
   ```
2. If missing, download from GitHub (see below)
3. Restart Django server

**Download Indonesian language pack manually:**
- URL: https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/ind.traineddata
- Save to: `c:\laragon\www\ak1\tessdata\ind.traineddata`
- File size should be ~7-8 MB

### Issue: Gemini API fails
**Cause:** API key invalid or rate-limited

**Fix:**
1. Verify API key in `ak1/settings.py`
2. Check Google Gemini console for rate limits
3. Try alternative model - system automatically falls back to other models
4. Wait a few minutes and retry

### Issue: Form auto-fills with error text
**Cause:** Old code still running or cache issue

**Fix:**
1. Clear browser cache: `Ctrl+Shift+Delete`
2. Stop Django server: `Ctrl+C`
3. Restart: `python manage.py runserver`
4. Try again

### Issue: 404 on login redirect
**Cause:** OLD - `LOGIN_URL` not set correctly

**Status:** ✅ FIXED in `ak1/settings.py` with `LOGIN_URL = 'login'`

---

## Performance Tips

### OCR is slow:
- Large images take longer
- System processes multiple OCR variants in parallel
- First run may be slower due to model loading
- Acceptable: 5-10 seconds per image

### Gemini is slow:
- Network latency to Google servers
- Large OCR text takes longer to analyze
- Acceptable: 2-5 seconds per request

### Tips to speed up:
1. Use clear, well-lit KTP photos
2. Crop image to just the KTP (remove background)
3. Ensure KTP fills most of the frame
4. Avoid shadows and glare

---

## Testing with Sample Data

### Create a test KTP JSON
```python
# In Django shell:
python manage.py shell

from pencaker.ocr_utils import analyze_ktp_with_gemini

# Simulate OCR text (fake but formatted like real OCR output)
ocr_text = """
NO. INDUK KEPENDUDUKAN
3520451234567890
NAMA
JOHN DOE
TEMPAT/TGL LAHIR
JAKARTA 15/05/1995
JENIS KELAMIN
LAKI-LAKI
ALAMAT
JL MERDEKA NO 123 JAKARTA 12345
"""

# Test Gemini analysis
data, error = analyze_ktp_with_gemini(ocr_text)
if error:
    print(f"Error: {error}")
else:
    print(f"Success: {data}")
```

---

## Production Checklist

Before going live:
- [ ] Move GEMINI_API_KEY to environment variable (not hardcoded)
- [ ] Set `DEBUG = False` in Django settings
- [ ] Add image size validation (max 5MB)
- [ ] Test with 50+ real KTP images
- [ ] Monitor error logs for patterns
- [ ] Setup email alerts for failures
- [ ] Document user-facing error messages

---

## Getting Help

If you still have issues:
1. Check the server console for error messages
2. Run `test_ocr_diagnostic.py` to diagnose environment
3. Check `/pencaker/test-ocr/` page for detailed OCR debugging
4. Review Django `manage.py shell` to test functions individually
5. Check internet connection (Gemini API needs it)
6. Verify Tesseract installation and language packs

---

**Last Updated:** December 9, 2025
