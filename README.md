# MaesaanAK1 - Sistem Pelayanan Disnaker & Absensi Digital

**MaesaanAK1** adalah aplikasi berbasis web yang dikembangkan untuk memodernisasi pelayanan di **Dinas Tenaga Kerja (Disnaker)**, khususnya dalam pembuatan Kartu Pencari Kerja (AK/1) dan pengelolaan Buku Tamu Digital.

Aplikasi ini mengintegrasikan **Artificial Intelligence (AI)** dan **Optical Character Recognition (OCR)** untuk mempercepat proses input data masyarakat. Cukup dengan mengunggah foto KTP, formulir akan terisi secara otomatis.

## 🌟 Fitur Unggulan Web

### 1. Pelayanan Kartu Kuning (AK/1) Online
- **Smart Form AK/1**: Pengisian data diri pencari kerja otomatis dari foto KTP.
- **Validasi AI**: Menggunakan Google Gemini untuk memastikan akurasi data hasil scan.
- **Upload Berkas**: Manajemen upload pas foto, ijazah, dan sertifikat dalam satu portal.

### 2. Buku Tamu Digital (Smart Attendance)
- **Scan & Log**: Tamu kantor cukup scan KTP atau isi form singkat.
- **Real-time Dashboard**: Pantau jumlah kunjungan harian secara real-time.

### 3. Teknologi Canggih
- **Backend**: Django (Python) yang aman dan scalable.
- **Vision AI**: Tesseract OCR engine + Gemini Generative AI.
- **Dukungan Database**: MySQL untuk penyimpanan data skala besar.

## 📋 Fitur Utama System
- **Auto-Fill Data KTP**: Upload foto KTP, sistem otomatis mengisi form (NIK, Nama, TTL, Alamat, dll).
- **AI-Powered Validation**: Menggunakan Google Gemini AI untuk memperbaiki hasil OCR yang kurang akurat.
- **Manajemen Absensi**: Pencatatan tamu/absensi dengan validasi identitas.
- **Laporan & Ekspor**: Generate laporan PDF dan Excel.

## 🛠️ Prasyarat System (Prerequisites)
Pastikan komputer Anda sudah terinstall:
1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **MySQL Server** (bisa via Laragon/XAMPP): Pastikan service MySQL berjalan.
3.  **Git**: [Download Git](https://git-scm.com/downloads)
4.  **Tesseract OCR Engine**:
    - **Windows**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
    - Install ke path default (`C:\Program Files\Tesseract-OCR`) atau pastikan masuk ke Environment Variable `PATH`.

## 🚀 Panduan Instalasi (Installation)

### 1. Clone Repository
```bash
git clone https://github.com/B4ks0/MaesaanAK1.git
cd MaesaanAK1
```

### 2. Setup Virtual Environment (Recommended)
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate
# Windows (CMD):
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database MySQL
Buat database baru dengan nama `absen_db` (atau sesuai konfigurasi di `settings.py`).
```sql
CREATE DATABASE absen_db;
```
*Catatan: Pastikan user/password database di `ak1/settings.py` sesuai dengan local server Anda (default: user `root`, password kosong).*

### 5. Konfigurasi API Key (Gemini AI)
Untuk fitur koreksi AI yang lebih akurat, Anda memerlukan API Key dari Google Gemini.
1.  Dapatkan Key di [Google AI Studio](https://aistudio.google.com/).
2.  Set environment variable atau edit `ak1/settings.py`:
    ```python
    # di file ak1/settings.py
    GEMINI_API_KEY = "MASUKKAN_API_KEY_ANDA_DISINI"
    ```
    *Atau menggunakan Environment Variable (Lebih Aman):*
    ```powershell
    $env:GEMINI_API_KEY="AIzaSy..."
    ```

### 6. Setup Database Schema
Jalankan migrasi untuk membuat tabel-tabel database.
```bash
python manage.py migrate
```

### 7. Buat Admin User
Untuk mengakses halaman admin Django.
```bash
python manage.py createsuperuser
```

---

## ▶️ Menjalankan Aplikasi
Setelah instalasi selesai, jalankan server development:
```bash
python manage.py runserver
```
Akses aplikasi melalui browser:
- **Halaman Utama**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Test OCR**: [http://127.0.0.1:8000/pencaker/test-ocr/](http://127.0.0.1:8000/pencaker/test-ocr/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔧 Troubleshooting

### Masalah: "tesseract is not installed" atau error path
*   Pastikan Tesseract OCR sudah terinstall.
*   Jika di Windows, cek path di `ak1/settings.py` atau `ocr_utils.py` jika perlu diarahkan manual:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ```

### Masalah: Database Error
*   Pastikan service MySQL (Laragon/XAMPP) sudah start.
*   Pastikan nama database `absen_db` sudah dibuat.

### Masalah: API Key Error
*   Jika OCR berjalan tapi hasil berantakan atau AI error, pastikan `GEMINI_API_KEY` valid dan memiliki kuota.

---

## 📂 Struktur Project
- `ak1/`: Project settings utama.
- `pencaker/`: Aplikasi utama manajemen pencari kerja & OCR.
- `ocr/`: Modul/utilities tambahan untuk OCR.
- `templates/`: File HTML frontend.
- `static/`: File CSS, JS, dan gambar.

---
**MaesaanAK1 Team © 2025**
