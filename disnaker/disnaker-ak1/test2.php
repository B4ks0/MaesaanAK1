<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>

<h1>Test 2: Autoload Issue</h1>

<?php
// Test tanpa autoload dulu
echo "Testing manual include...<br>";

if (file_exists('config/database.php')) {
    include 'config/database.php';
    echo "✅ database.php included<br>";
    
    // Test Database class
    if (class_exists('Database')) {
        echo "✅ Database class exists<br>";
        try {
            $pdo = Database::getInstance()->getConnection();
            echo "✅ Database connected<br>";
        } catch (Exception $e) {
            echo "❌ Database error: " . $e->getMessage() . "<br>";
        }
    } else {
        echo "❌ Database class not found<br>";
    }
} else {
    echo "❌ database.php not found<br>";
}