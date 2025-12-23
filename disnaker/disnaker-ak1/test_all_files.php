<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Check All Files</h1>";

$files = [
    'index.php',
    'register.php', 
    'login.php',
    'config/database.php',
    'includes/functions.php',
    'includes/header.php',
    'includes/footer.php'
];

foreach ($files as $file) {
    echo "📁 $file: ";
    if (file_exists($file)) {
        $size = filesize($file);
        $lines = count(file($file));
        echo "✅ EXISTS (Size: {$size} bytes, Lines: {$lines})";
    } else {
        echo "❌ NOT FOUND";
    }
    echo "<br>";
}

echo "<hr><h3>Functions Check:</h3>";
if (file_exists('includes/functions.php')) {
    include 'includes/functions.php';
    
    $functions = [
        'isUserLoggedIn',
        'sanitizeInput', 
        'redirect',
        'validateEmail',
        'validatePhone'
    ];
    
    foreach ($functions as $func) {
        echo "🔧 $func(): " . (function_exists($func) ? '✅ EXISTS' : '❌ MISSING') . "<br>";
    }
} else {
    echo "❌ functions.php not found";
}
