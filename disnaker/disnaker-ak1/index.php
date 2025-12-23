<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'config/database.php';
include 'includes/functions.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAESAAN - Sistem Kartu Pencari Kerja AK1</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* SEMUA CSS SAMA SEBELUMNYA - TIDAK DIUBAH */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: #2c3e50;
            padding: 40px 0;
            box-shadow: 0 4px 20px rgba(243, 156, 18, 0.3);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            pointer-events: none;
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            text-align: center;
            position: relative;
            z-index: 1;
        }

        .header h1 {
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .header p {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 5px;
        }

        .header-subtitle {
            font-size: 1.1em;
            opacity: 0.8;
        }

        /* Navigation - DIUBAH: Hanya Login */
        .nav-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .nav {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 15px 0;
            gap: 30px;
        }

        .nav-item {
            color: #333;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 25px;
            transition: all 0.3s ease;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-item:hover {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(243, 156, 18, 0.3);
        }

        .nav-item.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        /* Main Content */
        .main-content {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }

        /* Card Styles */
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        .card-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5em;
            margin-right: 15px;
            box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
        }

        .card-title {
            font-size: 1.4em;
            font-weight: 600;
            color: #2c3e50;
        }

        /* Grid Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        /* Feature Icons */
        .feature-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            color: white;
            font-size: 2em;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        }

        /* Status Items */
        .status-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .status-item {
            background: rgba(243, 156, 18, 0.1);
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #f39c12;
            text-align: center;
        }

        .status-label {
            font-size: 0.9em;
            color: #8b7355;
            font-weight: 500;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .status-value {
            font-size: 1.3em;
            font-weight: 600;
            color: #2c3e50;
        }

        .status-active {
            color: #27ae60 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .status-active::before {
            content: '●';
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        /* Buttons */
        .btn {
            border-radius: 25px;
            font-weight: 600;
            padding: 15px 30px;
            transition: all 0.3s ease;
            border: none;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1em;
        }

        .btn-primary {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }

        .btn-primary:hover {
            background: linear-gradient(135deg, #e67e22 0%, #f39c12 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(243, 156, 18, 0.4);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-secondary:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        /* Action Grid */
        .action-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .action-item {
            background: rgba(102, 126, 234, 0.1);
            padding: 25px;
            border-radius: 15px;
            text-decoration: none;
            color: #2c3e50;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .action-item:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        .action-icon {
            width: 50px;
            height: 50px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4em;
        }

        .action-text {
            flex: 1;
        }

        .action-title {
            font-weight: 600;
            margin-bottom: 5px;
            font-size: 1.1em;
        }

        .action-desc {
            font-size: 0.9em;
            opacity: 0.8;
        }

        /* Footer */
        .footer {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            text-align: center;
            padding: 40px 20px;
            margin-top: 60px;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Timeline */
        .timeline {
            border-left: 3px solid #3498db;
            margin: 20px 0;
            padding-left: 20px;
        }

        .timeline-item {
            margin-bottom: 25px;
            position: relative;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: -26px;
            top: 5px;
            width: 12px;
            height: 12px;
            background: #3498db;
            border-radius: 50%;
        }

        /* Login Admin Info */
        .admin-info {
            background: rgba(52, 152, 219, 0.1);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #3498db;
            margin-top: 15px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.5em;
            }

            .header p {
                font-size: 1.1em;
            }

            .nav {
                flex-wrap: wrap;
                gap: 15px;
            }

            .nav-item {
                padding: 10px 20px;
                font-size: 0.9em;
            }

            .dashboard-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .status-info {
                grid-template-columns: 1fr;
            }

            .action-grid {
                grid-template-columns: 1fr;
            }

            .btn {
                padding: 12px 25px;
                font-size: 1em;
            }
        }
    </style>
</head>
<body>

<header class="header">
    <div class="header-content">
        <h1>MAESAAN</h1>
        <p>Sistem Kartu Pencari Kerja Digital</p>
        <p class="header-subtitle">Dinas Tenaga Kerja Kabupaten Minahasa</p>
    </div>
</header>

<div class="nav-container">
    <div class="nav-content">
        <nav class="nav">
            <a href="index.php" class="nav-item active">
                <i class="fas fa-home"></i> Beranda
            </a>
            <a href="login.php" class="nav-item">
                <i class="fas fa-sign-in-alt"></i> Login
            </a>
        </nav>
    </div>
</div>

<div class="main-content">
    <!-- Hero Actions -->
    <div class="dashboard-grid">
        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <div class="card-title">Mulai Sekarang</div>
            </div>
            <div class="action-grid">
                <a href="login.php" class="action-item">
                    <div class="action-icon">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="action-text">
                        <div class="action-title">Login</div>
                        <div class="action-desc">Akses dashboard pencari kerja</div>
                    </div>
                </a>
            </div>
        </div>

        <!-- Status Info -->
        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-info-circle"></i>
                </div>
                <div class="card-title">Informasi Layanan</div>
            </div>
            <div class="status-info">
                <div class="status-item">
                    <div class="status-label">Waktu Verifikasi</div>
                    <div class="status-value">5-10 Menit</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Biaya Layanan</div>
                    <div class="status-value status-active">GRATIS</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Masa Berlaku</div>
                    <div class="status-value">2 Tahun</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Format AK1</div>
                    <div class="status-value">AK1/MIN/2025/XXXXXX</div>
                </div>
            </div>
        </div>
    </div>

    <!-- SOP Information -->
    <div class="card">
        <div class="card-header">
            <div class="card-icon">
                <i class="fas fa-file-alt"></i>
            </div>
            <div class="card-title">Alur Pendaftaran AK1</div>
        </div>
        <div class="timeline">
            <div class="timeline-item">
                <h4>1. Login ke Sistem</h4>
                <p>Gunakan akun user untuk masuk ke dashboard</p>
            </div>
            <div class="timeline-item">
                <h4>2. Isi Formulir Pendaftaran</h4>
                <p>Lengkapi data diri dan upload dokumen persyaratan</p>
            </div>
            <div class="timeline-item">
                <h4>3. Verifikasi oleh Admin</h4>
                <p>Petugas memverifikasi kelengkapan dokumen (5-10 menit)</p>
            </div>
            <div class="timeline-item">
                <h4>4. Terbitkan Kartu AK1</h4>
                <p>Sistem menghasilkan kartu AK1 digital yang dapat diunduh</p>
            </div>
        </div>
    </div>

    <!-- Contact Info -->
    <div class="card">
        <div class="card-header">
            <div class="card-icon">
                <i class="fas fa-address-card"></i>
            </div>
            <div class="card-title">Kontak Layanan</div>
        </div>
        <div class="status-info">
            <div class="status-item">
                <div class="status-label">Alamat</div>
                <div class="status-value">Dinas Tenaga Kerja<br>Kabupaten Minahasa</div>
            </div>
            <div class="status-item">
                <div class="status-label">Jam Layanan</div>
                <div class="status-value">Senin - Kamis: 08:00-16:00<br>Jumat: 08:00-15:30</div>
            </div>
            <div class="status-item">
                <div class="status-label">Telepon</div>
                <div class="status-value">[Nomor Telepon]</div>
            </div>
            <div class="status-item">
                <div class="status-label">WhatsApp</div>
                <div class="status-value">[Nomor WhatsApp]</div>
            </div>
        </div>
    </div>
</div>

<footer class="footer">
    <div class="footer-content">
        <h3><i class="fas fa-building"></i> Dinas Tenaga Kerja Kabupaten Minahasa</h3>
        <p>Sistem Layanan Digital Kartu Pencari Kerja (AK-1) - MAESAAN</p>
        <p>&copy; 2024 All Rights Reserved | Sesuai SOP Layanan</p>
    </div>
</footer>

<script>
    // Animasi seperti di dashboard
    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 200);
        });
    });
</script>

</body>
</html>