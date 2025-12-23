# AK1 Pencaker OCR Integration

## Ringkasan

Fitur OCR telah diintegrasikan ke dalam aplikasi AK1 untuk memungkinkan **auto-fill form pendaftaran dari KTP** menggunakan:

1. **Tesseract OCR** - Untuk ekstraksi teks dari gambar KTP
2. **Google Gemini AI** - Untuk analisis dan validasi data dari teks OCR

## Fitur Utama

### 1. Upload KTP dengan Preview
- User dapat upload foto KTP (JPG, PNG)
- Sistem menampilkan preview foto sebelum diproses
- Ukuran file maks 5MB

### 2. Automatic Data Extraction
- Tesseract OCR mengekstrak teks dari KTP
- Gemini AI menganalisis teks dan mengekstrak field:
  - **NIK** - 16 digit Nomor Induk Kependudukan
  - **Nama** - Nama lengkap
  - **Tempat Lahir** - Tempat kelahiran
  - **Tanggal Lahir** - Format DD-MM-YYYY
  - **Jenis Kelamin** - LAKI-LAKI / PEREMPUAN
  - **Status Perkawinan** - Belum Kawin / Kawin / Cerai Hidup / Cerai Mati
  - **Alamat** - Alamat lengkap dari KTP
  - **Agama** - Agama (opsional)
  - **Pekerjaan** - Pekerjaan (opsional)
  - **Kewarganegaraan** - WNI atau negara lain

### 3. Data Review & Verification
- User dapat review data yang diekstrak
- User dapat edit field jika ada yang salah
- Preview foto KTP di-display untuk verifikasi

### 4. Auto-fill Form Pendaftaran
- Data dari KTP otomatis mengisi form pendaftaran
- Field dari KTP di-set sebagai read-only
- User dapat menambahkan data tambahan (keahlian, pengalaman, dll)
- User dapat upload dokumen pendukung (ijazah, foto profil, dll)

## Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Requirements yang ditambahkan:
- `google-generativeai>=0.3.0` - Untuk Gemini AI API

### 2. Install Tesseract OCR

**Windows:**
- Download installer dari: https://github.com/UB-Mannheim/tesseract/wiki
- Install ke lokasi default (C:\Program Files\Tesseract-OCR)
- Atau gunakan Laragon build-in (jika tersedia)

Sistem akan auto-detect path Tesseract di lokasi umum:
- `C:\Program Files\Tesseract-OCR\tesseract.exe`
- `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`
- `C:\laragon\bin\tesseract\tesseract.exe`

### 3. Setup Gemini API Key

1. Buka Google AI Studio: https://aistudio.google.com/
2. Klik "Get API Key"
3. Pilih atau buat project baru
4. Copy API key

Kemudian set di `ak1/settings.py`:

```python
GEMINI_API_KEY = 'AIzaSy...'  # Your API key here
```

Atau gunakan environment variable:

```bash
set GEMINI_API_KEY=AIzaSy...
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

## URL Routes

Semua pencaker routes dimulai dengan `/pencaker/`:

| Route | URL | Deskripsi |
|-------|-----|-----------|
| Dashboard | `/pencaker/dashboard/` | Dashboard pencaker |
| Upload KTP | `/pencaker/upload-ktp/` | Upload KTP form |
| Review KTP | `/pencaker/review-ktp/` | Review extracted data |
| Isi Data Diri | `/pencaker/isi-data-diri/` | Form pengisian data lengkap |
| Test OCR | `/pencaker/test-ocr/` | Debug page (development only) |
| Preview KTP AJAX | `/pencaker/api/preview-ktp/` | AJAX preview image |
| Extract KTP AJAX | `/pencaker/api/extract-ktp/` | AJAX extract data |

## File Structure

```
pencaker/
├── __init__.py
├── ocr_utils.py          # OCR & Gemini AI utilities
├── forms.py              # Django forms
├── views.py              # View functions
├── urls.py               # URL routing
├── templates/
│   └── pencaker/
│       ├── dashboard.html           # Dashboard
│       ├── upload_ktp.html          # Upload form
│       ├── review_ktp.html          # Review page
│       ├── isi_data_diri.html       # Data entry form
│       └── test_ocr.html            # Debug page
└── migrations/
    └── __init__.py
```

## Workflow

1. **User Upload KTP**
   ```
   /pencaker/upload-ktp/ → POST dengan file KTP
   ```

2. **System Process**
   - Tesseract OCR membaca teks dari KTP
   - Gemini AI menganalisis dan mengekstrak field
   - Data disimpan di session

3. **User Review**
   ```
   /pencaker/review-ktp/ → GET/POST
   ```
   - Display data yang diekstrak
   - User dapat edit
   - POST menyimpan ke database

4. **User Complete Profile**
   ```
   /pencaker/isi-data-diri/ → GET/POST
   ```
   - Form pre-filled dengan data dari KTP
   - User tambahkan keahlian, pengalaman, dll
   - Upload dokumen pendukung

5. **Complete**
   - Data disimpan di `PendaftaranAK1` model
   - Redirect ke dashboard

## Gemini AI Models

Sistem menggunakan Gemini API dengan fallback ke model alternatif jika satu gagal:

**Primary (Priority Order):**
1. `gemini-2.5-pro` - State-of-the-art, paling canggih
2. `gemini-2.5-flash` - Fast and intelligent, best price-performance
3. `gemini-2.5-flash-lite` - Ultra fast, cost-efficient

**Fallback:**
- `gemini-2.0-flash`
- `gemini-1.5-flash`
- `gemini-1.5-pro`
- `gemini-pro`

## Image Preprocessing

Sistem melakukan preprocessing multi-variant untuk OCR optimal:

1. **Grayscale Resizing** - Convert ke grayscale dan resize
2. **Contrast Enhancement** - CLAHE untuk meningkatkan kontras
3. **Binarization** - Convert ke binary image dengan Otsu's method
4. **Deskewing** - Koreksi sudut kemiringan
5. **Sharpening** - Sharpening filter untuk detail

Semua variant di-OCR secara parallel dan hasil terbaik dipilih berdasarkan confidence score.

## Development

### Test OCR Debug Page

Untuk development, tersedia debug page di:
```
/pencaker/test-ocr/
```

Page ini menampilkan:
- Raw OCR text
- Metadata dari OCR (confidence, variants, dll)
- Extracted data dari Gemini AI (JSON)
- Error messages

Hanya tersedia ketika `DEBUG=True` di settings.

### Logging

Sistem menggunakan print statements untuk logging. Lihat console output untuk debug info:

```
[OCR] Memproses gambar KTP dengan Tesseract...
[OCR] ✅ Berhasil OCR (1234 karakter)
[Gemini] Mencoba model: gemini-2.5-pro
[Gemini] ✅ Model gemini-2.5-pro berhasil!
```

## Troubleshooting

### Error: "tesseract is not installed"

**Solusi:**
1. Install Tesseract dari: https://github.com/UB-Mannheim/tesseract/wiki
2. Pastikan path installed Tesseract di lokasi default
3. Atau set manual di `settings.py`:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\path\to\tesseract.exe'
   ```

### Error: "GEMINI_API_KEY tidak dikonfigurasi"

**Solusi:**
1. Set GEMINI_API_KEY di `ak1/settings.py`
2. Pastikan API key valid dari Google AI Studio

### Error: "Semua model Gemini tidak tersedia"

**Solusi:**
1. Check internet connection
2. Verify API key masih valid
3. Check billing/quota di Google Cloud Console
4. Try dengan model lain di konfigurasi

### KTP Text Not Extracted (Empty)

**Solusi:**
1. Pastikan KTP foto berkualitas tinggi
2. Lighting cukup terang
3. Foto tidak blur atau miring
4. Resolution minimal 800x600 pixels
5. Try dengan foto dari sudut berbeda

## Performance

- **OCR Processing**: ~2-5 detik (tergantung ukuran gambar)
- **Gemini Analysis**: ~1-3 detik (tergantung API response time)
- **Total**: ~5-10 detik per KTP

Untuk multiple OCR processing, sistem menggunakan ThreadPoolExecutor untuk parallel processing variant preprocessing.

## Security

- API key disimpan di `settings.py` (pastikan di-gitignore)
- File upload di-validate (format, size)
- Base64 encoding untuk image storage
- CSRF protection di semua forms
- Login required untuk semua pencaker views

## Future Improvements

- [ ] Support untuk KTP berbagai region/format
- [ ] Multiple language support
- [ ] Batch processing untuk multiple users
- [ ] Real-time preview dengan cropping
- [ ] Document quality score sebelum processing
- [ ] Caching untuk model Gemini
- [ ] Export to PDF dari data pendaftaran

## Contact & Support

Untuk pertanyaan atau bug report, silakan hubungi tim development.
