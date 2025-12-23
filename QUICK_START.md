# 🚀 Quick Start Guide - AK1 OCR Integration

**Time Required:** ~15 minutes to setup

## Step 1: Install Dependencies (1 min)

```bash
cd c:\laragon\www\ak1
pip install -r requirements.txt
```

**What's installed:**
- google-generativeai (new)
- Django, Pillow, OpenCV, Tesseract, Requests (already in requirements)

## Step 2: Install Tesseract OCR (5 min)

### Option A: Automatic (Windows)
```bash
# Download installer
# https://github.com/UB-Mannheim/tesseract/wiki

# Run installer, choose default installation path
# C:\Program Files\Tesseract-OCR

# System will auto-detect
```

### Option B: Using Laragon
```bash
# Check if Tesseract is already in Laragon bin folder
# If exists, system will auto-detect
```

### Verify Installation
```bash
tesseract --version
```

## Step 3: Get Gemini API Key (2 min)

1. Open: https://aistudio.google.com/
2. Click "Get API Key" button
3. Select or create a Google Cloud project
4. Copy your API key (starts with `AIzaSy...`)

## Step 4: Configure API Key (1 min)

**Option A: Direct Configuration (Development)**

Edit `ak1/settings.py`:
```python
GEMINI_API_KEY = 'AIzaSy...'  # Paste your API key here
```

**Option B: Environment Variable (Production)**

```bash
# PowerShell
$env:GEMINI_API_KEY="AIzaSy..."

# CMD
set GEMINI_API_KEY=AIzaSy...
```

Then in `ak1/settings.py`:
```python
import os
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
```

## Step 5: Run Migrations (2 min)

```bash
python manage.py migrate
```

## Step 6: Create Admin User (1 min)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## Step 7: Start Server (0.5 min)

```bash
python manage.py runserver
```

Server will start at `http://localhost:8000/`

## Step 8: Test the System (3 min)

### Access the Application

1. **Admin Panel:** http://localhost:8000/admin/
2. **Pencaker App:** http://localhost:8000/pencaker/dashboard/
3. **Debug Page:** http://localhost:8000/pencaker/test-ocr/

### Test Upload KTP

1. Go to: `/pencaker/upload-ktp/`
2. Upload a KTP image (JPG or PNG)
3. Click "Upload & Proses KTP"
4. System will extract data and show review page
5. Verify extracted data and edit if needed
6. Click "Simpan & Lanjutkan"
7. Complete your profile with additional info
8. Click "Simpan Data Diri"

### Check Debug Page

1. Go to: `/pencaker/test-ocr/`
2. Upload a KTP image
3. View raw OCR text and extracted data
4. Use for troubleshooting

## 📝 Main URL Routes

```
/pencaker/dashboard/         - Your profile dashboard
/pencaker/upload-ktp/        - Upload KTP
/pencaker/review-ktp/        - Review extracted data
/pencaker/isi-data-diri/     - Complete your profile
/pencaker/test-ocr/          - Debug page for testing
/admin/                      - Admin panel
```

## ✅ Verification Checklist

After setup, verify:

- [ ] Server runs without errors: `python manage.py runserver`
- [ ] Can access admin: `http://localhost:8000/admin/`
- [ ] Can access pencaker dashboard: `http://localhost:8000/pencaker/dashboard/`
- [ ] Debug page loads: `http://localhost:8000/pencaker/test-ocr/`
- [ ] Can upload KTP and extract data
- [ ] Extracted data displays correctly
- [ ] Can save and review data

## 🆘 Troubleshooting Quick Fix

### Issue: "tesseract is not installed"
```bash
# Windows - Download and install from:
# https://github.com/UB-Mannheim/tesseract/wiki

# Then verify:
tesseract --version
```

### Issue: "GEMINI_API_KEY tidak dikonfigurasi"
```python
# In ak1/settings.py, make sure you have:
GEMINI_API_KEY = 'AIzaSy...'  # Your actual key

# Don't forget to restart server after changes
```

### Issue: "Can't find localhost:8000"
```bash
# Make sure you ran:
python manage.py runserver

# Server should say:
# Starting development server at http://127.0.0.1:8000/
```

### Issue: Database error
```bash
# Run migrations again:
python manage.py migrate

# Then restart server
```

## 📁 Project Structure Quick Reference

```
c:\laragon\www\ak1\
├── pencaker/                    ← NEW OCR APP
│   ├── views.py                 ← Main logic
│   ├── ocr_utils.py             ← OCR processing
│   ├── forms.py                 ← Data forms
│   ├── urls.py                  ← Routes
│   └── templates/pencaker/      ← HTML templates
│
├── ak1/
│   ├── settings.py              ← ⚙️ Config (updated)
│   └── urls.py                  ← ⚙️ Routes (updated)
│
├── requirements.txt             ← ⚙️ Dependencies (updated)
├── OCR_INTEGRATION_SUMMARY.md   ← 📖 Full docs
└── manage.py                    ← Run commands
```

## 🎯 Next Steps

1. **Get familiar with the UI**
   - Upload test KTP
   - Review extracted data
   - Complete profile

2. **Understand the flow**
   - Read: `pencaker/README.md`
   - Understand: `pencaker/INTEGRATION_GUIDE.md`

3. **Customize if needed**
   - Modify templates (HTML)
   - Adjust forms (fields)
   - Configure settings

4. **Deploy to production**
   - Set DEBUG = False
   - Use environment variables for secrets
   - Configure HTTPS
   - Setup database

## 📖 Documentation

- **Quick Start:** This file
- **Full Documentation:** `pencaker/README.md`
- **Integration Details:** `pencaker/INTEGRATION_GUIDE.md`
- **Project Summary:** `OCR_INTEGRATION_SUMMARY.md`
- **Checklist:** `OCR_INTEGRATION_CHECKLIST.md`

## 🎓 Learning Resources

### How to Use OCR Feature

1. **Upload Page:** `/pencaker/upload-ktp/`
   - Select KTP image
   - Preview before uploading
   - Submit for processing

2. **Review Page:** `/pencaker/review-ktp/`
   - Check extracted data
   - Edit any incorrect fields
   - Save to database

3. **Profile Page:** `/pencaker/isi-data-diri/`
   - Data from KTP is pre-filled
   - Add optional information
   - Upload supporting documents

### How to Debug

Visit `/pencaker/test-ocr/`:
- Upload test KTP
- See raw OCR text output
- See extracted data in JSON
- Check error messages
- View metadata and confidence scores

### How to Check Data

Admin panel `/admin/`:
- View all registered users
- Search by NIK or name
- Filter by status
- Edit user data

## 🚀 You're Ready!

The OCR integration is complete and ready to use. Follow the steps above and you'll have a working KTP auto-fill system in 15 minutes.

**Questions?** Check the documentation files or visit the debug page to test.

---

**Good luck! 🎉**

For more details, see the full documentation:
- `pencaker/README.md`
- `pencaker/INTEGRATION_GUIDE.md`
- `OCR_INTEGRATION_SUMMARY.md`
