<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'config/database.php';
include 'includes/functions.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Redirect jika sudah login
if (isUserLoggedIn()) {
    redirect('dashboard.php');
}

$errors = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nama_lengkap = sanitizeInput($_POST['nama_lengkap'] ?? '');
    $email = sanitizeInput($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $password_confirm = $_POST['password_confirm'] ?? '';
    $no_telepon = sanitizeInput($_POST['no_telepon'] ?? '');

    // Validasi
    if (empty($nama_lengkap)) {
        $errors[] = "Nama lengkap harus diisi";
    }

    if (empty($email) || !validateEmail($email)) {
        $errors[] = "Email tidak valid";
    }

    if (strlen($password) < 6) {
        $errors[] = "Password minimal 6 karakter";
    }

    if ($password !== $password_confirm) {
        $errors[] = "Konfirmasi password tidak sesuai";
    }

    // Cek email unique
    if (empty($errors)) {
        $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
        $stmt->execute([$email]);
        
        if ($stmt->fetch()) {
            $errors[] = "Email sudah terdaftar";
        }
    }

    // Insert ke database
    if (empty($errors)) {
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        
        $stmt = $pdo->prepare("INSERT INTO users (nama_lengkap, email, password, no_telepon) VALUES (?, ?, ?, ?)");
        $stmt->execute([$nama_lengkap, $email, $hashed_password, $no_telepon]);
        
        $_SESSION['success'] = "Registrasi berhasil! Silakan login.";
        redirect('login.php');
    }
}
?>

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daftar - MAESAAN</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
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

        /* Header Styles - Sama seperti dashboard */
        .header {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: #2c3e50;
            padding: 30px 0;
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
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        /* Navigation Styles */
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
            max-width: 600px;
            margin: 40px auto;
            padding: 0 20px;
        }

        /* Card Styles - Sama seperti dashboard */
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
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
            justify-content: center;
            margin-bottom: 30px;
            text-align: center;
        }

        .card-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.8em;
            margin-right: 15px;
            box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
        }

        .card-title {
            font-size: 1.6em;
            font-weight: 600;
            color: #2c3e50;
        }

        /* Form Styles */
        .form-group {
            margin-bottom: 25px;
        }

        .form-label {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
            display: block;
        }

        .form-control {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            font-size: 1em;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.8);
        }

        .form-control:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
            background: white;
        }

        .form-text {
            font-size: 0.85em;
            color: #6c757d;
            margin-top: 5px;
        }

        /* Buttons */
        .btn {
            border-radius: 12px;
            font-weight: 600;
            padding: 15px 30px;
            transition: all 0.3s ease;
            border: none;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 1.1em;
            cursor: pointer;
            width: 100%;
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

        .btn-outline {
            background: transparent;
            border: 2px solid #3498db;
            color: #3498db;
        }

        .btn-outline:hover {
            background: #3498db;
            color: white;
        }

        /* Alert Styles */
        .alert {
            padding: 15px 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: none;
            font-weight: 500;
        }

        .alert-danger {
            background: rgba(231, 76, 60, 0.1);
            color: #c0392b;
            border-left: 4px solid #e74c3c;
        }

        .alert-danger ul {
            margin: 0;
            padding-left: 20px;
        }

        .alert-danger li {
            margin-bottom: 5px;
        }

        /* Links */
        .text-link {
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .text-link:hover {
            color: #2980b9;
            text-decoration: underline;
        }

        /* Info Box */
        .info-box {
            background: rgba(52, 152, 219, 0.1);
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #3498db;
            margin-bottom: 25px;
        }

        .info-box h6 {
            color: #2980b9;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .info-box ul {
            margin: 0;
            padding-left: 20px;
            color: #2c3e50;
        }

        .info-box li {
            margin-bottom: 5px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }

            .header p {
                font-size: 1em;
            }

            .nav {
                flex-wrap: wrap;
                gap: 15px;
            }

            .nav-item {
                padding: 10px 20px;
                font-size: 0.9em;
            }

            .main-content {
                margin: 20px auto;
            }

            .card {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>

<header class="header">
    <div class="header-content">
        <h1>MAESAAN</h1>
        <p>Sistem Kartu Pencari Kerja Digital</p>
    </div>
</header>

<div class="nav-container">
    <div class="nav-content">
        <nav class="nav">
            <a href="index.php" class="nav-item">
                <i class="fas fa-home"></i> Beranda
            </a>
            <a href="login.php" class="nav-item">
                <i class="fas fa-sign-in-alt"></i> Login
            </a>
            <a href="register.php" class="nav-item active">
                <i class="fas fa-user-plus"></i> Daftar
            </a>
        </nav>
    </div>
</div>

<div class="main-content">
    <div class="card">
        <div class="card-header">
            <div class="card-icon">
                <i class="fas fa-user-plus"></i>
            </div>
            <div class="card-title">Daftar Akun Baru</div>
        </div>

        <?php if (!empty($errors)): ?>
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>Perhatian!</strong>
                <ul class="mt-2 mb-0">
                    <?php foreach ($errors as $error): ?>
                        <li><?= $error ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>
        <?php endif; ?>

        <div class="info-box">
            <h6><i class="fas fa-info-circle"></i> Informasi Pendaftaran</h6>
            <ul>
                <li>Setelah registrasi, Anda dapat login dan mendaftar AK1</li>
                <li>Pastikan email aktif untuk notifikasi</li>
                <li>Password minimal 6 karakter</li>
            </ul>
        </div>

        <form method="POST" id="registerForm">
            <div class="form-group">
                <label class="form-label">
                    <i class="fas fa-user me-2"></i>Nama Lengkap
                </label>
                <input type="text" name="nama_lengkap" class="form-control" required 
                       value="<?= $_POST['nama_lengkap'] ?? '' ?>"
                       placeholder="Masukkan nama lengkap Anda">
            </div>

            <div class="form-group">
                <label class="form-label">
                    <i class="fas fa-envelope me-2"></i>Email
                </label>
                <input type="email" name="email" class="form-control" required
                       value="<?= $_POST['email'] ?? '' ?>"
                       placeholder="contoh@email.com">
                <div class="form-text">Gunakan email aktif untuk verifikasi</div>
            </div>

            <div class="form-group">
                <label class="form-label">
                    <i class="fas fa-phone me-2"></i>No. Telepon
                </label>
                <input type="tel" name="no_telepon" class="form-control"
                       value="<?= $_POST['no_telepon'] ?? '' ?>"
                       placeholder="081234567890">
                <div class="form-text">Format: 08xxxxxxxxxx</div>
            </div>

            <div class="form-group">
                <label class="form-label">
                    <i class="fas fa-lock me-2"></i>Password
                </label>
                <input type="password" name="password" class="form-control" required minlength="6"
                       placeholder="Minimal 6 karakter">
                <div class="form-text">Password minimal 6 karakter</div>
            </div>

            <div class="form-group">
                <label class="form-label">
                    <i class="fas fa-lock me-2"></i>Konfirmasi Password
                </label>
                <input type="password" name="password_confirm" class="form-control" required
                       placeholder="Ketik ulang password">
            </div>

            <button type="submit" class="btn btn-primary">
                <i class="fas fa-user-plus me-2"></i>Daftar Sekarang
            </button>
        </form>

        <div class="text-center mt-4">
            <p class="mb-3">Sudah punya akun?</p>
            <a href="login.php" class="btn btn-outline">
                <i class="fas fa-sign-in-alt me-2"></i>Login ke Akun
            </a>
        </div>
    </div>
</div>

<script>
    // Animasi seperti di dashboard
    document.addEventListener('DOMContentLoaded', function() {
        const card = document.querySelector('.card');
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200);

        // Focus pada input nama
        const namaInput = document.querySelector('input[name="nama_lengkap"]');
        if (namaInput) {
            namaInput.focus();
        }

        // Validasi password match
        const form = document.getElementById('registerForm');
        const password = document.querySelector('input[name="password"]');
        const passwordConfirm = document.querySelector('input[name="password_confirm"]');

        form.addEventListener('submit', function(e) {
            if (password.value !== passwordConfirm.value) {
                e.preventDefault();
                alert('Konfirmasi password tidak sesuai!');
                passwordConfirm.focus();
            }
        });

        // Real-time password match indicator
        passwordConfirm.addEventListener('input', function() {
            if (password.value !== passwordConfirm.value) {
                passwordConfirm.style.borderColor = '#e74c3c';
            } else {
                passwordConfirm.style.borderColor = '#2ecc71';
            }
        });
    });
</script>

</body>
</html>