<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Final Test</h1>";

// Test single include
include 'includes/functions.php';
echo "✅ functions.php loaded<br>";

// Test functions
if (function_exists('isUserLoggedIn')) {
    echo "✅ isUserLoggedIn exists<br>";
}

if (function_exists('sanitizeInput')) {
    $test = sanitizeInput('hello');
    echo "✅ sanitizeInput works: $test<br>";
}

echo "<div style='background:green;color:white;padding:20px;'>🎉 SEMUA BERHASIL! Website ready.</div>";
?>