<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Start session
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Clear all session data
session_destroy();

// Start new session for potential messages
session_start();
$_SESSION['success'] = "Logout berhasil!";

// Redirect to login
header("Location: login.php");
exit();
