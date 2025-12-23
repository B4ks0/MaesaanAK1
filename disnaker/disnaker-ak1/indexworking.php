<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Manual include tanpa autoload
include 'config/database.php';
?>

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DISNAKER AK1 - WORKING</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="index_working.php">
                <i class="fas fa-briefcase"></i> DISNAKER AK1
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="alert alert-success">
            <h4>✅ Website Berhasil Load!</h4>
            <p>Ini versi sederhana tanpa autoload complex.</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Menu</h5>
                        <a href="register.php" class="btn btn-primary">Register</a>
                        <a href="login.php" class="btn btn-secondary">Login</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>