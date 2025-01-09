<?php
require 'vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\key;

function verifyJWT($token, $secretKey) {
    try {
        $decoded = JWT::decode($token, new Key($secretKey, 'HS256'));

        if (isset($decoded->exp) && $decoded->exp < time()) {
            return false;
        }

        return $decoded;
    } catch (Exception $e) {
        return false;
    }
}