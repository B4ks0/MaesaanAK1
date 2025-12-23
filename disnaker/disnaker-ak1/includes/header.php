<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Manual include tanpa autoload
include 'config/database.php';
include 'includes/functions.php';

// Start session manual
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>

<?php include 'includes/header.php'; ?>

<div class="container mt-5">
    <div class="row">
        <div class="col-md-8 mx-auto text-center">
            <h1 class="text-primary">DISNAKER AK1</h1>
            <p class="lead">Sistem Kartu Pencari Kerja Digital</p>
            
            <div class="card mt-4">
                <div class="card-body">
                    <h5 class="card-title">Selamat Datang</h5>
                    <p class="card-text">
                        Layanan pendaftaran kartu AK1 secara online. 
                        Daftar sekarang untuk mendapatkan kartu digital.
                    </p>
                    
                    <div class="d-grid gap-2 d-md-block">
                        <a href="register.php" class="btn btn-primary btn-lg me-2">
                            <i class="fas fa-user-plus"></i> Daftar
                        </a>
                        <a href="login.php" class="btn btn-secondary btn-lg">
                            <i class="fas fa-sign-in-alt"></i> Login
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include 'includes/footer.php'; ?>