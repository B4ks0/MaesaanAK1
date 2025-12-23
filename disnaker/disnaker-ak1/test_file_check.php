<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>File Check</h1>";

$files = [
    'includes/functions_simple.php',
    'includes/functions_backup.php',
    'includes/functions.php',
    'config/database.php'
];

foreach ($files as $file) {
    $fullPath = __DIR__ . '/' . $file;
    echo "Checking: $file<br>";
    echo "Full path: $fullPath<br>";
    
    if (file_exists($file)) {
        echo "✅ File EXISTS<br>";
        echo "Size: " . filesize($file) . " bytes<br>";
        
        // Try to read content
        $content = file_get_contents($file);
        echo "Content length: " . strlen($content) . " characters<br>";
    } else {
        echo "❌ File NOT FOUND<br>";
    }
    echo "<hr>";
}
