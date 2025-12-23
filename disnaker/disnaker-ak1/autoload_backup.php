<?php
/**
 * Simple Autoloader untuk Disnaker AK1
 * SonarQube Compliant - menggunakan use statements
 */

spl_autoload_register(function ($className) {
    // Handle Disnaker namespace
    if (strpos($className, 'Disnaker\\') === 0) {
        $simpleName = str_replace('Disnaker\\', '', $className);
        $paths = [
            'Database' => 'config/database.php',
            'Auth' => 'includes/auth.php',
            'Validator' => 'includes/validator.php',
            'Utilities' => 'includes/functions.php'
        ];

        if (isset($paths[$simpleName]) && file_exists(__DIR__ . '/' . $paths[$simpleName])) {
            require_once __DIR__ . '/' . $paths[$simpleName];
            return true;
        }
    }

    // Convert namespace ke path file
    $filePath = __DIR__ . '/' . str_replace('\\', '/', $className) . '.php';

    if (file_exists($filePath)) {
        require_once $filePath;
        return true;
    }

    return false;
});

// Include file konfigurasi essential
require_once 'config/database.php';
