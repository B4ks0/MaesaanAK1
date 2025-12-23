def analyze_ktp_with_gemini(ocr_text: str) -> Tuple[dict, str]:
    """
    Analyze KTP OCR text using Gemini AI to extract structured data.
    Returns: (data_dict, error_message)
    On error, returns ({}, "error description")
    On success, returns (data_dict, "")
    
    Enhanced version that ensures ALL 10 fields are returned and logged.
    """
    if not ocr_text or not ocr_text.strip():
        return {}, "OCR text kosong - tidak ada data untuk dianalisis"
    
    try:
        api_key = getattr(settings, 'GEMINI_API_KEY', '')
        if not api_key:
            return {}, 'GEMINI_API_KEY tidak dikonfigurasi di settings.py'
        
        genai.configure(api_key=api_key)

        models_to_try = [
            'gemini-2.5-pro',
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
        ]

        model = None
        model_name = None
        last_error = None
        for model_name_attempt in models_to_try:
            try:
                model = genai.GenerativeModel(model_name_attempt)
                model_name = model_name_attempt
                print(f"[Gemini] Using model: {model_name}")
                break
            except Exception as e:
                last_error = str(e)
                print(f"[Gemini] Model {model_name_attempt} not available: {last_error}")
                continue

        if model is None:
            return {}, f"Tidak ada model Gemini yang tersedia: {last_error}"

        # Improved prompt to extract ALL KTP fields with proper formatting
        prompt = f"""Anda adalah ahli ekstraksi data KTP Indonesia dengan AI yang canggih.

TUGAS: Ekstrak SEMUA data dari teks OCR KTP ini dan kembalikan dalam format JSON LENGKAP.

TEKS OCR dari KTP:
{ocr_text}

EKSTRAK field berikut DENGAN HATI-HATI:

1. **nik** (wajib): Nomor Identitas Kependudukan - 16 digit tanpa spasi
   Format: "3520451234567890"

2. **nama** (wajib): Nama lengkap sesuai KTP
   Format: "JOHN DOE" atau "BUDI SANTOSO"

3. **tempat_lahir** (wajib): Tempat lahir
   Format: "Jakarta" atau "Surabaya"

4. **tanggal_lahir** (wajib): Tanggal lahir
   Format: "DD-MM-YYYY" (contoh: "15-05-1990")

5. **jenis_kelamin** (wajib): Jenis kelamin
   Format: "LAKI-LAKI" atau "PEREMPUAN" (HARUS HURUF BESAR)

6. **status_perkawinan** (wajib): Status perkawinan
   Format: "Belum Kawin", "Kawin", "Cerai Hidup", atau "Cerai Mati"

7. **alamat** (wajib): Alamat lengkap
   Format: "JL MERDEKA NO 123 RT 02 RW 05 JAKARTA 12345"

8. **agama** (wajib): Agama
   Format: "Islam", "Kristen", "Katholik", "Hindu", "Buddha", "Konghucu"

9. **pekerjaan** (wajib): Pekerjaan/profesi
   Format: "Pegawai Negeri Sipil" atau "Wiraswasta"

10. **kewarganegaraan** (wajib): Kewarganegaraan
    Format: "WNI" atau nama negara

INSTRUKSI PENTING:
- Ekstrak HANYA dari teks OCR yang ada - JANGAN buat data
- SEMUA 10 field HARUS ada dalam JSON response - tidak boleh kurang
- Jika field tidak ada di teks, gunakan string kosong "" (bukan null)
- Untuk tanggal, format PERSIS DD-MM-YYYY (misal: 15-05-1990)
- Untuk jenis_kelamin, gunakan PERSIS: "LAKI-LAKI" atau "PEREMPUAN"
- Untuk status_perkawinan, gunakan salah satu: "Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"
- Tempat lahir dan tanggal lahir TERPISAH - jangan gabung!
- Alamat: gabungkan semua baris jadi satu string jelas

BALAS HANYA DENGAN JSON OBJECT - TANPA MARKDOWN - TANPA PENJELASAN:
Contoh format respons yang HARUS sama persis strukturnya:
{{
    "nik": "3520451234567890",
    "nama": "JOHN DOE",
    "tempat_lahir": "Jakarta",
    "tanggal_lahir": "15-05-1990",
    "jenis_kelamin": "LAKI-LAKI",
    "status_perkawinan": "Belum Kawin",
    "alamat": "JL MERDEKA NO 123 JAKARTA 12345",
    "agama": "Islam",
    "pekerjaan": "Pegawai Negeri Sipil",
    "kewarganegaraan": "WNI"
}}

PENTING: Jangan skip field atau tambah field lain!"""

        try:
            print(f"[Gemini] Sending KTP extraction request to model: {model_name}")
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            print(f"[Gemini] Response received ({len(response_text)} chars)")
            
            # Log raw response for debugging (first 1000 chars)
            print(f"[Gemini] Raw response preview:\n{response_text[:1000]}")
            
        except Exception as e:
            alt_err = str(e)
            print(f"[Gemini] Model {model_name} failed: {alt_err}")
            # Try alternative models
            for alt in models_to_try:
                if alt == model_name:
                    continue
                try:
                    alt_model = genai.GenerativeModel(alt)
                    response = alt_model.generate_content(prompt)
                    response_text = response.text.strip()
                    model_name = alt
                    print(f"[Gemini] Fallback to model {model_name} successful")
                    break
                except Exception as ee:
                    alt_err = str(ee)
                    print(f"[Gemini] Alt model {alt} also failed: {alt_err}")
                    continue
            else:
                return {}, f"Semua model Gemini gagal: {alt_err}"

        # Clean response (remove markdown code blocks if present)
        if response_text.startswith('```json'):
            response_text = response_text[7:].strip()
        elif response_text.startswith('```'):
            response_text = response_text[3:].strip()
        if response_text.endswith('```'):
            response_text = response_text[:-3].strip()

        # Try to parse JSON
        try:
            data = json.loads(response_text)
            print(f"[Gemini] ✓ JSON parsed successfully")
            print(f"[Gemini] Returned keys: {list(data.keys())}")
            
            # CRITICAL: Ensure ALL expected fields exist
            expected_fields = ['nik', 'nama', 'tempat_lahir', 'tanggal_lahir', 
                              'jenis_kelamin', 'status_perkawinan', 'alamat', 
                              'agama', 'pekerjaan', 'kewarganegaraan']
            
            missing_fields = [f for f in expected_fields if f not in data]
            if missing_fields:
                print(f"[Gemini] ⚠️ Missing fields from Gemini response: {missing_fields}")
                print(f"[Gemini] Adding fallback empty strings for: {missing_fields}")
                for field in missing_fields:
                    data[field] = ''
            
            # Handle None values
            for field in expected_fields:
                if field in data and data[field] is None:
                    data[field] = ''
            
            print(f"[Gemini] ✓ After validation, has all keys: {list(data.keys())}")
            
            # Validate critical fields are not empty
            critical = ['nik', 'nama', 'alamat']
            empty_critical = [f for f in critical if not data.get(f, '').strip()]
            if empty_critical:
                print(f"[Gemini] ⚠️ Critical fields are empty: {empty_critical}")
            
            return data, ''
            
        except json.JSONDecodeError as je:
            print(f"[Gemini] JSON parse error: {str(je)}")
            # Try to extract JSON from response
            s = response_text.find('{')
            e = response_text.rfind('}') + 1
            if s >= 0 and e > s:
                try:
                    json_str = response_text[s:e]
                    data = json.loads(json_str)
                    print(f"[Gemini] ✓ JSON extracted and parsed: {list(data.keys())}")
                    
                    # Apply same field validation
                    expected_fields = ['nik', 'nama', 'tempat_lahir', 'tanggal_lahir', 
                                      'jenis_kelamin', 'status_perkawinan', 'alamat', 
                                      'agama', 'pekerjaan', 'kewarganegaraan']
                    for field in expected_fields:
                        if field not in data or data[field] is None:
                            data[field] = ''
                    
                    return data, ''
                except json.JSONDecodeError as je2:
                    return {}, f"Gagal parse JSON dari Gemini: {str(je2)}"
            return {}, f"Tidak ada JSON valid dalam response Gemini"

    except Exception as e:
        error_msg = f"Error saat menggunakan Gemini AI: {str(e)}"
        print(f"[Gemini] {error_msg}")
        return {}, error_msg

