<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Test Database</h1>";

// Test include database
include 'config/database.php';
echo "✅ Database included<br>";

// Test connection
try {
    $pdo = Database::getInstance()->getConnection();
    echo "✅ Database connected<br>";
} catch (Exception $e) {
    echo "❌ Database error: " . $e->getMessage() . "<br>";
}

// Test functions
include 'includes/functions.php';
echo "✅ Functions included<br>";

echo "<div style='background:green;color:white;padding:10px;'>SUCCESS!</div>";
