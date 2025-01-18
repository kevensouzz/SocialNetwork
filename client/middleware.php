<?php
require 'vendor/autoload.php';
require_once 'jwt.php';

use Dotenv\Dotenv;

$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

$jwtSub;

$currentRoute = $_SERVER['REQUEST_URI'];

if (preg_match('/\/auth\/(login|register|reset)/', $currentRoute)) {
  if (isset($_COOKIE['JWT'])) {
    $jwtToken = $_COOKIE['JWT'];
    $secretKey = $_ENV['JWT_SECRET_KEY'];

    $decoded = verifyJWT($jwtToken, $secretKey);

    if ($decoded) {
      header('Location: /app/');
      exit();
    }
  }
} else {
  if (isset($_COOKIE['JWT'])) {
    $jwtToken = $_COOKIE['JWT'];
    $secretKey = $_ENV['JWT_SECRET_KEY'];

    $decoded = verifyJWT($jwtToken, $secretKey);

    if ($decoded) {
      $jwtSub = $decoded->sub;
    } else {
      setcookie('JWT', '', time() - 3600, '/');
      header('Location: /auth/login/');
      exit();
    }
  } else {
    header('Location: /auth/login/');
    exit;
  }
}
