<?php
function getCleanPath($path)
{
  return rtrim(parse_url($path, PHP_URL_PATH), '/');
}

$currentPath = getCleanPath($_SERVER['REQUEST_URI']);
?>

<header id="header">
  <a id="banner" href="/home"><span>T</span>alk<span>C</span>hain</a>

  <nav id="navbar">
    <a href="/home" class="<?= $currentPath == '/home' ? 'active' : '' ?>">Home</a>
    <a href="/politics" class="<?= $currentPath == '/politics' ? 'active' : '' ?>">Politics</a>
    <a href="/auth" class="<?= $currentPath == '/auth/register' || $currentPath == '/auth/login' || $currentPath == '/auth/reset' ? 'active' : '' ?>">Auth</a>
  </nav>
</header>

<span class="header-division-line">
  <span></span>
</span>