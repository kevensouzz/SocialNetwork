<?php
require_once '../../../../middleware.php';
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TalkChain - Auth</title>
  <link rel="icon" type="image/x-icon" href="../../assets/favicon.ico">
  <link rel="stylesheet" href="../../assets/main.css">
  <link rel="stylesheet" href="register.css">
</head>

<body>
  <?php include '../../../components/header.php'; ?>
  <main id="main">
    <img draggable="false" src="../../assets/storyset/Sign up-cuate.svg" alt="Signup image">

    <form>
      <div class="text">
        <h1>Sign up</h1>
        <h2>Welcome to <span>TalkChain</span>!</h2>
      </div>

      <div class="fields">
        <span class="field">
          <label for="username">Username</label>
          <input type="text" placeholder="Only numbers and lower case letters. (3-16)" name="username" id="username">
        </span>

        <span class="field">
          <label for="email">Email</label>
          <input type="email" placeholder="An valid email." name="email" id="email">
        </span>

        <span class="field">
          <label for="password">Password</label>
          <input type="password" placeholder="Upper and lower case letters, numbers and special characters. (+8)" name="password" id="password">
        </span>

        <span class="field">
          <label for="password">Confirm Password</label>
          <input type="password" placeholder="Confirm the password assigned above." name="confirmPassword" id="confirmPassword">
        </span>

        <button type="submit" class="submit-btn">Register</button>
      </div>

      <a href="/auth/login">I already have an account</a>
    </form>
  </main>
</body>

</html>