<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>

<h1>Test 1: Include Files</h1>

<?php
// Test include header.php
echo "Testing header.php...<br>";
ob_start();
include 'includes/header.php';
$header_content = ob_get_clean();
echo "Header loaded: " . (strlen($header_content) > 0 ? "✅" : "❌") . "<br>";

// Test simple content
echo "<div class='alert alert-success'>CONTENT AREA</div>";

// Test include footer.php  
echo "Testing footer.php...<br>";
ob_start();
include 'includes/footer.php';
$footer_content = ob_get_clean();
echo "Footer loaded: " . (strlen($footer_content) > 0 ? "✅" : "❌") . "<br>";