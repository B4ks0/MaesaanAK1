<?php
/**
 * Utility Functions - FINAL VERSION
 * SonarQube Compliant
 */

// Function existence checks untuk prevent duplicate declaration
if (!function_exists('isUserLoggedIn')) {
    function isUserLoggedIn() {
        return isset($_SESSION['user_id']) && !empty($_SESSION['user_id']);
    }
}

if (!function_exists('sanitizeInput')) {
    function sanitizeInput($data) {
        if (is_array($data)) {
            return array_map('sanitizeInput', $data);
        }
        return htmlspecialchars(strip_tags(trim($data)), ENT_QUOTES, 'UTF-8');
    }
}

if (!function_exists('redirect')) {
    function redirect($url) {
        if (!headers_sent()) {
            header("Location: $url");
            exit();
        }
        echo "<script>window.location.href='$url';</script>";
        exit();
    }
}

if (!function_exists('validateEmail')) {
    function validateEmail($email) {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }
}

if (!function_exists('validatePhone')) {
    function validatePhone($phone) {
        $cleanPhone = preg_replace('/[^\d]/', '', $phone);
        return preg_match('/^08[1-9]\d{7,10}$/', $cleanPhone);
    }
}
?>