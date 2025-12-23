import cv2
import numpy as np
from PIL import Image
import pytesseract
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple, List, Dict
import google.generativeai as genai
import json
import re
import shutil
import subprocess
from django.conf import settings


def _pil_to_cv(image: Image.Image) -> np.ndarray:
    arr = np.array(image)
    if len(arr.shape) == 3 and arr.shape[2] == 3:
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    return arr


def _deskew(gray: np.ndarray) -> np.ndarray:
    coords = np.column_stack(np.where(gray > 0))
    if coords.shape[0] < 10:
        return gray
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = gray.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def _resize_for_dpi(img: np.ndarray, target_width=1600) -> np.ndarray:
    h, w = img.shape[:2]
    if w >= target_width:
        return img
    scale = target_width / float(w)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)


def _enhance_contrast(gray: np.ndarray) -> np.ndarray:
    if len(gray.shape) == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


def _binarize(gray: np.ndarray) -> np.ndarray:
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th


def _sharpen(img: np.ndarray) -> np.ndarray:
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)


def _preprocess_variants(image: Image.Image) -> List[Tuple[str, Image.Image]]:
    bgr = _pil_to_cv(image)
    variants = []

    if len(bgr.shape) == 3:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    else:
        gray = bgr.copy()

    # Resize for small images
    gray_resized = _resize_for_dpi(gray)
    variants.append(('gray_resized', Image.fromarray(gray_resized)))

    # Contrast enhanced
    enhanced = _enhance_contrast(gray_resized)
    variants.append(('enhanced_clahe', Image.fromarray(enhanced)))

    # Binarized
    bin_img = _binarize(enhanced)
    variants.append(('binarized', Image.fromarray(bin_img)))

    # Deskewed + enhanced
    try:
        deskewed = _deskew(enhanced)
        variants.append(('deskewed', Image.fromarray(deskewed)))
        variants.append(('deskewed_binarized', Image.fromarray(_binarize(deskewed))))
    except Exception:
        pass

    # Sharpened color for photos
    try:
        color_sharp = _sharpen(bgr)
        variants.append(('color_sharp', Image.fromarray(cv2.cvtColor(color_sharp, cv2.COLOR_BGR2RGB))))
    except Exception:
        pass

    variants.append(('original', image))

    # Deduplicate by name
    seen = set()
    dedup = []
    for name, img in variants:
        if name in seen:
            continue
        seen.add(name)
        dedup.append((name, img))

    return dedup


def _run_tesseract(pil_img: Image.Image, lang: str = 'ind+eng', psm: int = 6, oem: int = 1, whitelist: str = None) -> Dict:
    conf = f'--oem {oem} --psm {psm}'
    if whitelist:
        conf += f" -c tessedit_char_whitelist={whitelist}"

    try:
        data = pytesseract.image_to_data(pil_img, lang=lang, config=conf, output_type=pytesseract.Output.DICT)
    except Exception as e:
        return {'text': '', 'conf_avg': 0.0, 'raw': None, 'error': str(e)}

    texts = []
    confs = []
    n_boxes = len(data.get('text', []))
    for i in range(n_boxes):
        txt = (data['text'][i] or '').strip()
        if txt:
            try:
                conf_val = float(data['conf'][i])
            except Exception:
                conf_val = -1.0
            texts.append(txt)
            confs.append(conf_val)

    combined = '\n'.join(texts)
    avg_conf = float(sum([c for c in confs if c >= 0]) / max(1, sum(1 for c in confs if c >= 0))) if confs else 0.0
    return {'text': combined, 'conf_avg': avg_conf, 'raw': data, 'error': None}


def preprocess_and_ocr(image: Image.Image, lang: str = 'ind+eng', max_workers: int = 4, psm: int = 6, oem: int = 1) -> Tuple[str, dict]:
    variants = _preprocess_variants(image)
    max_workers = max(1, min(max_workers, len(variants)))

    results = []
    metadata = {'variants': []}

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_run_tesseract, img, lang, psm, oem): name for name, img in variants}
        for fut in as_completed(futures):
            name = futures[fut]
            try:
                res = fut.result()
            except Exception as e:
                res = {'text': '', 'conf_avg': 0.0, 'raw': None, 'error': str(e)}
            res['name'] = name
            metadata['variants'].append(res)
            results.append(res)

    # Select best variant by confidence and text length
    import math
    best = None
    best_score = -1
    for r in results:
        txt_len = len(r['text'])
        score = r.get('conf_avg', 0.0) * math.log(1 + txt_len)
        if score > best_score:
            best_score = score
            best = r

    # Merge lines from all variants preferring higher conf
    line_map = {}
    for r in sorted(results, key=lambda x: x.get('conf_avg', 0.0), reverse=True):
        for line in (r.get('text') or '').split('\n'):
            l = line.strip()
            if not l:
                continue
            prev_conf = line_map.get(l, 0.0)
            if r.get('conf_avg', 0.0) >= prev_conf:
                line_map[l] = r.get('conf_avg', 0.0)

    merged_lines = sorted(line_map.keys(), key=lambda x: (line_map.get(x, 0.0), len(x)), reverse=True)
    combined_text = '\n'.join(merged_lines)

    metadata['best_variant'] = best['name'] if best else None
    metadata['best_conf'] = best.get('conf_avg', 0.0) if best else 0.0
    metadata['variant_count'] = len(results)

    return combined_text, metadata


def _check_tesseract_available() -> Tuple[bool, str, List[str]]:
    try:
        ver = pytesseract.get_tesseract_version()
        langs = []
        try:
            langs = pytesseract.get_languages(config='')
        except Exception:
            try:
                out = subprocess.check_output(['tesseract', '--list-langs'], stderr=subprocess.STDOUT, text=True)
                langs = [l.strip() for l in out.splitlines() if l.strip()]
            except Exception:
                langs = []
        return True, str(ver), langs
    except Exception as e:
        if shutil.which('tesseract'):
            return False, 'tesseract found but pytesseract error: ' + str(e), []
        return False, str(e), []


def analyze_ktp_with_gemini(ocr_text: str) -> Tuple[dict, str]:
    """
    Analyze KTP OCR text using Gemini AI to extract structured data.
    Returns: (data_dict, error_message)
    On error, returns ({}, "error description")
    On success, returns (data_dict, "")
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


def _local_parse_ocr_text(ocr_text: str) -> dict:
    """
    Heuristic parser for OCR text as a fallback when Gemini is unavailable.
    Attempts to extract nik, nama, tempat_lahir, tanggal_lahir, jenis_kelamin,
    status_perkawinan, alamat, agama, pekerjaan, kewarganegaraan.
    Returns a dict (fields may be empty strings).
    """
    if not ocr_text:
        return {}

    text = ocr_text.replace('\r', '\n')
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    joined = ' '.join(lines)

    result = {
        'nik': '', 'nama': '', 'tempat_lahir': '', 'tanggal_lahir': '',
        'jenis_kelamin': '', 'status_perkawinan': '', 'alamat': '',
        'agama': '', 'pekerjaan': '', 'kewarganegaraan': ''
    }

    # NIK - first 16-digit group
    m = re.search(r"\b(\d{16})\b", joined)
    if m:
        result['nik'] = m.group(1)

    # Nama - look for line after a 'NAMA' header or a line containing 'NAMA'
    for i, l in enumerate(lines):
        if re.search(r"^\s*(NAMA|NAMA LENGKAP)\s*$", l, re.IGNORECASE):
            if i + 1 < len(lines):
                result['nama'] = lines[i+1]
                break
    if not result['nama']:
        # fallback: try to find a likely name by joining adjacent alphabetic lines
        alpha_lines = []
        skip_header_re = re.compile(r"(TEMPAT|TGL|LAHIR|NIK|ALAMAT|AGAMA|PEKERJAAN|STATUS|KTP|NO\.|NO:)", re.IGNORECASE)
        for l in lines:
            if skip_header_re.search(l):
                alpha_lines.append(None)
            elif re.match(r"^[A-Za-z .'\-]+$", l) and len(l) > 2:
                alpha_lines.append(l)
            else:
                alpha_lines.append(None)

        # find the longest contiguous run of alphabetic lines
        best = []
        cur = []
        for item in alpha_lines:
            if item:
                cur.append(item)
            else:
                if len(cur) > len(best):
                    best = cur
                cur = []
        if len(cur) > len(best):
            best = cur
        if best:
            # join into a single name
            candidate = ' '.join(best).strip()
            # ensure it's reasonable
            if len(candidate.split()) >= 2:
                result['nama'] = candidate
        else:
            # try combining nearby alphabetic candidates (non-contiguous)
            alpha_candidates = [(i, l) for i, l in enumerate(lines) if re.match(r"^[A-Za-z .'\-]+$", l) and len(l) > 2 and not skip_header_re.search(l)]
            best_pair = ('', -1)
            for a in range(len(alpha_candidates)):
                for b in range(a+1, min(a+4, len(alpha_candidates))):
                    i1, l1 = alpha_candidates[a]
                    i2, l2 = alpha_candidates[b]
                    if 0 < (i2 - i1) <= 3:
                        cand = (l1 + ' ' + l2).strip()
                        score = len(cand.split())
                        if score > best_pair[1]:
                            best_pair = (cand, score)
            if best_pair[1] >= 2:
                result['nama'] = best_pair[0]

    # Tempat + tanggal - look for lines containing 'TEMPAT' or 'TGL' or 'LAHIR'
    for l in lines:
        if re.search(r"(TEMPAT|TGL|LAHIR)", l, re.IGNORECASE):
            # try to find date in this line
            dm = re.search(r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})", l)
            if dm:
                date_raw = dm.group(1)
                result['tanggal_lahir'] = date_raw.replace('/', '-').strip()
            # place: words before date
            parts = re.split(r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})", l)
            if parts and parts[0].strip():
                place = re.sub(r"(TEMPAT|TGL|LAHIR|:)", "", parts[0], flags=re.IGNORECASE).strip()
                result['tempat_lahir'] = place
            break

    # If date still missing, search globally
    if not result['tanggal_lahir']:
        dm = re.search(r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})", joined)
        if dm:
            result['tanggal_lahir'] = dm.group(1).replace('/', '-')

    # Better attempt to find tempat_kota (KOTA / KABUPATEN)
    if not result['tempat_lahir']:
        m_kota = re.search(r"([A-Za-z\-]+)\s+(KOTA|KABUPATEN|KAB)\b", joined, re.IGNORECASE)
        if m_kota:
            place = m_kota.group(1).title()
            result['tempat_lahir'] = place
        else:
            # try to find common city names heuristically (e.g., MALANG, BATU)
            city_match = re.search(r"\b(MALANG|BATU|JAKARTA|SURABAYA|BANDUNG|YOGYAKARTA|SOLO|SEMARANG)\b", joined, re.IGNORECASE)
            if city_match:
                result['tempat_lahir'] = city_match.group(1).title()

    # Jenis kelamin
    if re.search(r"\b(LAKI|PRIA|L\b)", joined, re.IGNORECASE):
        result['jenis_kelamin'] = 'LAKI-LAKI'
    elif re.search(r"\b(PEREMPUAN|WANITA|P\b)", joined, re.IGNORECASE):
        result['jenis_kelamin'] = 'PEREMPUAN'

    # Status perkawinan
    if re.search(r"\b(KAWIN|MARRIED)\b", joined, re.IGNORECASE):
        result['status_perkawinan'] = 'KAWIN'
    elif re.search(r"\b(BELUM|SINGLE|TK)\b", joined, re.IGNORECASE):
        result['status_perkawinan'] = 'BELUM KAWIN'
    elif re.search(r"\b(CERAI|DIVORCED|WIDOW)\b", joined, re.IGNORECASE):
        # Distinguish CERAI HIDUP vs CERAI MATI by presence of 'mati' or 'hidup'
        if re.search(r"MATI", joined, re.IGNORECASE):
            result['status_perkawinan'] = 'CERAI MATI'
        elif re.search(r"HIDUP", joined, re.IGNORECASE):
            result['status_perkawinan'] = 'CERAI HIDUP'
        else:
            result['status_perkawinan'] = 'CERAI HIDUP'

    # Alamat - take lines after 'ALAMAT' header or fallback to cluster of lines
    alamat_lines = []
    for i, l in enumerate(lines):
        if re.search(r"^\s*ALAMAT\b", l, re.IGNORECASE):
            # collect next up to 3 lines
            for j in range(i+1, min(i+4, len(lines))):
                if re.search(r"^(NAMA|TEMPAT|TGL|JENIS|STATUS|AGAMA|PEKERJAAN)", lines[j], re.IGNORECASE):
                    break
                alamat_lines.append(lines[j])
            break
    if not alamat_lines:
        # heuristics: look for line containing RT/RW or 'JL' and take surrounding tokens
        for l in lines:
            if re.search(r"\b(RT\b|RW\b|JL\.|Jalan|Gg\.|Gg\b)", l, re.IGNORECASE) or re.search(r"\d{5}", l):
                alamat_lines.append(l)
    result['alamat'] = ' '.join(alamat_lines).strip()

    # agama, pekerjaan, kewarganegaraan simple search
    ag = re.search(r"\b(Islam|Kristen|Katholik|Hindu|Buddha|Konghucu)\b", joined, re.IGNORECASE)
    if ag:
        result['agama'] = ag.group(1).title()
    pk = re.search(r"\b(Pegawai Negeri Sipil|Wiraswasta|Pensiunan|Pelajar)\b", joined, re.IGNORECASE)
    if pk:
        result['pekerjaan'] = pk.group(1)
    kw = re.search(r"\b(WNI|WNA|Indonesia|Indonesia)\b", joined, re.IGNORECASE)
    if kw:
        result['kewarganegaraan'] = kw.group(0).upper()

    return result


def format_extracted_data(data: dict) -> dict:
    """
    Format and clean the extracted KTP data for display and storage.
    Ensures all fields are properly formatted for the form.
    """
    if not data or not isinstance(data, dict):
        return {}
    
    formatted = {}
    
    # NIK - clean to 16 digits only
    nik = str(data.get('nik', '')).strip()
    formatted['nik'] = ''.join(c for c in nik if c.isdigit())[:16]
    
    # Nama - uppercase, clean
    formatted['nama'] = str(data.get('nama', '')).strip().upper()
    
    # Tempat Lahir - proper case
    tempat_lahir = str(data.get('tempat_lahir', '')).strip()
    formatted['tempat_lahir'] = tempat_lahir.title() if tempat_lahir else ''
    
    # Tanggal Lahir - ensure DD-MM-YYYY format
    tanggal_lahir = str(data.get('tanggal_lahir', '')).strip()
    # Try to parse and reformat if needed
    if tanggal_lahir and len(tanggal_lahir) >= 8:
        # Remove common separators and reformat
        cleaned = ''.join(c for c in tanggal_lahir if c.isdigit())
        if len(cleaned) == 8:
            # Format as DD-MM-YY
            formatted['tanggal_lahir'] = f"{cleaned[0:2]}-{cleaned[2:4]}-{cleaned[4:8]}"
        elif len(cleaned) == 6:
            # Add century prefix
            formatted['tanggal_lahir'] = f"{cleaned[0:2]}-{cleaned[2:4]}-19{cleaned[4:6]}"
        else:
            formatted['tanggal_lahir'] = tanggal_lahir
    else:
        formatted['tanggal_lahir'] = tanggal_lahir
    
    # TTL combined - for the form field
    formatted['ttl'] = f"{formatted.get('tempat_lahir', '')}, {formatted.get('tanggal_lahir', '')}".strip(', ')
    
    # Jenis Kelamin - normalize to exact format
    jk = str(data.get('jenis_kelamin', '')).strip().upper()
    if 'LAKI' in jk or 'PRIA' in jk or 'L' == jk:
        formatted['jenis_kelamin'] = 'LAKI-LAKI'
    elif 'PEREM' in jk or 'WANITA' in jk or 'P' == jk:
        formatted['jenis_kelamin'] = 'PEREMPUAN'
    else:
        formatted['jenis_kelamin'] = jk
    
    # Status Perkawinan - normalize to exact format
    status = str(data.get('status_perkawinan', '')).strip().upper()
    status_map = {
        'BELUM': 'BELUM KAWIN',
        'SINGLE': 'BELUM KAWIN',
        'KAWIN': 'KAWIN',
        'MARRIED': 'KAWIN',
        'CERAI HIDUP': 'CERAI HIDUP',
        'DIVORCED': 'CERAI HIDUP',
        'CERAI MATI': 'CERAI MATI',
        'WIDOW': 'CERAI MATI',
    }
    
    formatted['status_perkawinan'] = status
    for key, val in status_map.items():
        if key in status:
            formatted['status_perkawinan'] = val
            break
    
    # Alamat - clean and ensure it's single line for display
    alamat = str(data.get('alamat', '')).strip()
    # Remove extra whitespace and newlines
    formatted['alamat'] = ' '.join(alamat.split()).upper()
    
    # Other fields - keep as is
    formatted['agama'] = str(data.get('agama', '')).strip()
    formatted['pekerjaan'] = str(data.get('pekerjaan', '')).strip()
    formatted['kewarganegaraan'] = str(data.get('kewarganegaraan', '')).strip()
    
    return formatted


def process_ktp_image(image_file) -> Tuple[dict, str]:
    """
    Complete KTP processing pipeline: OCR -> AI extraction -> format
    Returns: (extracted_data_dict, error_message_string)
    If error occurs, returns ({}, "error message")
    """
    try:
        # Open and validate image
        image = Image.open(image_file)
        if image.mode not in ('L', 'RGB', 'RGBA'):
            image = image.convert('RGB')

        # Check Tesseract availability
        ok, ver_or_err, langs = _check_tesseract_available()
        if not ok:
            error_msg = f"Tesseract OCR tidak tersedia di sistem ini. Pesan: {ver_or_err}"
            print(f"[Error] {error_msg}")
            return {}, error_msg

        # Choose best OCR language based on available languages
        lang = 'ind+eng'  # default
        if langs:
            joined = ' '.join(langs).lower()
            if 'ind' in joined or 'indonesia' in joined:
                lang = 'ind+eng'
            elif 'eng' in joined:
                lang = 'eng'
        print(f"[OCR] Using language: {lang}, available: {langs}")

        # Run OCR
        print("[OCR] Memproses gambar KTP dengan Tesseract...")
        ocr_text, metadata = preprocess_and_ocr(image, lang=lang)
        print(f"[OCR] Extracted {len(ocr_text)} characters")

        # Check if OCR was successful
        if not ocr_text or not ocr_text.strip():
            variant_errors = [v.get('error') for v in metadata.get('variants', []) if v.get('error')]
            error_parts = ["Tesseract OCR gagal mengekstrak teks dari gambar."]
            error_parts.append("Coba dengan gambar yang lebih jelas atau berkualitas lebih baik.")
            if variant_errors:
                error_parts.append(f"Detail: {'; '.join(variant_errors)}")
            error_msg = ' '.join(error_parts)
            print(f"[Error] {error_msg}")
            return {}, error_msg

        # Analyze with Gemini
        print("[Gemini] Menganalisis teks OCR dengan AI...")
        extracted_data, error = analyze_ktp_with_gemini(ocr_text)

        # If Gemini fails or returns empty, fallback to local heuristic parser
        if error or not extracted_data:
            print(f"[Warning] Gemini failed or returned no data: {error}")
            print("[Fallback] Attempting local OCR parsing heuristics...")
            local_data = _local_parse_ocr_text(ocr_text)
            if local_data and local_data.get('nik') and local_data.get('nama'):
                print("[Fallback] Local parser produced data; using fallback values.")
                extracted_data = local_data
            else:
                error_msg = f"Gemini AI gagal menganalisis teks: {error}"
                print(f"[Error] {error_msg}")
                return {}, error_msg

        # Validate that we got reasonable data
        if not extracted_data or not extracted_data.get('nik'):
            error_msg = "AI tidak berhasil mengekstrak data KTP. Coba gambar dengan lebih jelas."
            print(f"[Error] {error_msg}")
            return {}, error_msg

        # Format the extracted data for display
        print("[Format] Memformat data KTP...")
        formatted_data = format_extracted_data(extracted_data)

        print(f"[Success] Extracted KTP data successfully")
        return formatted_data, ''

    except Exception as e:
        error_msg = f"Error memproses KTP: {str(e)}"
        print(f"[Error] {error_msg}")
        return {}, error_msg
