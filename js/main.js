// ROCOCO JOURNAL — main.js

document.addEventListener('DOMContentLoaded', function () {

  // 헤더 정리 (페이지마다 헤더 HTML이 따로라 여기서 한 번에 처리 — 구조가 다르면 아무것도 안 함)
  // ① 수술후기+전후사진 → '후기·전후사진' 한 칸 ② 성형 가이드는 금색 강조(전후사진 버튼 자리)
  // ③ 로고 'Journal' 제거 ④ 언어 버튼 → 지구본 아이콘 + KO. 시술 분류(광대·코…)는 그대로 노출.
  (function () {
    var ul = document.querySelector('#gnb > ul');
    if (!ul) return;
    var items = [].slice.call(ul.children);
    function norm(h) { return (h || '').replace(/^(\.\.\/|\.\/|\/)+/, ''); }
    function first(li) { return li.querySelector(':scope > a'); }
    function find(path) {
      return items.filter(function (li) { var a = first(li); return a && norm(a.getAttribute('href')) === path; })[0];
    }
    var guide = find('guide/');
    var reviews = items.filter(function (li) { return li.querySelector(':scope > a.btn-gold-outline'); })[0];
    var cases = items.filter(function (li) { return li.querySelector(':scope > a.btn-gold'); })[0];
    var about = find('about/');
    if (guide && reviews && cases && about) {
      var proof = document.createElement('li');
      proof.className = 'has-sub gnb-proof';
      var pa = document.createElement('a');
      pa.href = '#';
      pa.textContent = '후기·전후사진';
      // 이 칸 자체는 이동하지 않는 묶음 메뉴 (모바일은 아래 공통 핸들러, 데스크톱 터치는 여기서 토글)
      pa.addEventListener('click', function (e) {
        e.preventDefault();
        if (window.innerWidth > 768) proof.classList.toggle('hover-open');
      });
      proof.appendChild(pa);
      var proofSub = document.createElement('ul');
      proofSub.className = 'sub-menu';
      [reviews, cases].forEach(function (li) {
        first(li).className = '';
        proofSub.appendChild(li);
      });
      proof.appendChild(proofSub);

      first(guide).className = 'btn-gold';
      guide.className = 'gnb-guide';
      ul.insertBefore(proof, about);
    }
    document.getElementById('gnb').classList.add('nav-ready');

    var logoSub = document.querySelector('.logo .logo-sub');
    if (logoSub && logoSub.textContent.trim() === 'Journal') logoSub.remove();

    var langBtn = document.getElementById('langBtn');
    if (langBtn) {
      var code = (document.documentElement.lang || 'ko').slice(0, 2).toUpperCase();
      langBtn.classList.add('lang-btn--globe');
      langBtn.setAttribute('aria-label', 'Language');
      langBtn.innerHTML = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.7 3.9 5.7 3.9 9s-1.3 6.3-3.9 9c-2.6-2.7-3.9-5.7-3.9-9S9.4 5.7 12 3z"/></svg><span>' + code + '</span>';
    }
  })();

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
        // 같은 단계의 다른 열린 서브메뉴 닫기 (바깥 묶음 메뉴는 그대로 둠)
        li.parentElement.querySelectorAll(':scope > .has-sub.sub-open').forEach(function (el) {
          el.classList.remove('sub-open');
          const s = el.querySelector(':scope > .sub-menu');
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

  // 스크롤 리빌 — .reveal/.reveal-left/.reveal-right 요소가 화면에 들어오면 나타남
  const revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if (revealEls.length) {
    if ('IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
      revealEls.forEach(function (el) { revealObserver.observe(el); });
    } else {
      revealEls.forEach(function (el) { el.classList.add('is-visible'); });
    }
  }

  // 헤더 회원 메뉴: 로그인 전 "로그인"(회원가입은 로그인 페이지 안), 로그인 후 "이름님 · 로그아웃"
  // (페이지마다 헤더 HTML이 따로라 1400여 개를 고치는 대신 여기서 한 번에 붙임)
  (function () {
    var list = document.querySelector('#gnb > ul');
    if (!list) return;
    // 이 스크립트 경로에서 사이트 루트까지의 상대 경로를 구함 (페이지 깊이와 무관)
    var scriptEl = document.querySelector('script[src$="js/main.js"]');
    if (!scriptEl) return;
    var root = scriptEl.getAttribute('src').replace(/js\/main\.js.*$/, '');
    var returnQ = '?return=' + encodeURIComponent(location.pathname);

    var name = null;
    try {
      var t = localStorage.getItem('rococo_member_token');
      if (t) {
        var payload = JSON.parse(atob(t.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
        if (payload.exp && Date.now() < payload.exp * 1000) {
          name = localStorage.getItem('rococo_member_name') || '회원';
        }
      }
    } catch (e) {}

    var li = document.createElement('li');
    li.className = 'gnb-member';
    if (name !== null) {
      var me = document.createElement('a');
      me.href = root + 'member/account/';
      me.textContent = name + '님';
      var out = document.createElement('button');
      out.type = 'button';
      out.textContent = '로그아웃';
      out.addEventListener('click', function () {
        try {
          localStorage.removeItem('rococo_member_token');
          localStorage.removeItem('rococo_member_name');
        } catch (e) {}
        location.reload();
      });
      li.appendChild(me);
      li.appendChild(out);
    } else {
      var login = document.createElement('a');
      login.href = root + 'member/login/' + returnQ;
      login.textContent = '로그인';
      li.appendChild(login);
    }
    list.appendChild(li);
  })();

  // 회원 로그인 상태 표시줄은 main.js가 아니라 각 페이지에 인라인으로 들어있음
  // (별도 파일이라 캐시되면 표시줄만 안 뜨는 문제가 있었음 — review_utils.mjs의 MEMBER_BAR 참고)

});
