<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'database.php';
include __DIR__ . '/../includes/functions.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
