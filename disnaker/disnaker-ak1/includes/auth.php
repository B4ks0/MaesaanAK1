<?php
/**
 * Auth Class - SonarQube Compliant
 */

namespace Disnaker;

class Auth {
    public static function startSession(): void {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
    }
    
    public static function isUserLoggedIn(): bool {
        self::startSession();
        return isset($_SESSION['user_id']) && !empty($_SESSION['user_id']);
    }
    
    public static function isAdminLoggedIn(): bool {
        self::startSession();
        return isset($_SESSION['admin_id']) && !empty($_SESSION['admin_id']);
    }
    
    public static function loginUser(int $userId, string $userName, string $userEmail): void {
        self::startSession();
        $_SESSION['user_id'] = $userId;
        $_SESSION['user_name'] = $userName;
        $_SESSION['user_email'] = $userEmail;
    }
    
    public static function loginAdmin(int $adminId, string $adminName, string $role): void {
        self::startSession();
        $_SESSION['admin_id'] = $adminId;
        $_SESSION['admin_name'] = $adminName;
        $_SESSION['admin_role'] = $role;
    }
    
    public static function logout(): void {
        self::startSession();
        session_destroy();
        session_start(); // Start new session for flash messages
    }
    
    public static function redirect(string $url): void {
        if (!headers_sent()) {
            header("Location: " . $url);
            exit();
        }
        echo "<script>window.location.href='{$url}';</script>";
        exit();
    }
    
    public static function setFlashMessage(string $type, string $message): void {
        self::startSession();
        $_SESSION['flash'] = compact('type', 'message');
    }
    
    public static function getFlashMessage(): ?array {
        self::startSession();
        $flash = $_SESSION['flash'] ?? null;
        unset($_SESSION['flash']);
        return $flash;
    }
}
