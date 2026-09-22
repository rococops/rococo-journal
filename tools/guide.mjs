// "성형 가이드" 섹션 — 원장님 케이스 글을 근거로 정리한 주제별 설명글.
// api/publish.js(발행/미리보기)와 로컬 재생성 스크립트가 함께 쓰는 순수 함수 모음.
//
// 저장 구조: guide/posts.json(목록 데이터) + guide/{slug}/index.html(글) + guide/index.html(목록)
import { navHtml } from './nav.mjs';

export const GUIDE = {
  path: 'guide',
  name: '성형 가이드',
  nameEn: 'Plastic Surgery Guide',
  headline: '성형 가이드',
  intro: '김상호 원장의 실제 수술 케이스를 바탕으로, 환자분들이 가장 많이 궁금해하시는 재수술·코·광대·눈 수술 이야기를 주제별로 정리했습니다.',
  listTitle: '성형 가이드 — 구축코·코재수술·광대축소 궁금증 정리 | 로코코성형외과 김상호 원장',
  listDescription: '구축코, 코재수술, 비공내리기, 퀵광대 등 환자분들이 자주 검색하는 성형 주제를 김상호 원장의 실제 케이스를 바탕으로 정리한 가이드입니다.',
};
export const SITE_BASE = 'https://journal.rococops.com';
const DEFAULT_IMAGE = 'images/thumbnails/2-2.jpg';
const BRAND_FULL = '로코코성형외과 김상호 원장';
const BRAND_SHORT = '로코코성형외과';
const MAX_TITLE = 60;

export function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
const jsonStr = (s) => String(s == null ? '' : s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, ' ');

// 이미지 주소는 우리 사이트 경로 또는 https만 허용 (javascript: 등 차단)
function safeUrl(u) {
  u = String(u || '').trim();
  return (/^https:\/\//i.test(u) || u.startsWith('/')) ? u : '';
}

function inline(s) {
  return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}

// 본문 문법(원장님이 초안함에서 편집하는 형식):
//   ## 소제목 / ### 작은 소제목 / - 목록 / 빈 줄로 문단 구분 / **굵게**
//   [[img:주소|사진 설명]]  ← 사진 자리
export function renderBody(text, altFallback = '') {
  const blocks = String(text || '').replace(/\r/g, '').split(/\n{2,}/).map(b => b.trim()).filter(Boolean);
  const out = [];
  for (const b of blocks) {
    const img = b.match(/^\[\[img:(.+?)(?:\|(.*?))?\]\]$/s);
    if (img) {
      const url = safeUrl(img[1]);
      if (!url) continue;
      const cap = (img[2] || '').trim();
      out.push(`<figure class="guide-figure"><img src="${esc(url)}" alt="${esc(cap || altFallback)}" loading="lazy">${cap ? `<figcaption>${esc(cap)}</figcaption>` : ''}</figure>`);
    } else if (/^### /.test(b)) {
      out.push(`<h3>${inline(b.slice(4))}</h3>`);
    } else if (/^## /.test(b)) {
      out.push(`<h2>${inline(b.slice(3))}</h2>`);
    } else if (b.split('\n').every(l => /^- /.test(l))) {
      out.push('<ul>' + b.split('\n').map(l => `<li>${inline(l.slice(2))}</li>`).join('') + '</ul>');
    } else {
      out.push(`<p>${inline(b.replace(/\n/g, ' '))}</p>`);
    }
  }
  return out.join('\n        ');
}

export function firstImage(body) {
  const m = String(body || '').match(/\[\[img:(.+?)(?:\|.*?)?\]\]/s);
  return m ? safeUrl(m[1]) : '';
}

// 검색 결과용 제목: 사람이 읽는 H1과 별개로, 글마다 검색 키워드를 담은 <title>을 둘 수 있음
export function metaTitleOf(post) {
  const base = (post.metaTitle || post.title || '').trim();
  const full = `${base} | ${BRAND_FULL}`;
  return full.length > MAX_TITLE ? `${base} | ${BRAND_SHORT}` : full;
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
    <div class="footer-bottom"><p>© 2025 Rococo Plastic Surgery. All rights reserved.</p></div>
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

function headTop(root, title, description, canonical, ogImage, ogType, schema, preview) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
${preview ? `<base href="${canonical}">\n` : ''}<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:image" content="${esc(ogImage)}">
<meta property="og:url" content="${canonical}">
<meta property="og:type" content="${ogType}">
<link rel="canonical" href="${canonical}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<script type="application/ld+json">
${schema}
</script>
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="${root}css/style.css">
</head>`;
}

const HEADER = (root, nav) => `<div class="gnb-overlay" id="gnbOverlay"></div>
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="${root}" class="logo"><span class="logo-main">ROCOCO</span><span class="logo-sub">Journal</span></a>
    <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
    ${nav}
  </div>
</header>`;

// ── 글 페이지 ──
// post: { slug, title, metaTitle?, summary, keyword, tag, date, body, sources:[{title,url}] }
// others: 사이드바에 보여줄 다른 가이드 글 목록 / opts.preview: 미리보기용(<base> 삽입)
export function generateGuidePage(post, others = [], opts = {}) {
  const root = '../../';
  const nav = navHtml(root, 'guide');
  const canonical = `${SITE_BASE}/${GUIDE.path}/${post.slug}/`;
  const metaTitle = metaTitleOf(post);
  const description = String(post.summary || '').trim().slice(0, 160);
  const hero = firstImage(post.body) || `${root}${DEFAULT_IMAGE}`;
  const ogImage = hero.startsWith('/') ? SITE_BASE + hero : (hero.startsWith('../') ? `${SITE_BASE}/${DEFAULT_IMAGE}` : hero);
  const date = post.date || new Date().toISOString().slice(0, 10);
  const tag = post.tag || GUIDE.name;
  const titleJ = jsonStr(post.title), descJ = jsonStr(description);

  const schema = `[{"@context":"https://schema.org","@type":"MedicalWebPage","headline":"${titleJ}","description":"${descJ}","url":"${canonical}","image":"${esc(ogImage)}","datePublished":"${date}","dateModified":"${date}","inLanguage":"ko-KR","author":{"@type":"Physician","name":"김상호","honorificPrefix":"원장","worksFor":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"}},"publisher":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"},"medicalAudience":{"@type":"MedicalAudience","audienceType":"Patient"},"specialty":"Plastic Surgery"},{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"${SITE_BASE}/"},{"@type":"ListItem","position":2,"name":"${GUIDE.name}","item":"${SITE_BASE}/${GUIDE.path}/"},{"@type":"ListItem","position":3,"name":"${titleJ}","item":"${canonical}"}]}]`;

  const sources = (post.sources || []).filter(s => s && s.url);
  const sourcesHtml = sources.length
    ? `<div class="guide-sources">
          <p class="guide-sources-title">이 글은 아래 실제 케이스 글을 바탕으로 정리했습니다</p>
          <ul>${sources.map(s => `<li><a href="${esc(s.url)}">${esc(s.title || s.url)}</a></li>`).join('')}</ul>
        </div>`
    : '';

  const related = others.filter(o => o.slug !== post.slug).slice(0, 5);
  const relatedHtml = related.length
    ? `<div class="sidebar-related">
          <p class="sidebar-title">다른 가이드 글</p>
          ${related.map(o => `<a href="${root}${GUIDE.path}/${esc(o.slug)}/" class="related-link">${esc(o.title)}</a>`).join('\n          ')}
        </div>`
    : '';

  return `${headTop(root, metaTitle, description, canonical, ogImage, 'article', schema, opts.preview)}
<body>
${HEADER(root, nav)}
<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb">
      <a href="${root}">홈</a><span>›</span>
      <a href="${root}${GUIDE.path}/">${GUIDE.name}</a><span>›</span>
      <span>${esc(post.title.slice(0, 24))}${post.title.length > 24 ? '...' : ''}</span>
    </div>
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <span class="eyebrow">${GUIDE.nameEn}</span>
        <h1 class="article-title">${esc(post.title)}</h1>
        <p class="article-summary">${esc(description)}</p>
        <div class="article-meta">
          <span class="meta-author">김상호 원장</span><span class="dot">·</span>
          <span class="meta-cat">${esc(tag)}</span><span class="dot">·</span>
          <span class="meta-clinic">로코코성형외과</span>
        </div>
      </div>
      <div class="article-hero-img"><img src="${esc(hero)}" alt="${esc(post.title)}" loading="eager"></div>
    </div>
  </div>
</section>
<article class="article-body">
  <div class="container">
    <div class="article-layout">
      <div class="article-content">
        ${renderBody(post.body, post.title)}
        ${sourcesHtml}
        <div class="inline-cta">
          <p class="inline-cta-text">내 경우에도 해당되는지 궁금하신가요?</p>
          <a href="${root}counsel/online/?from=${encodeURIComponent(post.title)}" class="inline-cta-btn">김상호 원장에게 직접 상담하기 →</a>
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
          <a href="${root}counsel/online/?from=${encodeURIComponent(post.title)}" class="sidebar-btn">상담 신청하기 →</a>
        </div>
        ${relatedHtml}
        <div class="sidebar-related">
          <p class="sidebar-title">${GUIDE.name}</p>
          <a href="${root}${GUIDE.path}/" class="related-link">전체 가이드 보기 →</a>
        </div>
      </aside>
    </div>
  </div>
</article>
${FOOTER(root)}
</body>
</html>`;
}

// ── 목록 페이지 ──
export function generateGuideIndex(posts) {
  const root = '../';
  const nav = navHtml(root, 'guide');
  const canonical = `${SITE_BASE}/${GUIDE.path}/`;
  const sorted = [...posts].sort((a, b) => (b.date || '').localeCompare(a.date || '') || String(b.slug).localeCompare(String(a.slug)));
  const ogImage = `${SITE_BASE}/${DEFAULT_IMAGE}`;

  const schema = `[{"@context":"https://schema.org","@type":"CollectionPage","name":"${GUIDE.name}","description":"${jsonStr(GUIDE.listDescription)}","url":"${canonical}","inLanguage":"ko","publisher":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"}},{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"${SITE_BASE}/"},{"@type":"ListItem","position":2,"name":"${GUIDE.name}","item":"${canonical}"}]}]`;

  const cards = sorted.map(p => {
    const img = p.image || `${root}${DEFAULT_IMAGE}`;
    const href = `${esc(p.slug)}/`;
    return `      <a href="${href}" class="card" data-date="${esc(p.date || '')}">
        <div class="card-img">
          <img src="${esc(img)}" alt="${esc(p.title)}" loading="lazy">
          <span class="card-tag">${esc(p.tag || GUIDE.name)}</span>
        </div>
        <div class="card-body">
          <p class="card-title">${esc(p.title)}</p>
          <p class="card-desc">${esc(String(p.summary || '').slice(0, 90))}</p>
          <span class="card-date">${esc((p.date || '').slice(0, 7).replace('-', '. '))}</span>
        </div>
      </a>`;
  }).join('\n');

  return `${headTop(root, GUIDE.listTitle, GUIDE.listDescription, canonical, ogImage, 'website', schema, false)}
<body>
${HEADER(root, nav)}
<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb"><a href="${root}">홈</a><span>›</span><span>${GUIDE.name}</span></div>
    <div class="article-hero-inner" style="grid-template-columns: 1fr;">
      <div class="article-hero-text">
        <span class="eyebrow">${GUIDE.nameEn}</span>
        <h1 class="article-title">${GUIDE.headline}</h1>
        <p class="article-summary">${GUIDE.intro}</p>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head">
      <h2 class="section-label">가이드 글 (${sorted.length}편)</h2>
    </div>
${sorted.length ? `    <div class="card-grid">\n${cards}\n    </div>` : '    <p style="color:var(--gray-400);padding:2rem 0">곧 첫 번째 가이드가 올라옵니다.</p>'}
  </div>
</section>
${FOOTER(root)}
</body>
</html>`;
}
