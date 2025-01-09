<?php
require_once '../../jwt.php';
require '../../vendor/autoload.php';

use Dotenv\dotenv;

$dotenv = Dotenv::createImmutable(__DIR__ . '/../../');
$dotenv->load();

$jwtSub;

if (isset($_COOKIE['JWT'])) {
  $jwtToken = $_COOKIE['JWT'];
  $secretKey = $_ENV['JWT_SECRET_KEY'];

  $decoded = verifyJWT($jwtToken, $secretKey);

  if ($decoded) {
    $jwtSub = $decoded->sub;
  } else {
    setcookie('JWT', '', time() - 3600, '/');
    header('Location: /auth');
    exit();
  }
} else {
  header('Location: /auth');
  exit;
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TalkChain - Dashboard</title>
  <link rel="stylesheet" href="app.css">
</head>

<body>
</body>

</html>