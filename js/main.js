// ROCOCO JOURNAL — main.js

document.addEventListener('DOMContentLoaded', function () {

  // 모바일 메뉴 토글
  const toggle = document.getElementById('navToggle');
  const gnb = document.getElementById('gnb');
  const overlay = document.getElementById('gnbOverlay');
  const closeBtn = document.getElementById('gnbClose');

  function openMenu() {
    gnb.classList.add('open');
    if (overlay) overlay.classList.add('open');
    toggle.setAttribute('aria-label', '메뉴 닫기');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    gnb.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    toggle.setAttribute('aria-label', '메뉴 열기');
    document.body.style.overflow = '';
  }

  if (toggle && gnb) {
    toggle.addEventListener('click', function () {
      gnb.classList.contains('open') ? closeMenu() : openMenu();
    });
  }
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (overlay) overlay.addEventListener('click', closeMenu);

  // 모바일 서브메뉴 토글 (화살표 회전 + max-height 슬라이드)
  const hasSubItems = document.querySelectorAll('.has-sub > a');
  hasSubItems.forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        const li = this.parentElement;
        const sub = this.nextElementSibling;
        const isOpen = li.classList.contains('sub-open');
        // 다른 열린 서브메뉴 닫기
        document.querySelectorAll('.has-sub.sub-open').forEach(function (el) {
          el.classList.remove('sub-open');
          const s = el.querySelector('.sub-menu');
          if (s) s.classList.remove('open');
        });
        if (!isOpen) {
          li.classList.add('sub-open');
          if (sub) sub.classList.add('open');
        }
      }
    });
  });

  // 스크롤 시 헤더 그림자
  const header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', function () {
      header.style.boxShadow = window.scrollY > 20
        ? '0 2px 20px rgba(0,0,0,0.06)' : 'none';
    });
  }

  // 본문 이미지 클릭 시 원본 크기로 펼치기/접기
  document.querySelectorAll('.article-content img').forEach(function (img) {
    img.addEventListener('click', function () {
      img.classList.toggle('expanded');
    });
  });

  // 이미지 lazy load fallback
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) img.src = img.dataset.src;
          observer.unobserve(img);
        }
      });
    });
    document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
      observer.observe(img);
    });
  }

});
