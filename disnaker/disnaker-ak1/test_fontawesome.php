<!DOCTYPE html>
<html>
<head>
    <title>Test Font Awesome</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .icon-test { 
            font-size: 2rem; 
            margin: 10px; 
            padding: 20px;
            border: 2px solid #333;
            display: inline-block;
        }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Test Font Awesome Icons</h1>
    
    <div class="icon-test">
        <i class="fas fa-user"></i> User Icon
    </div>
    
    <div class="icon-test">
        <i class="fas fa-id-card"></i> ID Card Icon
    </div>
    
    <div class="icon-test">
        <i class="fas fa-briefcase"></i> Briefcase Icon
    </div>
    
    <div class="icon-test success">
        <i class="fas fa-check-circle"></i> Success Icon
    </div>
    
    <div class="icon-test error">
        <i class="fas fa-times-circle"></i> Error Icon
    </div>
    
    <h2>Jika icon muncul, Font Awesome berhasil loading!</h2>
</body>
</html>