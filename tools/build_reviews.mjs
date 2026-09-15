// 환자 후기(postscript_curated.json) → 저널 "수술후기" 섹션 생성
// 구조: {cat}/{subdir}/reviews/index.html (목록) + {cat}/{subdir}/reviews/{num}/index.html (개별)
// 케이스 글({cat}/{subdir}/index.html)의 .card-grid는 절대 건드리지 않음.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { navHtml, CAT_NAMES } from './nav.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SITE_BASE = 'https://journal.rococops.com';
const PHOTO_BASE = 'https://rococops.com/files/postscript/attach';

// 서브카테고리 자체 케이스 목록 페이지(H1)에서 subName을 읽어옴 — SUBCATS 메타를 별도로 두지 않고 재사용
function findSubName(catPath, subDir) {
  const idxPath = join(ROOT, catPath, subDir, 'index.html');
  if (!existsSync(idxPath)) return subDir;
  const html = readFileSync(idxPath, 'utf8');
  const m = html.match(/<h1 class="article-title">([\s\S]*?)<\/h1>/);
  return m ? m[1].trim() : subDir;
}

// ── 익명화: 흔한 한국 성씨로 시작하는 순한글 3자(성+이름2자)만 실명으로 간주, 가운데 글자만 마스킹.
//    나머지(닉네임/영문/숫자/2·4자 등)는 원본 그대로 사용 — 사용자 확인: "흔한 한국성씨 3자일경우만 간주해 가운데글자만 마스킹" ──
const SURNAMES = new Set(['김','이','박','최','정','강','조','윤','장','임','한','오','서','신','권','황','안','송','전','홍','유','고','문','양','손','배','백','허','남','심','노','하','곽','성','차','주','우','구','나','민','진','지','엄','채','원','천','방','공','현','함','변','염','여','추','도','소','석','선','설','마','길','위','표','명','기','반','왕','금','옥','육','인','맹','제','계','피','연','국','예','경','봉','사','어','두','감','판','단','갈','좌','편','부','간','매','상','시','목','형']);

function isRealName3(name) {
  return /^[가-힣]{3}$/.test(name) && SURNAMES.has(name[0]);
}

function maskName(name) {
  if (!name) return '고객';
  name = name.trim();
  if (!name) return '고객';
  if (isRealName3(name)) return name[0] + '0' + name[2];
  return name;
}

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

const FOOTER = (root) => `<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-info">
        <p class="footer-logo">ROCOCO <em>Journal</em></p>
        <p>로코코성형외과의원</p>
        <p>서울특별시 강남구 논현로 842 (신사동 599) 압구정빌딩 3층</p>
        <p>대표원장 김상호 · 02-2135-2702</p>
        <p>사업자등록번호 211-09-48591</p>
      </div>
      <div class="footer-hours">
        <p class="footer-title">진료시간</p>
        <p>월·금 — 09:00 ~ 19:00</p><p>화·수·목 — 09:00 ~ 18:00</p>
        <p>토 — 09:00 ~ 13:00</p><p>일·공휴일 휴진</p>
      </div>
      <div class="footer-links">
        <p class="footer-title">바로가기</p>
        <a href="https://rococops.com" target="_blank">기존 홈페이지</a>
        <a href="${root}counsel/">상담·예약</a>
        <a href="${root}cases/">전후사진</a>
        <a href="${root}about/">About 로코코</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 Rococo Plastic Surgery. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="${root}js/main.js"></script>
<a href="https://pf.kakao.com/_xdBpRl" target="_blank" rel="noopener" class="kakao-float">
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="14" cy="13" rx="12" ry="10" fill="#3C1E1E"/>
    <path d="M10.5 10.5c0-1.1.9-2 2-2h3c1.1 0 2 .9 2 2v2a2 2 0 01-2 2h-.8l-1.7 2.2v-2.2h-.5a2 2 0 01-2-2v-2z" fill="#FEE500"/>
  </svg>
  카카오톡 상담 문의
</a>`;

// ── 개별 후기 페이지 ──
function generateReviewPage(r, cfg) {
  const root = '../../../../'; // {cat}/{subdir}/reviews/{num}/ → 4단계
  const reviewsListRoot = '../';   // → {cat}/{subdir}/reviews/
  const caseListRoot = '../../';   // → {cat}/{subdir}/
  const catName = CAT_NAMES[cfg.catPath];
  const masked = maskName(r.writer);
  const title = r.subject.trim() || `${cfg.subName} 후기`;
  const bodyParas = r.contents_text.split('\n').map(s => s.trim()).filter(Boolean);
  const bodyHtml = bodyParas.map(p => `<p>${esc(p)}</p>`).join('\n        ');
  const photoUrls = r.photos.map((f, i) => `${PHOTO_BASE}${(i % 6) + 1}/${f}`);
  const imgHtml = photoUrls.map(u => `<img src="${u}" alt="${esc(masked)}님 후기 사진" loading="lazy">`).join('\n        ');
  const content = bodyHtml + (imgHtml ? '\n        ' + imgHtml : '');
  const description = r.contents_text.slice(0, 140).replace(/\s+/g,' ').trim();
  const ogUrl = `${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/reviews/${r.num}/`;
  const ogImage = photoUrls[0] || `${root}images/thumbnails/1-1.jpg`;
  const heroImage = photoUrls[0] || `${root}images/thumbnails/1-1.jpg`;
  const dateStr = (r.udate || '').slice(0, 10) || '2020-01-01';
  const nav = navHtml(root, cfg.catPath);
  const titleJ = title.replace(/"/g,'\\"');
  const descJ = description.replace(/"/g,'\\"');

  return `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(title)} — ${cfg.subName} 수술후기 | 로코코성형외과</title>
<meta name="description" content="${esc(description)}">
<meta property="og:title" content="${esc(title)} — ${cfg.subName} 수술후기">
<meta property="og:description" content="${esc(description)}">
<meta property="og:image" content="${ogImage}">
<meta property="og:url" content="${ogUrl}">
<meta property="og:type" content="article">
<link rel="canonical" href="${ogUrl}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<script type="application/ld+json">
[{"@context":"https://schema.org","@type":"Review","headline":"${titleJ}","reviewBody":"${descJ}","url":"${ogUrl}","datePublished":"${dateStr}","inLanguage":"ko-KR","author":{"@type":"Person","name":"${masked}"},"itemReviewed":{"@type":"MedicalProcedure","name":"${cfg.subName}","provider":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"}},"publisher":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"}},{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"${SITE_BASE}/"},{"@type":"ListItem","position":2,"name":"${catName}","item":"${SITE_BASE}/${cfg.catPath}/"},{"@type":"ListItem","position":3,"name":"${cfg.subName}","item":"${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/"},{"@type":"ListItem","position":4,"name":"수술후기","item":"${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/reviews/"},{"@type":"ListItem","position":5,"name":"${titleJ}","item":"${ogUrl}"}]}]
</script>
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="${root}css/style.css">
</head>
<body>
<div class="gnb-overlay" id="gnbOverlay"></div>
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="${root}" class="logo"><span class="logo-main">ROCOCO</span><span class="logo-sub">Journal</span></a>
    <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
    ${nav}
  </div>
</header>
<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb">
      <a href="${root}">홈</a><span>›</span>
      <a href="${root}${cfg.catPath}/">${catName}</a><span>›</span>
      <a href="${caseListRoot}">${cfg.subName}</a><span>›</span>
      <a href="${reviewsListRoot}">수술후기</a><span>›</span>
      <span>${esc(title.slice(0,24))}${title.length>24?'...':''}</span>
    </div>
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <span class="eyebrow">PATIENT REVIEW · 환자 후기</span>
        <h1 class="article-title">${esc(title)}</h1>
        <p class="article-summary">${esc(description)}</p>
        <div class="article-meta">
          <span class="meta-author">${esc(masked)}님 후기</span><span class="dot">·</span>
          <span class="meta-cat">${cfg.subName}</span><span class="dot">·</span>
          <span class="meta-clinic">로코코성형외과</span>
        </div>
      </div>
      <div class="article-hero-img"><img src="${heroImage}" alt="${esc(cfg.subName)} 환자 후기" loading="eager"></div>
    </div>
  </div>
</section>
<article class="article-body">
  <div class="container">
    <div class="article-layout">
      <div class="article-content">
        ${content}
        <div class="inline-cta">
          <p class="inline-cta-text">${cfg.subName}에 대해 더 궁금한 점이 있으신가요?</p>
          <a href="${root}counsel/online/?from=${cfg.subName}후기" class="inline-cta-btn">김상호 원장에게 직접 상담하기 →</a>
        </div>
      </div>
      <aside class="article-sidebar">
        <div class="sidebar-card">
          <p class="sidebar-title">전후사진 보기</p>
          <p class="sidebar-desc">로코코에서 수술하신 분들의 실제 케이스를 확인하세요</p>
          <a href="${root}cases/" class="sidebar-btn">전후사진 열람 →</a>
        </div>
        <div class="sidebar-card">
          <p class="sidebar-title">온라인 상담</p>
          <p class="sidebar-desc">02-2135-2702<br>월·금 09:00~19:00<br>화·수·목 09:00~18:00<br>토 09:00~13:00</p>
          <a href="${root}counsel/online/?from=${cfg.subName}후기" class="sidebar-btn">상담 신청하기 →</a>
        </div>
        <div class="sidebar-related">
          <p class="sidebar-title">${cfg.subName} 다른 후기</p>
          <a href="${reviewsListRoot}" class="related-link">수술후기 목록 보기 →</a>
        </div>
        <div class="sidebar-related">
          <p class="sidebar-title">${cfg.subName} 케이스 설명</p>
          <a href="${caseListRoot}" class="related-link">원장님 케이스 글 보기 →</a>
        </div>
      </aside>
    </div>
  </div>
</article>
<section class="cta-section">
  <div class="container">
    <div class="cta-grid">
      <a href="${root}cases/" class="cta-card"><div class="cta-card-inner"><span class="cta-label">${cfg.subName} 전후사진</span><h3 class="cta-title">실제 수술 결과를<br>직접 확인하세요</h3><p class="cta-desc">로코코에서 진행한 실제 케이스 사진을 확인하세요</p><span class="cta-btn">전후사진 보기 →</span></div></a>
      <a href="${root}counsel/online/?from=${cfg.subName}후기" class="cta-card"><div class="cta-card-inner"><span class="cta-label">온라인 상담</span><h3 class="cta-title">궁금한 점을<br>직접 물어보세요</h3><p class="cta-desc">김상호 원장이 직접 답변해 드립니다</p><span class="cta-btn">상담 신청하기 →</span></div></a>
    </div>
  </div>
</section>
${FOOTER(root)}
</body>
</html>`;
}

// ── 후기 목록 페이지 ──
function generateReviewIndex(reviews, cfg) {
  const root = '../../../'; // {cat}/{subdir}/reviews/ → 3단계
  const caseListRoot = '../';
  const catName = CAT_NAMES[cfg.catPath];
  const nav = navHtml(root, cfg.catPath);

  const photoReviews = reviews.filter(r => r.photos.length);
  const textReviews = reviews.filter(r => !r.photos.length);

  // 사진 있는 후기 — 기존 카드그리드(썸네일 포함)
  const photoCards = photoReviews.map((r) => {
    const masked = maskName(r.writer);
    const photo = `${PHOTO_BASE}1/${r.photos[0]}`;
    const desc = r.contents_text.slice(0, 70).replace(/\s+/g,' ').trim();
    return `      <a href="${r.num}/" class="card" data-date="${(r.udate||'').slice(0,10)}">
        <div class="card-img">
          <img src="${photo}" alt="${esc(masked)}님 후기" loading="lazy">
          <span class="card-tag">사진 후기</span>
        </div>
        <div class="card-body">
          <p class="card-title">${esc(r.subject.trim() || cfg.subName + ' 후기')}</p>
          <p class="card-desc">${esc(desc)}</p>
        </div>
      </a>`;
  }).join('\n');

  // 글만 있는 후기 — 썸네일 없는 텍스트 리스트 (사진 후기 자리에 가짜 이미지 채우지 않음)
  const textRows = textReviews.map((r) => {
    const masked = maskName(r.writer);
    const desc = r.contents_text.slice(0, 90).replace(/\s+/g,' ').trim();
    return `      <a href="${r.num}/" class="review-row">
        <p class="review-row-title">${esc(r.subject.trim() || cfg.subName + ' 후기')}</p>
        <p class="review-row-desc">${esc(desc)}</p>
        <p class="review-row-meta">${esc(masked)}님 후기 · ${cfg.subName}</p>
      </a>`;
  }).join('\n');

  // 사진/글 둘 다 있을 때만 필터·섹션 분리 표시 — 한쪽이 0건이면 굳이 나누지 않음
  const showSplit = photoReviews.length > 0 && textReviews.length > 0;

  const filterBar = showSplit ? `    <div class="sort-toggle" id="reviewFilter" style="margin-bottom:1.5rem;">
      <button type="button" class="sort-btn active" data-filter="all">전체 (${reviews.length})</button>
      <button type="button" class="sort-btn" data-filter="photo">사진 있는 후기 (${photoReviews.length})</button>
      <button type="button" class="sort-btn" data-filter="text">글만 (${textReviews.length})</button>
    </div>` : '';

  const photoSection = photoReviews.length === 0 ? '' : `    <div id="photo-section">
      ${showSplit ? `<p style="font-weight:700;font-size:0.95rem;color:var(--gray-600);margin-bottom:1rem;">사진 후기 (${photoReviews.length})</p>` : ''}
      <div class="card-grid" id="photo-grid">
${photoCards}
      </div>
      <div style="text-align:center;margin-top:2rem;">
        <button type="button" class="sort-btn" id="loadMorePhoto" style="padding:0.7rem 2rem;">더보기 →</button>
      </div>
    </div>`;

  const textSection = textReviews.length === 0 ? '' : `    <div id="text-section" style="margin-top:${showSplit ? '2.5rem' : '0'};">
      ${showSplit ? `<p style="font-weight:700;font-size:0.95rem;color:var(--gray-600);margin-bottom:1rem;">글 후기 (${textReviews.length})</p>` : ''}
      <div class="review-list" id="text-list">
${textRows}
      </div>
      <div style="text-align:center;margin-top:2rem;">
        <button type="button" class="sort-btn" id="loadMoreText" style="padding:0.7rem 2rem;">더보기 →</button>
      </div>
    </div>`;

  const paginationScript = `
    <script>
      (function(){
        var PAGE = 9;
        function setupSection(containerId, moreBtnId, itemSelector){
          var container = document.getElementById(containerId);
          if (!container) return null;
          var items = Array.prototype.slice.call(container.querySelectorAll(itemSelector));
          var moreBtn = document.getElementById(moreBtnId);
          var shown = PAGE;
          function apply(){
            items.forEach(function(el, i){ el.hidden = i >= shown; });
            if (moreBtn) moreBtn.hidden = shown >= items.length;
          }
          if (moreBtn) moreBtn.addEventListener('click', function(){ shown += PAGE; apply(); });
          apply();
          return { reset: function(){ shown = PAGE; apply(); } };
        }
        var photoPager = setupSection('photo-grid', 'loadMorePhoto', '.card');
        var textPager = setupSection('text-list', 'loadMoreText', '.review-row');

        var filterBtns = document.querySelectorAll('#reviewFilter .sort-btn');
        var photoSection = document.getElementById('photo-section');
        var textSection = document.getElementById('text-section');
        filterBtns.forEach(function(btn){
          btn.addEventListener('click', function(){
            filterBtns.forEach(function(b){ b.classList.remove('active'); });
            btn.classList.add('active');
            var f = btn.dataset.filter;
            if (photoSection) photoSection.hidden = (f === 'text');
            if (textSection) textSection.hidden = (f === 'photo');
            if (photoPager) photoPager.reset();
            if (textPager) textPager.reset();
          });
        });
      })();
    </script>`;

  return `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${cfg.subName} 수술후기 (${reviews.length}건) — 로코코성형외과 김상호 원장</title>
<meta name="description" content="${cfg.subName} 환자분들이 직접 남긴 수술후기 ${reviews.length}건 — 로코코성형외과">
<meta property="og:title" content="${cfg.subName} 수술후기 | 로코코 저널">
<meta property="og:description" content="${cfg.subName} 환자분들이 직접 남긴 수술후기 ${reviews.length}건">
<meta property="og:image" content="${root}images/thumbnails/1-1.jpg">
<meta property="og:url" content="${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/reviews/">
<meta property="og:type" content="website">
<link rel="canonical" href="${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/reviews/">
<script type="application/ld+json">
[{"@context":"https://schema.org","@type":"CollectionPage","name":"${cfg.subName} 수술후기 — 로코코성형외과","description":"${cfg.subName} 환자 후기 ${reviews.length}건","url":"${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/reviews/","inLanguage":"ko","about":{"@type":"MedicalProcedure","name":"${cfg.subName}"},"publisher":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"}},{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"${SITE_BASE}/"},{"@type":"ListItem","position":2,"name":"${catName}","item":"${SITE_BASE}/${cfg.catPath}/"},{"@type":"ListItem","position":3,"name":"${cfg.subName}","item":"${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/"},{"@type":"ListItem","position":4,"name":"수술후기","item":"${SITE_BASE}/${cfg.catPath}/${cfg.subDir}/reviews/"}]}]
</script>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="${root}css/style.css">
</head>
<body>
<div class="gnb-overlay" id="gnbOverlay"></div>
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="${root}" class="logo"><span class="logo-main">ROCOCO</span><span class="logo-sub">Journal</span></a>
    <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
    ${nav}
  </div>
</header>
<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb">
      <a href="${root}">홈</a><span>›</span>
      <a href="${root}${cfg.catPath}/">${catName}</a><span>›</span>
      <a href="${caseListRoot}">${cfg.subName}</a><span>›</span>
      <span>수술후기</span>
    </div>
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <span class="eyebrow">PATIENT REVIEWS · 환자 후기</span>
        <h1 class="article-title">${cfg.subName} 수술후기</h1>
        <p class="article-summary">${cfg.subName}을 받으신 환자분들이 직접 남기신 후기 ${reviews.length}건입니다.</p>
        <div class="article-meta">
          <span class="meta-cat">${cfg.subName}</span><span class="dot">·</span>
          <span class="meta-clinic">로코코성형외과</span>
        </div>
      </div>
      <div class="article-hero-img"><img src="${root}images/thumbnails/1-1.jpg" alt="${cfg.subName} 수술후기" loading="eager"></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head">
      <h2 class="section-label">${cfg.subName} 수술후기 (${reviews.length}건)</h2>
      <a href="${caseListRoot}" style="font-size:0.85rem;color:var(--gray-600);">← ${cfg.subName} 케이스 글 보기</a>
    </div>
${filterBar}
${photoSection}
${textSection}
${paginationScript}
  </div>
</section>
${FOOTER(root)}
</body>
</html>`;
}

// ── 실행 — 분류(cat)되고 불만어감(flag_bad) 아닌 모든 후기를, 서브카테고리별로 전부 발행 ──
const curated = JSON.parse(readFileSync(join(ROOT, 'postscript_curated.json'), 'utf8'));
const usable = curated.filter(r => r.cat && !r.flag_bad);

const groups = new Map(); // "catPath/subDir" -> rows[]
for (const r of usable) {
  const key = r.cat.join('/');
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key).push(r);
}

console.log(`대상 서브카테고리: ${groups.size}개, 총 후기: ${usable.length}건\n`);

let totalNew = 0, totalSkipped = 0;
for (const [key, rows] of [...groups.entries()].sort((a, b) => b[1].length - a[1].length)) {
  const [catPath, subDir] = key.split('/');
  const cfg = { catPath, subDir, subName: findSubName(catPath, subDir) };
  const sorted = rows.sort((a, b) => b.score - a.score);
  const baseDir = join(ROOT, catPath, subDir, 'reviews');
  mkdirSync(baseDir, { recursive: true });

  const built = [];
  let newInGroup = 0;
  for (const r of sorted) {
    const dir = join(baseDir, String(r.num));
    if (existsSync(dir)) { totalSkipped++; built.push(r); continue; }
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, 'index.html'), generateReviewPage(r, cfg), 'utf8');
    totalNew++; newInGroup++;
    built.push(r);
  }
  writeFileSync(join(baseDir, 'index.html'), generateReviewIndex(built, cfg), 'utf8');
  console.log(`${key} — ${cfg.subName} (총 ${built.length}건, 신규 ${newInGroup})`);
}

console.log(`\n완료 — 신규 생성 ${totalNew}건, 이미 있어서 건너뜀 ${totalSkipped}건`);
