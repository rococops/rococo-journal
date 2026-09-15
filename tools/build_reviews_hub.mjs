// 사이트 전체 "수술후기" 랜딩 페이지(reviews/index.html) 생성.
// 빈님 피드백: 카테고리부터 고르게 하지 말고, 들어오면 전체 후기 리스트가 바로 보이고
// 그 위에서 카테고리를 필터로 선택하는 구조가 맞다 — 그래서 카테고리 허브가 아니라
// 전체 통합 리스트 + 상단 카테고리 필터 칩으로 재구성.
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { navHtml, CAT_NAMES } from './nav.mjs';
import { PHOTO_BASE, maskName, esc, FOOTER } from './review_utils.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SITE_BASE = 'https://journal.rococops.com';

const subNameCache = new Map();
function findSubName(catPath, subDir) {
  const key = `${catPath}/${subDir}`;
  if (subNameCache.has(key)) return subNameCache.get(key);
  const idxPath = join(ROOT, catPath, subDir, 'index.html');
  let name = subDir;
  if (existsSync(idxPath)) {
    const html = readFileSync(idxPath, 'utf8');
    const m = html.match(/<h1 class="article-title">([\s\S]*?)<\/h1>/);
    if (m) name = m[1].trim();
  }
  subNameCache.set(key, name);
  return name;
}

const curated = JSON.parse(readFileSync(join(ROOT, 'postscript_curated.json'), 'utf8'));
const usable = curated
  .filter(r => r.cat && r.isauth === 'Y')
  .sort((a, b) => b.score - a.score);

console.log(`전체 후기: ${usable.length}건`);

// 카테고리 필터 집계는 제목에서 태그된 모든 카테고리(cats) 기준 — 복합시술 후기는
// 관련된 모든 상위 카테고리 필터에 다 걸림. 대표(cat) 상관없이 topCats(중복제거)로 집계.
function topCatsOf(r) {
  const list = (r.cats && r.cats.length ? r.cats : [r.cat]).map(c => c[0]);
  return [...new Set(list)];
}

const catCounts = new Map();
for (const r of usable) {
  for (const catPath of topCatsOf(r)) {
    catCounts.set(catPath, (catCounts.get(catPath) || 0) + 1);
  }
}
Object.keys(CAT_NAMES).filter(c => catCounts.has(c)).forEach(c => console.log(`  ${CAT_NAMES[c]}: ${catCounts.get(c)}건`));

const nav = navHtml('../', null);

const rows = usable.map((r) => {
  const [catPath, subDir] = r.cat; // 대표 카테고리 — 실제 페이지 위치(링크)는 항상 여기
  const subName = findSubName(catPath, subDir);
  const masked = maskName(r.writer);
  const desc = r.contents_text.slice(0, 60).replace(/\s+/g,' ').trim();
  const thumb = r.photos.length
    ? `<div class="review-row-thumb"><img src="${PHOTO_BASE}1/${r.photos[0]}" alt="" loading="lazy"></div>`
    : `<div class="review-row-thumb-empty"></div>`;
  const dataCat = topCatsOf(r).join(' ');
  return `      <a href="../${catPath}/${subDir}/reviews/${r.num}/" class="review-row" data-cat="${dataCat}">
        ${thumb}
        <div class="review-row-body">
          <p class="review-row-title">${r.isbest === 'Y' ? '<span class="review-row-best">BEST</span>' : ''}<span class="review-row-tag">${esc(subName)}</span>${esc(r.subject.trim() || subName + ' 후기')}</p>
          <p class="review-row-desc">${esc(desc)}</p>
          <p class="review-row-meta">${esc(masked)}님 후기 · ${(r.udate||'').slice(0,7).replace('-','.')}</p>
        </div>
      </a>`;
}).join('\n');

const filterChips = ['all', ...Object.keys(CAT_NAMES).filter(c => catCounts.has(c))].map(c => {
  if (c === 'all') return `<button type="button" class="sort-btn active" data-cat="all">전체 (${usable.length})</button>`;
  return `<button type="button" class="sort-btn" data-cat="${c}">${esc(CAT_NAMES[c])} (${catCounts.get(c)})</button>`;
}).join('\n      ');

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
<title>수술후기 (${usable.length}건) — 로코코성형외과 김상호 원장</title>
<meta name="description" content="로코코성형외과에서 시술받으신 환자분들이 직접 남기신 수술후기 ${usable.length}건.">
<meta property="og:title" content="수술후기 | 로코코 저널">
<meta property="og:description" content="환자분들이 직접 남기신 수술후기를 확인하세요.">
<meta property="og:url" content="https://journal.rococops.com/reviews/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://journal.rococops.com/reviews/">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"수술후기 — 로코코성형외과","description":"환자분들이 직접 남기신 수술후기 ${usable.length}건","url":"https://journal.rococops.com/reviews/","inLanguage":"ko","publisher":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"https://journal.rococops.com"}}
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
        <h1 class="article-title">수술후기</h1>
        <p class="article-summary">로코코성형외과에서 시술받으신 환자분들이 직접 남기신 후기 ${usable.length}건입니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sort-toggle" id="reviewCatFilter" style="margin-bottom:1.5rem;flex-wrap:wrap;">
      ${filterChips}
    </div>
    <div class="review-list review-list-cols" id="review-list">
${rows}
    </div>
    <div style="text-align:center;margin-top:2rem;">
      <button type="button" class="sort-btn" id="loadMoreReviews" style="padding:0.7rem 2rem;">더보기</button>
    </div>
  </div>
</section>

${FOOTER('../')}
<script>
(function(){
  var PAGE = 30;
  var list = document.getElementById('review-list');
  var allItems = Array.prototype.slice.call(list.querySelectorAll('.review-row'));
  var moreBtn = document.getElementById('loadMoreReviews');
  var chips = document.querySelectorAll('#reviewCatFilter .sort-btn');
  var state = { cat: 'all', shown: PAGE };
  function matches(el){ return state.cat === 'all' || el.dataset.cat.split(' ').indexOf(state.cat) !== -1; }
  function apply(){
    var filtered = allItems.filter(matches);
    allItems.forEach(function(el){ el.hidden = true; });
    filtered.slice(0, state.shown).forEach(function(el){ el.hidden = false; });
    moreBtn.hidden = filtered.length <= state.shown;
  }
  chips.forEach(function(btn){
    btn.addEventListener('click', function(){
      chips.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      state.cat = btn.dataset.cat;
      state.shown = PAGE;
      apply();
    });
  });
  moreBtn.addEventListener('click', function(){ state.shown += PAGE; apply(); });
  apply();
})();
</script>
</body>
</html>
`;

writeFileSync(join(ROOT, 'reviews', 'index.html'), html, 'utf8');
console.log('생성 완료: reviews/index.html');
