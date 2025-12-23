<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>
<h1>EMERGENCY FIX - Memory Error</h1>
<p>Terjadi infinite loop. Mari kita reset.</p>

<?php
// List semua file dan cari yang bermasalah
$files = [
    'index.php',
    'includes/header.php',
    'includes/footer.php', 
    'includes/functions.php',
    'config/database.php',
    'autoload.php'
];

foreach ($files as $file) {
    if (file_exists($file)) {
        echo "📁 $file - EXISTS<br>";
        
        // Check file size
        $size = filesize($file);
        echo "&nbsp;&nbsp;Size: " . $size . " bytes<br>";
        
        // Check for recursive includes
        $content = file_get_contents($file);
        if (strpos($content, 'include') !== false || strpos($content, 'require') !== false) {
            echo "&nbsp;&nbsp;⚠️ Contains include/require<br>";
        }
    } else {
        echo "📁 $file - NOT FOUND<br>";
    }
}
?>

<hr>
<h3>SOLUSI:</h3>
<ol>
<li>Rename <code>includes/functions.php</code> ke <code>includes/functions_backup.php</code></li>
<li>Buat <code>includes/functions_simple.php</code> yang baru</li>
<li>Test dengan file sederhana</li>
</ol>