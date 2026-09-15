// 사이트 전체 "수술후기" 허브 페이지(reviews/index.html) 생성.
// {cat}/{subdir}/reviews/index.html 이 존재하는 서브카테고리를 파일시스템에서 스캔해 카드로 나열.
// 후기 배치가 카테고리별로 추가될 때마다 이 스크립트만 재실행하면 허브가 자동으로 갱신됨.
import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { navHtml, CAT_NAMES } from './nav.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

function findSubName(catPath, subDir) {
  const idxPath = join(ROOT, catPath, subDir, 'index.html');
  if (!existsSync(idxPath)) return subDir;
  const html = readFileSync(idxPath, 'utf8');
  const m = html.match(/<h1 class="article-title">([\s\S]*?)<\/h1>/);
  return m ? m[1].trim() : subDir;
}

function countReviews(catPath, subDir) {
  const reviewsDir = join(ROOT, catPath, subDir, 'reviews');
  return readdirSync(reviewsDir).filter(name => {
    const p = join(reviewsDir, name);
    return /^\d+$/.test(name) && statSync(p).isDirectory();
  }).length;
}

const populated = [];
for (const catPath of Object.keys(CAT_NAMES)) {
  const catDir = join(ROOT, catPath);
  if (!existsSync(catDir)) continue;
  for (const subDir of readdirSync(catDir)) {
    const reviewsIdx = join(catDir, subDir, 'reviews', 'index.html');
    if (existsSync(reviewsIdx)) {
      populated.push({
        catPath,
        subDir,
        subName: findSubName(catPath, subDir),
        count: countReviews(catPath, subDir),
      });
    }
  }
}

console.log(`수술후기 있는 서브카테고리: ${populated.length}개`);
populated.forEach(p => console.log(`  ${p.catPath}/${p.subDir} — ${p.subName} (${p.count}건)`));

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

const nav = navHtml('../', null);
const totalCount = populated.reduce((sum, p) => sum + p.count, 0);

// 카테고리(광대성형/코성형/...)별로 묶어서 — cta-card(검정, 1~2개용 강조 패턴)를
// 27개 반복하면 새까만 벽이 되어버려서, 흰 배경 카드 그리드 + 카테고리 그룹핑으로 변경
const byCat = new Map();
for (const p of populated) {
  if (!byCat.has(p.catPath)) byCat.set(p.catPath, []);
  byCat.get(p.catPath).push(p);
}

const groups = Object.keys(CAT_NAMES)
  .filter(catPath => byCat.has(catPath))
  .map(catPath => {
    const items = byCat.get(catPath);
    const cards = items.map(p => `        <a href="../${p.catPath}/${p.subDir}/reviews/" class="card review-hub-card">
          <div class="card-body">
            <p class="card-title">${esc(p.subName)}</p>
            <p class="card-desc">환자분들이 직접 남기신 후기 ${p.count}건</p>
            <span class="review-hub-link">후기 보러가기 →</span>
          </div>
        </a>`).join('\n');
    return `    <div class="review-hub-group">
      <h2 class="section-label">${esc(CAT_NAMES[catPath])}</h2>
      <div class="card-grid">
${cards}
      </div>
    </div>`;
  }).join('\n');

const emptyState = populated.length === 0
  ? `    <p style="color:var(--gray-500);">아직 준비 중입니다. 곧 카테고리별 수술후기를 만나보실 수 있어요.</p>`
  : '';

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
<title>수술후기 (${totalCount}건) — 로코코성형외과 김상호 원장</title>
<meta name="description" content="로코코성형외과에서 시술받으신 환자분들이 직접 남기신 수술후기 ${totalCount}건을 시술별로 확인하세요.">
<meta property="og:title" content="수술후기 | 로코코 저널">
<meta property="og:description" content="환자분들이 직접 남기신 수술후기를 시술별로 확인하세요.">
<meta property="og:url" content="https://journal.rococops.com/reviews/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://journal.rococops.com/reviews/">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"수술후기 — 로코코성형외과","description":"환자분들이 직접 남기신 수술후기 ${totalCount}건","url":"https://journal.rococops.com/reviews/","inLanguage":"ko","publisher":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"https://journal.rococops.com"}}
</script>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>

<div class="gnb-overlay" id="gnbOverlay"></div>
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="../" class="logo">
      <span class="logo-main">ROCOCO</span>
      <span class="logo-sub">Journal</span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기">
      <span></span><span></span><span></span>
    </button>
    ${nav}
  </div>
</header>

<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb">
      <a href="../">홈</a>
      <span>›</span>
      <span>수술후기</span>
    </div>
    <div class="article-hero-inner" style="grid-template-columns: 1fr;">
      <div class="article-hero-text">
        <span class="eyebrow">PATIENT REVIEWS · 환자 후기</span>
        <h1 class="article-title">수술후기</h1>
        <p class="article-summary">로코코성형외과에서 시술받으신 환자분들이 직접 남기신 후기 ${totalCount}건을 시술별로 확인하세요.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
${groups}${emptyState}
  </div>
</section>

<footer class="site-footer">
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
        <p>월·금 — 09:00 ~ 19:00</p>
        <p>화·수·목 — 09:00 ~ 18:00</p>
        <p>토 — 09:00 ~ 13:00</p>
        <p>일·공휴일 휴진</p>
      </div>
      <div class="footer-links">
        <p class="footer-title">바로가기</p>
        <a href="https://rococops.com" target="_blank">기존 홈페이지</a>
        <a href="../counsel/">상담·예약</a>
        <a href="../cases/">전후사진</a>
        <a href="../about/">About 로코코</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 Rococo Plastic Surgery. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="../js/main.js"></script>
</body>
</html>
`;

writeFileSync(join(ROOT, 'reviews', 'index.html'), html, 'utf8');
console.log('생성 완료: reviews/index.html');
