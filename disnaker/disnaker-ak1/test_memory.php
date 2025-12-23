<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Memory Test</h1>";
echo "Memory usage: " . memory_get_usage() . " bytes<br>";
echo "Memory peak: " . memory_get_peak_usage() . " bytes<br>";

// Test include functions_simple
include 'includes/functions_simple.php';
echo "✅ functions_simple.php loaded<br>";

// Test function
$test = sanitizeInput("hello");
echo "✅ sanitizeInput working: $test<br>";

echo "<div style='background:green;color:white;padding:20px;'>SUCCESS! No memory issues.</div>";
?>