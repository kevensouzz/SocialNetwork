<?php
require_once '../../../../middleware.php';
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TalkChain - Login</title>
  <link rel="icon" type="image/x-icon" href="../../assets/favicon.ico">
  <link rel="stylesheet" href="../../assets/main.css">
  <link rel="stylesheet" href="login.css">
</head>

<body>
  <?php include '../../../components/header.php'; ?>
  <main id="main">
    <img src="../../assets/storyset/Login-amico.svg" alt="Signin image">

    <form>
      <div class="text">
        <h1>Sign in</h1>
        <h2>Welcome to <span>TalkChain</span>!</h2>
      </div>

      <div class="fields">
        <span class="field">
          <label for="username">Username</label>
          <input type="text" placeholder="Type your username here." name="username" id="username">
        </span>

        <span class="field">
          <label for="password">Password</label>
          <input type="password" placeholder="Type your password here." name="password" id="password">
        </span>

        <button type="submit" class="submit-btn">Login</button>
      </div>

      <p class="links">
        <a href="/auth/register">I don't have an account</a> or <a href="/auth/reset">I forgot my password</a>
      </p>
    </form>
  </main>
</body>

</html>