// ROCOCO JOURNAL — main.js

document.addEventListener('DOMContentLoaded', function () {

  // 모바일 메뉴 토글
  const toggle = document.getElementById('navToggle');
  const gnb = document.getElementById('gnb');
  const overlay = document.getElementById('gnbOverlay');

  function closeMenu() {
    gnb.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    toggle.setAttribute('aria-label', '메뉴 열기');
    document.body.style.overflow = '';
  }

  if (toggle && gnb) {
    toggle.addEventListener('click', function () {
      const isOpen = gnb.classList.toggle('open');
      if (overlay) overlay.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-label', isOpen ? '메뉴 닫기' : '메뉴 열기');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    if (overlay) overlay.addEventListener('click', closeMenu);
  }

  // 모바일 서브메뉴 토글 (클릭해서 열고 닫기)
  const hasSubItems = document.querySelectorAll('.has-sub > a');
  hasSubItems.forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        const sub = this.nextElementSibling;
        if (sub) sub.classList.toggle('open');
      }
    });
  });

  // 스크롤 시 헤더 스타일 변경
  const header = document.getElementById('header');
  window.addEventListener('scroll', function () {
    if (window.scrollY > 20) {
      header.style.boxShadow = '0 2px 20px rgba(0,0,0,0.06)';
    } else {
      header.style.boxShadow = 'none';
    }
  });

  // 본문 이미지 클릭 시 원본 크기로 펼치기/접기
  const articleImgs = document.querySelectorAll('.article-content img');
  articleImgs.forEach(function (img) {
    img.addEventListener('click', function () {
      img.classList.toggle('expanded');
    });
  });

  // 이미지 lazy load fallback
  const imgs = document.querySelectorAll('img[loading="lazy"]');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
          }
          observer.unobserve(img);
        }
      });
    });
    imgs.forEach(function (img) { observer.observe(img); });
  }

});
