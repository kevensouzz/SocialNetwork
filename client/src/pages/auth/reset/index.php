<?php
require_once '../../../../middleware.php';
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TalkChain - Recovery Password</title>
  <link rel="icon" type="image/x-icon" href="../../assets/favicon.ico">
  <link rel="stylesheet" href="../../assets/main.css">
  <link rel="stylesheet" href="forgot.css">
</head>

<body>
  <?php include '../../../components/header.php'; ?>
  <main id="main">
    <img draggable="false" src="../../assets/storyset/Reset password-pana.svg" alt="Reset password image.">

    <form>
      <div class="text">
        <h2>Lets <span>recovery</span> your password!</h2>

        <p>We'll send you an email with a code to <span>change your password</span>.</p>
      </div>

      <div class="fields">
        <span class="field">
          <label for="email">Email</label>
          <input type="email" placeholder="Your accounts email." name="email" id="email">
        </span>

        <button type="submit" class="submit-btn">Enviar</button>
      </div>

      <div class="links">
        Back to <a href="/auth/login">Login</a> or <a href="/auth/register">Register</a>
      </div>
    </form>
  </main>
</body>

</html>