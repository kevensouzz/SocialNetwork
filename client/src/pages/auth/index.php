<?php
// require_once '../../../middleware.php';
// require_once '../../../jwt.php';

// use Dotenv\dotenv;

// $dotenv = Dotenv::createImmutable(__DIR__ . '/../../../');
// $dotenv->load();

// if (isset($_COOKIE['JWT'])) {
//   $jwtToken = $_COOKIE['JWT'];
//   $secretKey = $_ENV['JWT_SECRET_KEY'];

//   $decoded = verifyJWT($jwtToken, $secretKey);

//   if ($decoded) {
//     header('Location: /app');
//     exit();
//   }
// }

header('Location: /auth/login');
exit();
