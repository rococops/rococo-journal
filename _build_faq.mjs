// 로코코 저널 — about/faq 페이지 생성기
// 원본: C:\Users\binia\Desktop\로코코cafe블로그\_저널FAQ_AEO.md
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = 'C:/Users/binia/Desktop/journal';
const SRC = 'C:/Users/binia/Desktop/로코코cafe블로그/_저널FAQ_AEO.md';
const OUT_DIR = join(ROOT, 'about', 'faq');
const URL = 'https://journal.rococops.com/about/faq/';

// 그룹명 → 앵커 id (사이트 카테고리 슬러그와 통일)
const SLUG = {
  '코성형 기본': 'basic',
  '코재수술': 'revision',
  '매부리코': 'hump',
  '휜코·절골술': 'osteotomy',
  '복코·코끝성형': 'tip',
  '콧구멍·콧볼(비익)': 'nostril',
  '코막힘·비염수술': 'rhinitis',
  '광대축소': 'cheekbone',
  '눈성형': 'eye',
  '이마거상술': 'forehead',
  '동안성형·지방이식·윤곽': 'antiaging',
  '상담·수술 전후 관리': 'care',
};

// ── 파싱 ──────────────────────────────────────────────
const md = readFileSync(SRC, 'utf8');
const groups = [];
let cur = null;
for (const raw of md.split(/\r?\n/)) {
  const line = raw.trim();
  if (line.startsWith('## ')) { cur = { name: line.slice(3).trim(), items: [] }; groups.push(cur); continue; }
  if (!cur) continue;
  if (line.startsWith('**Q. ')) { cur.items.push({ q: line.slice(5).replace(/\*\*$/, '').trim(), a: '' }); continue; }
  if (line.startsWith('A. ')) { cur.items[cur.items.length - 1].a = line.slice(3).trim(); }
}
const total = groups.reduce((s, g) => s + g.items.length, 0);
groups.forEach(g => { if (!SLUG[g.name]) throw new Error('슬러그 없음: ' + g.name); });
groups.forEach(g => g.items.forEach(it => { if (!it.a) throw new Error('답변 없음: ' + it.q); }));

// ── 유틸 ──────────────────────────────────────────────
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// ── JSON-LD (FAQPage) ─────────────────────────────────
const faqLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  name: '자주 묻는 질문',
  url: URL,
  inLanguage: 'ko',
  about: { '@type': 'MedicalSpecialty', name: 'Plastic Surgery' },
  author: {
    '@type': 'Physician',
    name: '김상호',
    medicalSpecialty: 'PlasticSurgery',
    worksFor: { '@type': 'MedicalBusiness', name: '로코코성형외과' },
  },
  publisher: {
    '@type': 'MedicalBusiness',
    name: '로코코성형외과',
    url: 'https://journal.rococops.com',
    telephone: '+82-2-2135-2702',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '논현로 842 압구정빌딩 3층',
      addressLocality: '강남구',
      addressRegion: '서울특별시',
      addressCountry: 'KR',
    },
  },
  mainEntity: groups.flatMap(g => g.items.map(it => ({
    '@type': 'Question',
    name: it.q,
    answerCount: 1,
    acceptedAnswer: { '@type': 'Answer', text: it.a },
  }))),
};

const breadcrumbLd = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: '홈', item: 'https://journal.rococops.com/' },
    { '@type': 'ListItem', position: 2, name: 'About', item: 'https://journal.rococops.com/about/' },
    { '@type': 'ListItem', position: 3, name: '자주 묻는 질문', item: URL },
  ],
};

// ── GNB (philosophy 페이지에서 그대로 추출해 재사용) ──
const tpl = readFileSync(join(ROOT, 'about', 'philosophy', 'index.html'), 'utf8');
const gnb = tpl.slice(tpl.indexOf('<div class="gnb-overlay"'), tpl.indexOf('</header>') + 9);
const footer = tpl.slice(tpl.indexOf('<!-- 하단 CTA -->'), tpl.lastIndexOf('</body>'));

// ── 본문 ──────────────────────────────────────────────
const nav = groups.map(g =>
  `        <a href="#${SLUG[g.name]}" class="faq-chip">${esc(g.name)} <em>${g.items.length}</em></a>`
).join('\n');

const sections = groups.map(g => `
<section class="faq-section" id="${SLUG[g.name]}">
  <div class="container">
    <h2 class="faq-group">${esc(g.name)}</h2>
${g.items.map(it => `    <div class="faq-item">
      <h3 class="faq-q">${esc(it.q)}</h3>
      <p class="faq-a">${esc(it.a)}</p>
    </div>`).join('\n')}
  </div>
</section>`).join('\n');

const html = `<!DOCTYPE html>
<html lang="ko">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0Y6WHB6J6X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0Y6WHB6J6X');
</script>
<script>
fetch('https://rococo-journal-api.vercel.app/api/track', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({path: location.pathname, referrer: document.referrer})
}).catch(function(){});
</script>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>자주 묻는 질문 | 로코코 저널</title>
<meta name="description" content="코성형·코재수술·매부리코·휜코·콧구멍성형·광대축소·눈성형·이마거상술 등 로코코성형외과 김상호 원장이 상담에서 가장 많이 받는 질문 ${total}가지를 정리했습니다.">
<meta property="og:title" content="자주 묻는 질문 | 로코코 저널">
<meta property="og:description" content="상담에서 가장 많이 받는 질문 ${total}가지를 시술별로 정리했습니다.">
<meta property="og:image" content="https://rococops.com/images/intro/interior/photo/1.jpg">
<meta property="og:url" content="${URL}">
<meta property="og:type" content="website">
<link rel="canonical" href="${URL}">
<script type="application/ld+json">
${JSON.stringify(faqLd, null, 2)}
</script>
<script type="application/ld+json">
${JSON.stringify(breadcrumbLd, null, 2)}
</script>
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="../../css/style.css">
</head>
<body>

${gnb}

<!-- 아티클 히어로 -->
<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb">
      <a href="../../">홈</a>
      <span>›</span>
      <a href="../">About</a>
      <span>›</span>
      <span>자주 묻는 질문</span>
    </div>
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <span class="eyebrow">About 로코코</span>
        <h1 class="article-title">자주 묻는 질문</h1>
        <p class="article-summary">김상호 원장이 상담에서 가장 많이 받는 질문 ${total}가지를 시술별로 정리했습니다. 가능한 범위와 함께 어려운 부분까지 그대로 담았습니다.</p>
        <div class="article-meta">
          <span class="meta-author">김상호 원장</span>
          <span class="dot">·</span>
          <span class="meta-cat">자주 묻는 질문</span>
          <span class="dot">·</span>
          <span class="meta-clinic">로코코성형외과</span>
        </div>
      </div>
      <div class="article-hero-img">
        <img src="https://rococops.com/images/intro/interior/photo/1.jpg" alt="로코코성형외과 진료실" loading="eager">
      </div>
    </div>
  </div>
</section>

<!-- 검색 · 카테고리 바로가기 -->
<nav class="faq-nav" id="faqNav" aria-label="질문 검색 및 시술별 바로가기">
  <div class="container">
    <div class="faq-nav-inner">
      <div class="faq-search" id="faqSearchWrap">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <label for="faqSearch" class="sr-only">질문 검색</label>
        <input type="search" id="faqSearch" placeholder="궁금한 내용을 검색해 보세요 (예: 늑연골, 붓기, 흉터)" autocomplete="off" aria-controls="faqResults">
        <button type="button" class="faq-search-clear" id="faqClear" aria-label="검색어 지우기">&#x2715;</button>
      </div>
      <p class="faq-count" id="faqCount" role="status" aria-live="polite"></p>
      <div class="faq-chips">
${nav}
      </div>
    </div>
  </div>
</nav>

<div id="faqResults">
${sections}

<div class="faq-empty" id="faqEmpty">
  <div class="container">
    <p class="faq-empty-title">검색 결과가 없습니다</p>
    <p>다른 검색어로 찾아보시거나, 궁금한 점을 상담으로 직접 물어봐 주세요.</p>
  </div>
</div>
</div>

<!-- 안내 -->
<section class="section">
  <div class="container">
    <div class="faq-notice">
      <p class="faq-notice-title">읽으실 때 참고해 주세요</p>
      <p>이 페이지의 내용은 일반적인 정보 제공을 위한 것이며, 개인의 상태에 따라 적용되는 방법과 결과는 달라질 수 있습니다.</p>
      <p>회복 기간과 경과는 개인차가 있으며, 모든 수술과 시술에는 부작용의 가능성이 있습니다.</p>
      <p>내 경우에 무엇이 가능하고 무엇이 어려운지는 진료에서 직접 확인하신 뒤 판단하시는 것이 정확합니다.</p>
    </div>
  </div>
</section>

${footer}
<script src="../../js/main.js"></script>
<script>
(function () {
  var input = document.getElementById('faqSearch');
  if (!input) return;
  var nav = document.getElementById('faqNav');
  var wrap = document.getElementById('faqSearchWrap');
  var clear = document.getElementById('faqClear');
  var count = document.getElementById('faqCount');
  var empty = document.getElementById('faqEmpty');
  var sections = [].slice.call(document.querySelectorAll('.faq-section'));
  var items = [].slice.call(document.querySelectorAll('.faq-item'));
  var header = document.querySelector('.site-header');

  // 앵커 점프가 고정 헤더·검색바에 가리지 않도록 오프셋을 실측해 반영.
  // 웹폰트 로딩·칩 줄바꿈·검색 상태에 따라 높이가 바뀌므로 변화를 계속 관찰한다.
  function offset() {
    var h = (header ? header.offsetHeight : 0) + nav.offsetHeight + 16;
    document.documentElement.style.setProperty('--faq-offset', h + 'px');
  }
  offset();
  window.addEventListener('resize', offset);
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(offset);
    ro.observe(nav);
    if (header) ro.observe(header);
  } else {
    window.addEventListener('load', offset);
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(offset);

  // 공백을 무시한 정규화 문자열 + 원문 인덱스 매핑
  function index(el) {
    var raw = el.textContent;
    var norm = '', map = [];
    for (var i = 0; i < raw.length; i++) {
      var c = raw[i];
      if (/\\s/.test(c)) continue;
      norm += c.toLowerCase();
      map.push(i);
    }
    return { el: el, raw: raw, norm: norm, map: map };
  }
  var data = items.map(function (it) {
    return {
      item: it,
      parts: [index(it.querySelector('.faq-q')), index(it.querySelector('.faq-a'))]
    };
  });

  function paint(part, from, to) {
    var el = part.el, raw = part.raw;
    while (el.firstChild) el.removeChild(el.firstChild);
    if (from < 0) { el.appendChild(document.createTextNode(raw)); return; }
    el.appendChild(document.createTextNode(raw.slice(0, from)));
    var mk = document.createElement('mark');
    mk.textContent = raw.slice(from, to);
    el.appendChild(mk);
    el.appendChild(document.createTextNode(raw.slice(to)));
  }

  function run() {
    var q = input.value.replace(/\\s/g, '').toLowerCase();
    wrap.classList.toggle('has-value', input.value.length > 0);

    if (!q) {
      nav.classList.remove('searching');
      empty.classList.remove('show');
      data.forEach(function (d) {
        d.item.hidden = false;
        d.parts.forEach(function (p) { paint(p, -1); });
      });
      sections.forEach(function (s) { s.hidden = false; });
      offset();
      return;
    }

    nav.classList.add('searching');
    var hits = 0;
    data.forEach(function (d) {
      var found = false;
      d.parts.forEach(function (p) {
        var i = p.norm.indexOf(q);
        if (i < 0) { paint(p, -1); return; }
        found = true;
        paint(p, p.map[i], p.map[i + q.length - 1] + 1);
      });
      d.item.hidden = !found;
      if (found) hits++;
    });
    sections.forEach(function (s) {
      s.hidden = !s.querySelector('.faq-item:not([hidden])');
    });
    count.innerHTML = hits ? '검색 결과 <b>' + hits + '</b>개' : '검색 결과가 없습니다';
    empty.classList.toggle('show', hits === 0);
    offset();
  }

  var t;
  input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(run, 120); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Escape') { input.value = ''; run(); } });
  clear.addEventListener('click', function () { input.value = ''; input.focus(); run(); });
  document.querySelectorAll('.faq-chip').forEach(function (a) {
    a.addEventListener('click', function () { if (input.value) { input.value = ''; run(); } });
  });
})();
</script>
</body>
</html>
`;

mkdirSync(OUT_DIR, { recursive: true });
writeFileSync(join(OUT_DIR, 'index.html'), html, 'utf8');
console.log(`about/faq/index.html 생성 — 그룹 ${groups.length} / 질문 ${total} / ${(html.length / 1024).toFixed(1)}KB`);
groups.forEach(g => console.log(`  #${SLUG[g.name].padEnd(10)} ${g.name} (${g.items.length})`));
