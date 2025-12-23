<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'config/database.php';
include 'includes/functions.php';

// Start session
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Redirect ke login jika belum login
if (!isset($_SESSION['user_id']) || empty($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}

// Ambil data user dari database
$user_id = $_SESSION['user_id'];
try {
    $pdo = Database::getInstance()->getConnection();
    $stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
    $stmt->execute([$user_id]);
    $user = $stmt->fetch();
    
    if (!$user) {
        session_destroy();
        header("Location: login.php");
        exit();
    }
} catch (Exception $e) {
    die("Database error: " . $e->getMessage());
}

// Ambil data pendaftaran AK1
$stmt = $pdo->prepare("SELECT * FROM pendaftaran_ak1 WHERE user_id = ? ORDER BY created_at DESC LIMIT 1");
$stmt->execute([$user_id]);
$pendaftaran = $stmt->fetch();

// Set data untuk dashboard
$username = $user['nama_lengkap'];
$status_kartu = $pendaftaran ? getStatusText($pendaftaran['status']) : "Belum Mendaftar";
$masa_berlaku = $pendaftaran && $pendaftaran['status'] == 'diverifikasi' ? 
    date('d-m-Y', strtotime('+2 years', strtotime($pendaftaran['verified_at']))) : "-";
$tanggal_terbit = $pendaftaran && $pendaftaran['status'] == 'diverifikasi' ? 
    formatTanggal($pendaftaran['verified_at']) : "-";
?>

<!-- SALIN SEMUA CODE DASHBOARD ANDA YANG SUDAH DIBUAT -->
<!-- PASTIKAN UNTUK MENGUBAH VARIABLE PHP DI DALAMNYA -->

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Kartu Pencari Kerja AK1</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* COPY ALL YOUR EXISTING CSS STYLES HERE */
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
            padding: 30px 0;
            box-shadow: 0 4px 20px rgba(243, 156, 18, 0.3);
            position: relative;
            overflow: hidden;
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-left h1 {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .user-profile {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            min-width: 250px;
        }

        .user-avatar {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2em;
            color: white;
            margin: 0 auto 15px;
        }

        .user-name {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .user-status {
            background: #27ae60;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            display: inline-block;
        }

        /* Navigation Styles */
        .nav-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
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
            padding: 20px 0;
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
            padding-bottom: 100px;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
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
        }

        .card-title {
            font-size: 1.4em;
            font-weight: 600;
            color: #2c3e50;
        }

        /* Status Card Specific */
        .status-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .status-item {
            background: rgba(243, 156, 18, 0.1);
            padding: 15px;
            border-radius: 12px;
            border-left: 4px solid #f39c12;
        }

        .status-label {
            font-size: 0.9em;
            color: #8b7355;
            font-weight: 500;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .status-value {
            font-size: 1.1em;
            font-weight: 600;
            color: #2c3e50;
        }

        .status-active {
            color: #27ae60 !important;
            display: flex;
            align-items: center;
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

        /* Quick Actions */
        .action-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .action-item {
            background: rgba(102, 126, 234, 0.1);
            padding: 20px;
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
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .action-icon {
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
        }

        .action-text {
            flex: 1;
        }

        .action-title {
            font-weight: 600;
            margin-bottom: 3px;
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
            padding: 30px 20px;
            margin-top: 60px;
        }

        /* Progress Bar */
        .progress-container {
            background: rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            height: 8px;
            margin: 15px 0;
            overflow: hidden;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            border-radius: 10px;
            transition: width 1s ease;
        }

        /* Card Full Width */
        .card-full {
            grid-column: 1 / -1;
        }

        /* Statistics */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-item {
            text-align: center;
            padding: 20px 15px;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
        }

        .stat-number {
            font-size: 2em;
            font-weight: 700;
            color: #f39c12;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 0.9em;
            color: #666;
            font-weight: 500;
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
                text-align: center;
            }

            .header-left h1 {
                font-size: 2em;
            }

            .nav {
                flex-wrap: wrap;
                gap: 15px;
                justify-content: center;
            }

            .nav-item {
                padding: 10px 16px;
                font-size: 0.9em;
            }

            .dashboard-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .action-grid {
                grid-template-columns: 1fr;
            }

            .status-info {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

<header class="header">
    <div class="header-content">
        <div class="header-left">
            <h1>MAESAAN</h1>
            <p>Sistem Kartu Pencari Kerja Digital</p>
        </div>
        <div class="user-profile">
            <div class="user-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="user-name"><?php echo htmlspecialchars($username); ?></div>
            <div class="user-status"><?php echo $status_kartu; ?></div>
        </div>
    </div>
</header>

<div class="nav-container">
    <div class="nav-content">
        <nav class="nav">
            <a href="dashboard.php" class="nav-item active">
                <i class="fas fa-home"></i> Dashboard
            </a>
            <a href="pendaftaran-ak1.php" class="nav-item">
                <i class="fas fa-edit"></i> Daftar AK1
            </a>
            <a href="kartu-ak1.php" class="nav-item">
                <i class="fas fa-id-card"></i> Kartu AK1
            </a>
            <a href="profil.php" class="nav-item">
                <i class="fas fa-user-edit"></i> Profil Saya
            </a>
            <a href="logout.php" class="nav-item">
                <i class="fas fa-sign-out-alt"></i> Logout
            </a>
        </nav>
    </div>
</div>

<div class="main-content">
    <div class="dashboard-grid">
        <!-- Status Kartu Card -->
        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-id-badge"></i>
                </div>
                <div class="card-title">Status Kartu AK1</div>
            </div>
            <div class="status-info">
                <div class="status-item">
                    <div class="status-label">Status Kartu</div>
                    <div class="status-value status-active">
                        <?php echo $status_kartu; ?>
                    </div>
                </div>
                <div class="status-item">
                    <div class="status-label">Tanggal Terbit</div>
                    <div class="status-value"><?php echo $tanggal_terbit; ?></div>
                </div>
                <div class="status-item">
                    <div class="status-label">Masa Berlaku</div>
                    <div class="status-value"><?php echo $masa_berlaku; ?></div>
                </div>
                <div class="status-item">
                    <div class="status-label">Validitas</div>
                    <div class="status-value">
                        <div class="progress-container">
                            <div class="progress-bar" style="width: <?php echo $pendaftaran ? '75%' : '0%'; ?>"></div>
                        </div>
                        <small><?php echo $pendaftaran ? '75% tersisa' : '0% tersisa'; ?></small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quick Actions Card -->
        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-bolt"></i>
                </div>
                <div class="card-title">Aksi Cepat</div>
            </div>
            <div class="action-grid">
                <a href="pendaftaran-ak1.php" class="action-item">
                    <div class="action-icon">
                        <i class="fas fa-plus-circle"></i>
                    </div>
                    <div class="action-text">
                        <div class="action-title">Daftar Baru</div>
                        <div class="action-desc">Buat kartu AK1 baru</div>
                    </div>
                </a>
                <a href="kartu-ak1.php" class="action-item">
                    <div class="action-icon">
                        <i class="fas fa-download"></i>
                    </div>
                    <div class="action-text">
                        <div class="action-title">Unduh Kartu</div>
                        <div class="action-desc">Cetak kartu digital</div>
                    </div>
                </a>
                <a href="profil.php" class="action-item">
                    <div class="action-icon">
                        <i class="fas fa-edit"></i>
                    </div>
                    <div class="action-text">
                        <div class="action-title">Update Profil</div>
                        <div class="action-desc">Perbarui data diri</div>
                    </div>
                </a>
                <a href="logout.php" class="action-item">
                    <div class="action-icon">
                        <i class="fas fa-sign-out-alt"></i>
                    </div>
                    <div class="action-text">
                        <div class="action-title">Logout</div>
                        <div class="action-desc">Keluar dari sistem</div>
                    </div>
                </a>
            </div>
        </div>

        <!-- Statistics Card -->
        <div class="card card-full">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <div class="card-title">Statistik Pencarian Kerja</div>
            </div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">0</div>
                    <div class="stat-label">Lowongan Dilihat</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">0</div>
                    <div class="stat-label">Lamaran Terkirim</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">0</div>
                    <div class="stat-label">Interview</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">1</div>
                    <div class="stat-label">Hari Aktif</div>
                </div>
            </div>
        </div>

        <!-- Announcements Card -->
        <div class="card card-full">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-bullhorn"></i>
                </div>
                <div class="card-title">Pengumuman & Informasi</div>
            </div>
            <div class="announcement-item">
                <div class="announcement-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="announcement-text">
                    <strong>Peringatan:</strong> <?php echo $pendaftaran ? 'Laporan 3 bulanan wajib dilakukan agar kartu tetap aktif.' : 'Silakan daftar kartu AK1 untuk mendapatkan layanan lengkap.'; ?>
                </div>
            </div>
            <div class="announcement-item">
                <div class="announcement-icon">
                    <i class="fas fa-info-circle"></i>
                </div>
                <div class="announcement-text">
                    <strong>Info:</strong> Bawa dokumen asli (KTP, Ijazah, Pas Foto) saat verifikasi di kantor Dinas Ketenagakerjaan terdekat.
                </div>
            </div>
            <div class="announcement-item">
                <div class="announcement-icon">
                    <i class="fas fa-star"></i>
                </div>
                <div class="announcement-text">
                    <strong>Selamat Datang:</strong> Anda berhasil login ke sistem DISNAKER AK1. <?php echo $pendaftaran ? 'Kartu AK1 Anda sedang dalam proses verifikasi.' : 'Silakan lengkapi pendaftaran AK1 Anda.'; ?>
                </div>
            </div>
        </div>
    </div>
</div>

<footer class="footer">
    <div class="footer-content">
        <h3><i class="fas fa-building"></i> Dinas Ketenagakerjaan</h3>
        <p>Sistem Kartu Pencari Kerja Digital (AK1) - Memudahkan pencarian kerja untuk semua</p>
        <p>&copy; 2024 All Rights Reserved | Powered by Digital Innovation</p>
    </div>
</footer>

<script>
    // JavaScript dari dashboard Anda
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    window.addEventListener('load', function() {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 500);
        });
    });
</script>

</body>
</html>