<?php
/**
 * Validator Class - SonarQube Compliant
 */

namespace Disnaker;

class Validator {
    public static function sanitize($data) {
        if (is_array($data)) {
            return array_map([self::class, 'sanitize'], $data);
        }
        return htmlspecialchars(strip_tags(trim($data)), ENT_QUOTES, 'UTF-8');
    }
    
    public static function validateEmail(string $email): bool {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }
    
    public static function validateNIK(string $nik): bool {
        return preg_match('/^\d{16}$/', $nik);
    }
    
    public static function validatePhone(string $phone): bool {
        $cleanPhone = preg_replace('/[^\d]/', '', $phone);
        return preg_match('/^08[1-9]\d{7,10}$/', $cleanPhone);
    }
    
    public static function validateRequired(array $data, array $fields): array {
        $errors = [];
        
        foreach ($fields as $field) {
            if (empty(trim($data[$field] ?? ''))) {
                $errors[] = "Field {$field} harus diisi.";
            }
        }
        
        return $errors;
    }
    
    public static function validatePassword(string $password, string $confirmPassword): array {
        $errors = [];
        
        if (strlen($password) < 6) {
            $errors[] = "Password minimal 6 karakter.";
        }
        
        if ($password !== $confirmPassword) {
            $errors[] = "Konfirmasi password tidak sesuai.";
        }
        
        return $errors;
    }
}
