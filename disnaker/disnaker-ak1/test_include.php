
<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Test Include</h1>";

// Method 1: Relative path
echo "Method 1: Relative path...<br>";
if (file_exists('includes/functions_simple.php')) {
    include 'includes/functions_simple.php';
    echo "✅ Relative include SUCCESS<br>";
} else {
    echo "❌ Relative include FAILED<br>";
}

// Method 2: Absolute path  
echo "<br>Method 2: Absolute path...<br>";
$absolutePath = __DIR__ . '/includes/functions_simple.php';
if (file_exists($absolutePath)) {
    include $absolutePath;
    echo "✅ Absolute include SUCCESS<br>";
} else {
    echo "❌ Absolute include FAILED<br>";
}

// Test function
echo "<br>Testing function...<br>";
if (function_exists('sanitizeInput')) {
    $result = sanitizeInput('test');
    echo "✅ sanitizeInput works: $result<br>";
} else {
    echo "❌ sanitizeInput not found<br>";
}

echo "<div style='background:green;color:white;padding:20px;'>TEST COMPLETE</div>";
?>