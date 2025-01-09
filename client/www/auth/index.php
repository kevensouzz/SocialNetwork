<?php
require_once '../../jwt.php';
require '../../vendor/autoload.php';

use Dotenv\dotenv;

$dotenv = Dotenv::createImmutable(__DIR__ . '/../../');
$dotenv->load();

if (isset($_COOKIE['JWT'])) {
  $jwtToken = $_COOKIE['JWT'];
  $secretKey = $_ENV['JWT_SECRET_KEY'];

  $decoded = verifyJWT($jwtToken, $secretKey);

  if ($decoded) {
    header('Location: /app');
    exit();
  }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TalkChain - Auth</title>
  <link rel="stylesheet" href="../assets/css/main.css">
  <link rel="stylesheet" href="auth.css">
</head>

<body>
  <?php include '../../components/header.php'; ?>
  <main id="main"></main>
  <?php include '../../components/footer.php'; ?>
</body>

</html>