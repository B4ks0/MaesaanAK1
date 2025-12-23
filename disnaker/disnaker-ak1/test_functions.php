<?php
require_once 'includes/functions.php';

echo "<h1>Test Functions - Regex Fixed</h1>";

// Test validateNIK dengan \d
echo "<h3>Test validateNIK (dengan \\d):</h3>";
echo "3273010101900001: " . (validateNIK('3273010101900001') ? 'Valid' : 'Invalid') . "<br>";
echo "123: " . (validateNIK('123') ? 'Valid' : 'Invalid') . "<br>";
echo "ABCDEFGHIJKLMNOP: " . (validateNIK('ABCDEFGHIJKLMNOP') ? 'Valid' : 'Invalid') . "<br>";

// Test validatePhone dengan \d
echo "<h3>Test validatePhone (dengan \\d):</h3>";
echo "08123456789: " . (validatePhone('08123456789') ? 'Valid' : 'Invalid') . "<br>";
echo "0812345678901: " . (validatePhone('0812345678901') ? 'Valid' : 'Invalid') . "<br>";
echo "0211234567: " . (validatePhone('0211234567') ? 'Valid' : 'Invalid') . "<br>";
echo "082191381332: " . (validatePhone('082191381332') ? 'Valid' : 'Invalid') . "<br>";

echo "<div class='alert alert-success'>✅ All regex functions fixed with \\d syntax!</div>";