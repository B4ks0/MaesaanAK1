# Tutorial Sambung Website ke Domain (Django + Nginx + VM)

Ini panduan **realistis & step-by-step** untuk menghubungkan domain ke Django yang berjalan di VM.

> **Intinya dulu (biar clear):**
> ❌ **Domain TIDAK bisa langsung menunjuk ke `localhost:8000`**
> ✅ Domain **harus menunjuk ke IP publik VM**, lalu **port 80/443** → diteruskan ke Django (`8000`) lewat **reverse proxy**

---

## Arsitektur yang BENAR (wajib paham dulu)

```
Internet
   ↓
Domain (example.com)
   ↓
IP Publik VM
   ↓
Nginx (port 80 / 443)
   ↓
Django (127.0.0.1:8000)
```

> **Django jangan diekspos langsung ke internet.**
> Yang hadapi publik = **Nginx**

---

## LANGKAH 1 — Arahkan DOMAIN ke IP VM

Masuk ke **DNS Manager domain kamu** (Niagahoster / Rumahweb / Cloudflare / dll)

Buat **A Record**:

| Type | Name  | Value          |
| ---- | ----- | -------------- |
| A    | `@`   | `IP_PUBLIK_VM` |
| A    | `www` | `IP_PUBLIK_VM` |

Contoh:

```
example.com → 103.xxx.xxx.xxx
www.example.com → 103.xxx.xxx.xxx
```

⏳ Tunggu ±1–5 menit (kadang sampai 1 jam)

---

## LANGKAH 2 — Pastikan Django jalan di VM

Di VM:

```bash
python manage.py runserver 127.0.0.1:8000
```

⚠️ **JANGAN**

```bash
0.0.0.0:8000
```

itu bahaya buat production.

---

## LANGKAH 3 — Install Nginx di VM

```bash
sudo apt update
sudo apt install nginx -y
```

Cek:

```bash
systemctl status nginx
```

Buka browser:

```
http://IP_VM
```

Kalau keluar **Welcome to Nginx** → OK

---

## LANGKAH 4 — Konfigurasi Nginx → Django

### Buat config baru:

```bash
sudo nano /etc/nginx/sites-available/django
```

Isi:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Aktifkan:

```bash
sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## LANGKAH 5 — Set `ALLOWED_HOSTS` Django

Di `settings.py`:

```python
ALLOWED_HOSTS = [
    "example.com",
    "www.example.com",
    "IP_VM"
]
```

Restart Django:

```bash
CTRL + C
python manage.py runserver 127.0.0.1:8000
```

---

## LANGKAH 6 — TEST

Buka browser:

```
http://example.com
```

🎉 **Sekarang domain → Django localhost:8000**

---

## (OPSIONAL TAPI WAJIB UNTUK PRODUKSI) HTTPS

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d example.com -d www.example.com
```

Nginx otomatis jadi:

```
https://example.com
```

---

## Q: "Gimana kalau ada 5 domain & 5 website Django beda di 1 VM?"

Jawabannya: **BISA BANGET**. Itu nama teknisnya **Virtual Hosting**.

> **Ilustrasi:**
> 1 VM
> 1 IP Publik
> 5 Domain beda
> 5 Aplikasi Django jalan di port beda (8001, 8002, 8003, dst)

### Arsitektur Multi-Domain

```
Domain A ──┐
Domain B ──┼──► IP VM (NGINX) ──┬──► Django A (Port 8001)
Domain C ──┘                    ├──► Django B (Port 8002)
                                └──► Django C (Port 8003)
```

### Caranya:

#### 1. Jalankan tiap Django di port beda
```bash
# App 1
python manage.py runserver 127.0.0.1:8001

# App 2
python manage.py runserver 127.0.0.1:8002

# App 3
python manage.py runserver 127.0.0.1:8003
```

#### 2. Buat Config Nginx terpisah buat tiap domain
Contoh `/etc/nginx/sites-available/app1`:
```nginx
server {
    listen 80;
    server_name domain1.com;
    location / {
        proxy_pass http://127.0.0.1:8001;
    }
}
```

Contoh `/etc/nginx/sites-available/app2`:
```nginx
server {
    listen 80;
    server_name domain2.com;
    location / {
        proxy_pass http://127.0.0.1:8002;
    }
}
```

#### 3. Aktifkan semua
```bash
sudo ln -s /etc/nginx/sites-available/app1 /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/app2 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4. HTTPS Massal
```bash
sudo certbot --nginx -d domain1.com -d domain2.com -d domain3.com
```

---

## RANGKUMAN CEPAT (REALITA)

| Pertanyaan                              | Jawaban             |
| --------------------------------------- | ------------------- |
| Domain ke localhost:8000 bisa langsung? | ❌ Tidak             |
| Harus hosting?                          | ✅ VM kamu = hosting |
| Butuh Nginx?                            | ✅ WAJIB             |
| Django langsung expose ke publik?       | ❌ Jangan            |
| Ini standar industri?                   | ✅ Iya               |
