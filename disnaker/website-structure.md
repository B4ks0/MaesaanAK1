# MAESAAN - Sistem Kartu Pencari Kerja AK1 Digital

## Overview
MAESAAN adalah sistem layanan digital untuk pendaftaran dan pengelolaan Kartu Pencari Kerja (AK1) yang dikembangkan untuk Dinas Tenaga Kerja Kabupaten Minahasa. Sistem ini menyediakan platform lengkap untuk proses pendaftaran, verifikasi, dan pengelolaan kartu AK1 secara digital.

## Arsitektur Sistem

### Struktur Direktori
```
c:/xampp/htdocs/disnaker-ak1/
├── index.php                    # Landing page utama
├── dashboard.php               # Dashboard user
├── pendaftaran-ak1.php         # Form pendaftaran dengan OCR
├── kartu-ak1.php              # Halaman kartu AK1
├── profil.php                  # Manajemen profil user
├── status-pendaftaran.php      # Status pendaftaran
├── login.php                   # Login user
├── register.php                # Registrasi user
├── logout.php                  # Logout
├── admin/                      # Panel admin
│   ├── dashboard_admin.php
│   ├── login_admin.php
│   └── verifikasi_pendaftaran.php
├── config/                     # Konfigurasi sistem
│   ├── database.php
│   └── init.php
├── includes/                   # Komponen reusable
│   ├── functions.php
│   ├── auth.php
│   ├── validator.php
│   ├── header.php
│   └── footer.php
└── assets/                     # Static assets
    ├── css/
    └── js/
```

## Flowchart Sistem

### 1. Landing Page (index.php)
```
Beranda → [Login] → Dashboard
    ↓
Informasi Layanan
    ↓
Alur Pendaftaran AK1
    ↓
Kontak Layanan
```

### 2. User Registration Flow
```
Register → Email Verification → Login → Dashboard
```

### 3. AK1 Registration Flow
```
Dashboard → Daftar AK1 → OCR Scan KTP → Upload Dokumen → Submit Form → Admin Verification → Kartu AK1
```

### 4. Admin Verification Flow
```
Admin Login → Dashboard Admin → Verifikasi Pendaftaran → Approve/Reject → Generate Kartu AK1
```

## Fitur Utama

### 🎯 User Features

#### Authentication & Authorization
- **User Registration**: Form registrasi dengan validasi email dan password
- **User Login**: Sistem login dengan session management
- **Profile Management**: Update data profil dan informasi pribadi
- **Secure Logout**: Logout dengan penghapusan session

#### AK1 Card Management
- **Digital Card Generation**: Pembuatan kartu AK1 digital
- **Card Status Tracking**: Monitoring status pendaftaran real-time
- **Card Download**: Unduh kartu AK1 dalam format digital
- **Card Validity Check**: Cek masa berlaku kartu (2 tahun)

#### Advanced Registration
- **OCR KTP Scanner**: Scan otomatis KTP menggunakan Tesseract.js
- **Photo Upload**: Upload pas foto 3x4 dengan validasi ukuran
- **Document Upload**: Upload ijazah/sertifikat dengan multiple format
- **Form Auto-fill**: Isi form otomatis dari hasil OCR
- **Real-time Validation**: Validasi form real-time dengan feedback

### 👨‍💼 Admin Features

#### Admin Dashboard
- **Statistics Overview**: Statistik pendaftaran dan verifikasi
- **User Management**: Kelola data pengguna sistem
- **Application Management**: Kelola aplikasi pendaftaran AK1

#### Verification System
- **Document Review**: Review dokumen yang diupload user
- **Application Approval**: Approve/reject aplikasi pendaftaran
- **Status Updates**: Update status pendaftaran real-time
- **Bulk Operations**: Operasi massal untuk multiple applications

## Fasilitas Teknis

### 🔧 Backend Technologies

#### PHP Core System
- **Session Management**: Secure session handling
- **Database Abstraction**: PDO untuk database operations
- **Error Handling**: Comprehensive error reporting
- **Security**: Input sanitization dan validation

#### Database Structure
```sql
-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nama_lengkap VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pendaftaran AK1 table
CREATE TABLE pendaftaran_ak1 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    nik VARCHAR(16) NOT NULL,
    nama VARCHAR(255) NOT NULL,
    ttl VARCHAR(255) NOT NULL,
    jk ENUM('LAKI-LAKI', 'PEREMPUAN') NOT NULL,
    status ENUM('BELUM KAWIN', 'KAWIN', 'CERAI HIDUP', 'CERAI MATI'),
    pendidikan VARCHAR(50),
    alamat TEXT NOT NULL,
    keahlian VARCHAR(255),
    pengalaman TEXT,
    photo_data LONGTEXT,
    ijazah_data LONGTEXT,
    status ENUM('pending', 'diverifikasi', 'ditolak') DEFAULT 'pending',
    verified_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 🎨 Frontend Technologies

#### UI/UX Design
- **Responsive Design**: Mobile-first approach
- **Modern CSS**: Gradient backgrounds, glassmorphism effects
- **Font Awesome Icons**: Comprehensive icon library
- **Smooth Animations**: CSS transitions dan JavaScript animations

#### JavaScript Features
- **OCR Integration**: Tesseract.js untuk text recognition
- **Camera API**: Webcam access untuk KTP scanning
- **Drag & Drop**: File upload dengan drag and drop
- **Real-time Preview**: Preview gambar sebelum upload
- **Form Validation**: Client-side validation dengan feedback

### 📱 Mobile Responsiveness

#### Breakpoints
- **Desktop**: > 1200px
- **Tablet**: 768px - 1199px
- **Mobile**: < 768px

#### Responsive Features
- **Flexible Grid**: CSS Grid untuk layout adaptif
- **Touch-Friendly**: Button sizes dan spacing untuk mobile
- **Optimized Images**: Responsive image handling
- **Readable Typography**: Font scaling untuk different screens

## Security Features

### 🔒 Authentication Security
- **Password Hashing**: bcrypt untuk password storage
- **Session Security**: Secure session configuration
- **CSRF Protection**: Token-based CSRF prevention
- **Input Validation**: Server-side input sanitization

### 🛡️ Data Protection
- **SQL Injection Prevention**: Prepared statements
- **XSS Protection**: HTML entity encoding
- **File Upload Security**: File type dan size validation
- **Access Control**: Role-based access control

## Performance Optimization

### ⚡ Loading Optimization
- **Lazy Loading**: Images loaded on demand
- **Minified Assets**: Compressed CSS dan JavaScript
- **Caching**: Browser caching untuk static assets
- **CDN Integration**: Font Awesome dari CDN

### 🚀 Database Optimization
- **Indexed Queries**: Optimized database indexes
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Efficient SQL queries
- **Data Pagination**: Paginated data loading

## Integration Points

### 📧 Email System
- **Registration Confirmation**: Email verification
- **Status Updates**: Notification emails
- **Password Reset**: Secure password recovery

### 📄 Document Processing
- **OCR Engine**: Tesseract.js integration
- **Image Processing**: Canvas manipulation
- **File Storage**: Base64 encoding untuk database storage
- **Format Support**: JPG, PNG, PDF support

## SOP (Standard Operating Procedure)

### 📋 User Registration Process
1. **Access Landing Page**: User mengakses halaman utama
2. **Register Account**: Isi form registrasi
3. **Email Verification**: Verifikasi email (opsional)
4. **Login**: Masuk ke dashboard
5. **Complete Profile**: Lengkapi data profil

### 📝 AK1 Application Process
1. **Start Application**: Klik "Daftar AK1"
2. **OCR Scan**: Scan KTP menggunakan kamera/OCR
3. **Upload Documents**: Upload pas foto dan ijazah
4. **Fill Form**: Lengkapi form pendaftaran
5. **Submit Application**: Kirim aplikasi
6. **Wait Verification**: Tunggu verifikasi admin
7. **Download Card**: Unduh kartu AK1 jika disetujui

### ✅ Admin Verification Process
1. **Admin Login**: Masuk ke panel admin
2. **Review Applications**: Tinjau aplikasi pending
3. **Verify Documents**: Periksa kelengkapan dokumen
4. **Approve/Reject**: Setujui atau tolak aplikasi
5. **Generate Card**: Sistem generate kartu digital
6. **Notify User**: Kirim notifikasi ke user

## Maintenance & Support

### 🔧 System Maintenance
- **Regular Backups**: Database dan file backups
- **Security Updates**: Regular security patches
- **Performance Monitoring**: System performance tracking
- **Error Logging**: Comprehensive error logging

### 📞 Support Features
- **Contact Information**: Informasi kontak layanan
- **Service Hours**: Jam operasional layanan
- **Help Documentation**: Panduan pengguna
- **Status Page**: Sistem status dan informasi

## Future Enhancements

### 🚀 Planned Features
- **SMS Notifications**: SMS untuk status updates
- **Mobile App**: Native mobile application
- **API Integration**: REST API untuk third-party integration
- **Advanced Analytics**: Detailed reporting dan analytics
- **Multi-language Support**: Bahasa Indonesia dan Inggris
- **Offline Mode**: PWA dengan offline capabilities

### 📈 Scalability Improvements
- **Microservices Architecture**: Modular system design
- **Cloud Deployment**: AWS/Azure deployment ready
- **Load Balancing**: Multi-server deployment support
- **Database Sharding**: Horizontal scaling support

## Deployment Guide

### 🖥️ Server Requirements
- **PHP**: Version 7.4+
- **MySQL**: Version 5.7+
- **Web Server**: Apache/Nginx
- **SSL Certificate**: HTTPS support
- **File Permissions**: Proper directory permissions

### 📦 Installation Steps
1. **Clone Repository**: Download source code
2. **Configure Database**: Setup MySQL database
3. **Update Config**: Configure database credentials
4. **Set Permissions**: Configure file permissions
5. **Run Installation**: Execute setup script
6. **Test System**: Verify all features working

### 🔄 Update Process
1. **Backup Data**: Backup database dan files
2. **Download Update**: Get latest version
3. **Apply Changes**: Update source code
4. **Run Migrations**: Execute database migrations
5. **Test Updates**: Verify system functionality
6. **Deploy Changes**: Push to production

## Conclusion

MAESAAN merupakan sistem digital yang komprehensif untuk pengelolaan Kartu Pencari Kerja AK1 dengan fitur modern seperti OCR scanning, responsive design, dan admin panel yang powerful. Sistem ini dirancang untuk kemudahan pengguna sekaligus efisiensi operasional Dinas Tenaga Kerja.

Dengan arsitektur yang modular dan teknologi terkini, sistem ini siap untuk dikembangkan lebih lanjut sesuai kebutuhan masa depan. Dokumentasi lengkap ini dapat digunakan sebagai blueprint untuk membangun sistem serupa atau melakukan pengembangan lebih lanjut.
