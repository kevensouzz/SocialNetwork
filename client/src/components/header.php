<?php
function getCleanPath($path)
{
  return rtrim(parse_url($path, PHP_URL_PATH), '/');
}

$currentPath = getCleanPath($_SERVER['REQUEST_URI']);
?>

<header id="header">
  <?php
  include('banner.php');
  ?>

  <nav id="navbar">
    <a href="/home" class="<?= $currentPath == '/home' ? 'active' : '' ?>">Home</a>
    <a href="/politics" class="<?= $currentPath == '/politics' ? 'active' : '' ?>">Politics</a>
    <a href="/auth" class="<?= $currentPath == '/auth/register' || $currentPath == '/auth/login' || $currentPath == '/auth/reset' ? 'active' : '' ?>">Auth</a>
  </nav>

  <button id="btn-open-mobile-navbar">
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0000C8"
      stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-align-center">
      <line x1="21" x2="3" y1="6" y2="6" />
      <line x1="17" x2="7" y1="12" y2="12" />
      <line x1="19" x2="5" y1="18" y2="18" />
    </svg>
  </button>
</header>

<span class="header-division-line">
  <span></span>
</span>

<nav id="mobile-navbar">
  <header id="mobile-navbar-header">
    <?php
    include('banner.php')
    ?>

    <button id="btn-close-mobile-navbar">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0000c8"
        stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x">
        <path d="M18 6 6 18" />
        <path d="m6 6 12 12" />
      </svg>
    </button>
  </header>

  <span class="mobile-header-division-line">
    <span></span>
  </span>

  <main>
    <span id="mobile-navbar-content">
      <a href="/home" class="<?= $currentPath == '/home' ? 'active' : '' ?>">Home</a>
      <a href="/politics" class="<?= $currentPath == '/politics' ? 'active' : '' ?>">Politics</a>
      <a href="/auth" class="<?= $currentPath == '/auth/register' || $currentPath == '/auth/login' || $currentPath == '/auth/reset' ? 'active' : '' ?>">Auth</a>
    </span>
  </main>
</nav>

<script>
  const btnOpenMobileNavbar = document.getElementById('btn-open-mobile-navbar');
  const btnCloseMobileNavbar = document.getElementById('btn-close-mobile-navbar');
  const mobileNavbar = document.getElementById('mobile-navbar');
  const headerBanner = document.querySelector('#header .banner');
  const headerDivisionLine = document.querySelector('.header-division-line');
  const body = document.body;

  btnOpenMobileNavbar.addEventListener('click', function() {
    if (mobileNavbar.style.display === 'none' || mobileNavbar.style.display === '') {
      mobileNavbar.style.display = 'flex';
      body.classList.add('no-scroll');
      btnOpenMobileNavbar.style.display = 'none';
      headerBanner.style.display = 'none';
      headerDivisionLine.style.display = 'none';
    }
  });

  btnCloseMobileNavbar.addEventListener('click', function() {
    if (mobileNavbar.style.display === 'flex') {
      btnOpenMobileNavbar.style.display = 'flex';
      headerDivisionLine.style.display = 'flex';
      headerBanner.style.display = 'block';
      body.classList.remove('no-scroll');
      mobileNavbar.style.display = 'none';
    }
  })
</script>