// 환자 후기(postscript_curated.json) → 저널 "수술후기" 섹션 생성
// 구조: {cat}/{subdir}/reviews/index.html (목록) + {cat}/{subdir}/reviews/{num}/index.html (개별)
// 케이스 글({cat}/{subdir}/index.html)의 .card-grid는 절대 건드리지 않음.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { navHtml, CAT_NAMES } from './nav.mjs';
import { PHOTO_BASE, maskName, esc, FOOTER } from './review_utils.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SITE_BASE = 'https://journal.rococops.com';

// 서브카테고리 자체 케이스 목록 페이지(H1)에서 subName을 읽어옴 — SUBCATS 메타를 별도로 두지 않고 재사용
function findSubName(catPath, subDir) {
  const idxPath = join(ROOT, catPath, subDir, 'index.html');
  if (!existsSync(idxPath)) return subDir;
  const html = readFileSync(idxPath, 'utf8');
  const m = html.match(/<h1 class="article-title">([\s\S]*?)<\/h1>/);
  return m ? m[1].trim() : subDir;
}

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

  // 후기 목록 — 사진 유무 관계없이 하나의 컴팩트 row 리스트로 통일.
  // 원본 사진 품질이 들쭉날쭉(검열바·콜라주 등)해서 큰 카드로 쓰면 지저분해짐 —
  // 작은 정사각 썸네일 하나로 줄여서 텍스트 중심 리스트로 (빈님 피드백 반영)
  // 정렬은 최신순 고정(빈님 확인: "수술후기 들어가면 최신글이 나와야지" / BEST·베스트순 없앰)
  const dateSorted = [...reviews].sort((a, b) => (b.udate||'').localeCompare(a.udate||''));
  const rows = dateSorted.map((r) => {
    const masked = maskName(r.writer);
    const desc = r.contents_text.slice(0, 60).replace(/\s+/g,' ').trim();
    const thumb = r.photos.length
      ? `<div class="review-row-thumb"><img src="${PHOTO_BASE}1/${r.photos[0]}" alt="" loading="lazy"></div>`
      : `<div class="review-row-thumb-empty"></div>`;
    // 복수 카테고리 태그된 글은 실제 페이지가 대표(primary) 카테고리 쪽에만 생성됨 —
    // 지금 이 목록이 대표 카테고리가 아니면(교차 노출) 실제 위치로 경로를 잡아줌
    const isPrimary = r.cat[0] === cfg.catPath && r.cat[1] === cfg.subDir;
    const href = isPrimary ? `${r.num}/` : `${root}${r.cat[0]}/${r.cat[1]}/reviews/${r.num}/`;
    return `      <a href="${href}" class="review-row">
        ${thumb}
        <div class="review-row-body">
          <p class="review-row-title">${esc(r.subject.trim() || cfg.subName + ' 후기')}</p>
          <p class="review-row-desc">${esc(desc)}</p>
          <p class="review-row-meta">${esc(masked)}님 후기 · ${(r.udate||'').slice(0,7).replace('-','.')}</p>
        </div>
      </a>`;
  }).join('\n');

  const listSection = `    <div class="review-list review-list-cols" id="review-list">
${rows}
    </div>
    <div style="text-align:center;margin-top:2rem;">
      <button type="button" class="sort-btn" id="loadMoreReviews" style="padding:0.7rem 2rem;">더보기</button>
    </div>`;

  const paginationScript = `
    <script>
      (function(){
        var PAGE = 30;
        var list = document.getElementById('review-list');
        var items = Array.prototype.slice.call(list.querySelectorAll('.review-row'));
        var moreBtn = document.getElementById('loadMoreReviews');
        var shown = PAGE;
        function apply(){
          items.forEach(function(el, i){ el.hidden = i >= shown; });
          if (moreBtn) moreBtn.hidden = shown >= items.length;
        }
        if (moreBtn) moreBtn.addEventListener('click', function(){ shown += PAGE; apply(); });
        apply();
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
${listSection}
${paginationScript}
  </div>
</section>
${FOOTER(root)}
</body>
</html>`;
}

// ── 실행 — 분류(cat)되고 불만어감(flag_bad) 아닌 모든 후기를, 서브카테고리별로 전부 발행 ──
const curated = JSON.parse(readFileSync(join(ROOT, 'postscript_curated.json'), 'utf8'));
// isauth='Y'(본원 인증완료) 아닌 글은 절대 발행하지 않음 — 빈님 확인: "미인증 글은 올리면 안 됨"
// flag_bad(환불/불만/실망 단어 포함) 35건은 사람이 직접 검토 후 발행 승인 — 빈님 확인: "니가 고른거라면 그냥 다 올려줘"
const usable = curated.filter(r => r.cat && r.isauth === 'Y');

// 페이지 생성은 대표(primary=cat) 카테고리 위치에서만 1회 — URL 중복 방지
const primaryGroups = new Map(); // "catPath/subDir" -> rows[]
for (const r of usable) {
  const key = r.cat.join('/');
  if (!primaryGroups.has(key)) primaryGroups.set(key, []);
  primaryGroups.get(key).push(r);
}

// 목록 노출은 제목에서 태그된 모든 카테고리(cats) 기준 — 복합시술 후기가
// 관련 카테고리 전부에 다 보이게 (빈님 확인: "제목에 보이는 모든 키워드를 카테고리로")
const listingGroups = new Map();
for (const r of usable) {
  for (const c of (r.cats && r.cats.length ? r.cats : [r.cat])) {
    const key = c.join('/');
    if (!listingGroups.has(key)) listingGroups.set(key, []);
    listingGroups.get(key).push(r);
  }
}

console.log(`대상 서브카테고리: ${listingGroups.size}개, 총 후기: ${usable.length}건\n`);

let totalNew = 0, totalSkipped = 0;
for (const [key, rows] of [...primaryGroups.entries()].sort((a, b) => b[1].length - a[1].length)) {
  const [catPath, subDir] = key.split('/');
  const cfg = { catPath, subDir, subName: findSubName(catPath, subDir) };
  const sorted = rows.sort((a, b) => b.score - a.score);
  const baseDir = join(ROOT, catPath, subDir, 'reviews');
  mkdirSync(baseDir, { recursive: true });

  let newInGroup = 0;
  for (const r of sorted) {
    const dir = join(baseDir, String(r.num));
    const isNew = !existsSync(dir);
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, 'index.html'), generateReviewPage(r, cfg), 'utf8'); // 항상 재생성(템플릿 변경 시 기존 글도 반영)
    if (isNew) { totalNew++; newInGroup++; } else { totalSkipped++; }
  }
  console.log(`${key} — ${cfg.subName} 페이지 생성 (${sorted.length}건, 신규 ${newInGroup})`);
}

// 목록(index.html)은 listingGroups 기준으로 별도 생성 — primaryGroups에 없던
// 서브카테고리도(교차 태그만 있는 경우) 목록은 만들어야 하므로 전체를 순회
for (const [key, rows] of [...listingGroups.entries()].sort((a, b) => b[1].length - a[1].length)) {
  const [catPath, subDir] = key.split('/');
  const cfg = { catPath, subDir, subName: findSubName(catPath, subDir) };
  const sorted = [...rows].sort((a, b) => b.score - a.score);
  const baseDir = join(ROOT, catPath, subDir, 'reviews');
  mkdirSync(baseDir, { recursive: true });
  writeFileSync(join(baseDir, 'index.html'), generateReviewIndex(sorted, cfg), 'utf8');
}

console.log(`\n완료 — 신규 페이지 ${totalNew}건, 이미 있어서 건너뜀 ${totalSkipped}건, 목록 페이지 ${listingGroups.size}개`);
