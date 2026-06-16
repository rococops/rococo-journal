import * as cheerio from 'cheerio';

const GITHUB_REPO = 'rococops/rococo-journal';
const GITHUB_API  = 'https://api.github.com';
const THUMB_BASE  = 'https://journal.rococops.com/images/thumbnails/';
const SITE_BASE   = 'https://journal.rococops.com';

// ── 카테고리 메타 ──────────────────────────────────────────────
const SUBCATS = [
  {catPath:'cheekbone', subDir:'quick',          subName:'15분 광대축소술',       subNameEn:'Quick Cheekbone Reduction', keywords:'퀵광대 광대축소술',            thumbPool:['1-1.jpg','1-2.jpg','1-3.jpg','1-4.jpg']},
  {catPath:'cheekbone', subDir:'fat-graft',       subName:'심부볼·관자 지방이식',  subNameEn:'Deep Cheek & Temple Fat Graft', keywords:'심부볼지방이식 관자지방이식', thumbPool:['1-1.jpg','1-2.jpg']},
  {catPath:'cheekbone', subDir:'liposuction',     subName:'광대라인 지방흡입',     subNameEn:'Cheekline Liposuction',     keywords:'광대지방흡입 얼굴지방흡입',    thumbPool:['1-1.jpg','1-2.jpg']},
  {catPath:'cheekbone', subDir:'rear',            subName:'뒷광대축소술',          subNameEn:'Rear Cheekbone Reduction',  keywords:'뒷광대축소술 뒷광대',          thumbPool:['1-1.jpg','1-2.jpg']},
  {catPath:'cheekbone', subDir:'revision',        subName:'광대 재수술',           subNameEn:'Cheekbone Revision',        keywords:'광대재수술 광대수술재수술',    thumbPool:['1-1.jpg','1-2.jpg']},
  {catPath:'nose',      subDir:'column',          subName:'진료단상',              subNameEn:'Rhinoplasty Column',        keywords:'코성형 코성형칼럼',            thumbPool:['2-1.jpg','2-2.jpg','2-3.jpg','2-4.jpg']},
  {catPath:'nose',      subDir:'revision',        subName:'코재수술',              subNameEn:'Rhinoplasty Revision',      keywords:'코재수술 코성형재수술',        thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'rib-cartilage',   subName:'늑연골 명품코성형',     subNameEn:'Rib Cartilage Rhinoplasty', keywords:'자가늑연골 늑연골코성형',      thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'septal',          subName:'비중격연골 코성형',     subNameEn:'Septal Cartilage Rhinoplasty', keywords:'비중격연골코성형',          thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'scarless',        subName:'흉터없는 코성형',       subNameEn:'Scarless Rhinoplasty',      keywords:'흉터없는코성형 비개방코성형',  thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'hump',            subName:'매부리코',              subNameEn:'Hump Nose Correction',      keywords:'매부리코 매부리코수술',        thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'bulbous',         subName:'복코',                  subNameEn:'Bulbous Nose Correction',   keywords:'복코성형 복코교정',            thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'osteotomy',       subName:'절골술',                subNameEn:'Osteotomy',                 keywords:'절골술 콧대좁히기',            thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'long',            subName:'긴코',                  subNameEn:'Long Nose Correction',      keywords:'긴코수술 긴코교정',            thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'columella',       subName:'비주성형',              subNameEn:'Columella Plasty',          keywords:'비주내리기 비주성형',          thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'cat',             subName:'비순각 고양이 입매교정',subNameEn:'Cat Eye Lip Line',          keywords:'비순각수술 입매교정',          thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nose',      subDir:'male',            subName:'남자의 코성형',         subNameEn:'Rhinoplasty for Men',       keywords:'남자코성형 남자성형',          thumbPool:['8-1.jpg','8-2.jpg']},
  {catPath:'nose',      subDir:'rhinitis',        subName:'비염수술',              subNameEn:'Rhinitis Surgery',          keywords:'비염수술 하비갑개축소술',      thumbPool:['2-1.jpg','2-2.jpg']},
  {catPath:'nostril',   subDir:'alar-lowering',   subName:'비공내리기',            subNameEn:'Alar Lowering',             keywords:'비공내리기 콧구멍내리기',      thumbPool:['3-1.jpg','3-2.jpg','3-3.jpg']},
  {catPath:'nostril',   subDir:'alar-raising',    subName:'콧날개올리기',          subNameEn:'Alar Raising',              keywords:'콧날개올리기 콧날개성형',      thumbPool:['3-1.jpg','3-2.jpg']},
  {catPath:'nostril',   subDir:'v-shape',         subName:'V형 콧구멍교정',        subNameEn:'V-shape Nostril Correction',keywords:'V형콧구멍교정 콧구멍교정',     thumbPool:['3-1.jpg','3-2.jpg']},
  {catPath:'nostril',   subDir:'reduction',       subName:'콧구멍축소술',          subNameEn:'Nostril Reduction',         keywords:'콧구멍축소술 콧구멍줄이기',   thumbPool:['3-1.jpg','3-2.jpg']},
  {catPath:'nostril',   subDir:'alar-base',       subName:'콧볼축소술',            subNameEn:'Alar Base Reduction',       keywords:'콧볼축소술 콧볼줄이기',        thumbPool:['3-1.jpg','3-2.jpg']},
  {catPath:'forehead',  subDir:'endoscopic',      subName:'내시경 이마거상술',     subNameEn:'Endoscopic Brow Lift',      keywords:'내시경이마거상술 이마거상술',  thumbPool:['4-1.jpg','4-2.jpg']},
  {catPath:'forehead',  subDir:'reduction',       subName:'이마축소술',            subNameEn:'Forehead Reduction',        keywords:'이마축소술 이마성형',          thumbPool:['4-1.jpg','4-2.jpg']},
  {catPath:'eye',       subDir:'correction',      subName:'눈매교정술',            subNameEn:'Ptosis Correction',         keywords:'눈매교정 비절개눈매교정',      thumbPool:['9-1.jpg','9-2.jpg','9-3.jpg']},
  {catPath:'eye',       subDir:'double',          subName:'쌍커풀 자연유착법',     subNameEn:'Natural Adhesion Double Eyelid', keywords:'쌍커풀수술 자연유착법',   thumbPool:['9-1.jpg','9-2.jpg']},
  {catPath:'eye',       subDir:'incision',        subName:'트임성형',              subNameEn:'Canthoplasty',              keywords:'뒷트임 밑트임 앞트임',         thumbPool:['9-1.jpg','9-2.jpg']},
  {catPath:'eye',       subDir:'brow-lift',       subName:'눈썹하거상술',          subNameEn:'Sub-brow Lift',             keywords:'눈썹하거상술 눈썹거상',        thumbPool:['9-1.jpg','9-2.jpg']},
  {catPath:'eye',       subDir:'fat-graft',       subName:'꺼진눈 지방이식',       subNameEn:'Sunken Eye Fat Graft',      keywords:'꺼진눈지방이식 눈지방이식',    thumbPool:['9-1.jpg','9-2.jpg']},
  {catPath:'eye',       subDir:'lower-fat',       subName:'눈밑지방 재배치',       subNameEn:'Lower Eyelid Fat Repositioning', keywords:'눈밑지방재배치 눈밑성형',  thumbPool:['9-1.jpg','9-2.jpg']},
  {catPath:'anti-aging',subDir:'blepharoplasty',  subName:'상·하안검성형',         subNameEn:'Upper & Lower Blepharoplasty', keywords:'상안검성형 하안검성형',      thumbPool:['6-1.jpg','6-2.jpg']},
  {catPath:'anti-aging',subDir:'lifting',         subName:'엘라스티꿈 실리프팅',   subNameEn:'Elasticum Thread Lift',     keywords:'실리프팅 엘라스티꿈리프팅',   thumbPool:['6-1.jpg','6-2.jpg']},
  {catPath:'anti-aging',subDir:'filler-botox',    subName:'필러·보톡스',           subNameEn:'Filler & Botox',            keywords:'필러 보톡스',                  thumbPool:['6-1.jpg','6-2.jpg']},
  {catPath:'anti-aging',subDir:'chin',            subName:'무턱성형',              subNameEn:'Chin Augmentation',         keywords:'무턱수술 무턱성형',            thumbPool:['5-1.jpg','5-2.jpg']},
  {catPath:'anti-aging',subDir:'fat-graft',       subName:'미세지방이식',          subNameEn:'Micro Fat Grafting',        keywords:'미세지방이식 지방이식',        thumbPool:['6-1.jpg','6-2.jpg']},
];

const CAT_NAMES = {
  cheekbone: '광대성형', nose: '코성형', nostril: '콧구멍성형',
  forehead: '이마성형', eye: '눈성형', 'anti-aging': '동안성형',
};

// ── HTML 정제 ──────────────────────────────────────────────────
function fixSrc(src) {
  if (!src) return null;
  src = src.trim();
  if (src.startsWith('//')) return 'https:' + src;
  if (src.startsWith('http://')) return 'https://' + src.slice(7);
  if (src.startsWith('https://')) return src;
  if (src.startsWith('/')) return 'https://rococops.com' + src;
  return 'https://rococops.com/' + src;
}

function cleanText(t) {
  if (!t) return '';
  return t
    .replace(/[​‌‍﻿]/g, '')
    .replace(/ /g, ' ')
    .replace(/https?:\/\/\S+|www\.\S+/gi, '')
    .replace(/\^[\^_\-]*\^[;*]?/g, '')
    .replace(/원문\s*(링크|보기)\s*:?/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function esc(s) {
  return String(s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function buildArticleBlocks(html, altText) {
  const $ = cheerio.load(html || '');
  const blocks = [];
  const images = [];
  const alt = esc(altText);

  const BLOCK_TAGS = new Set(['p','div','li','td','th','h1','h2','h3','h4','blockquote']);

  function walk(el) {
    if (el.type === 'text') {
      const t = cleanText(el.data || '');
      if (t) blocks.push({type:'text', val:t});
      return;
    }
    if (el.type !== 'tag') return;
    const tag = el.name.toLowerCase();
    if (tag === 'script' || tag === 'style') return;

    if (tag === 'img') {
      const src = fixSrc($(el).attr('src'));
      if (src) { blocks.push({type:'img', val:src}); images.push(src); }
      return;
    }

    // 네이버 관련글 박스
    if (tag === 'blockquote') {
      const style = $(el).attr('style') || '';
      if (style.includes('se2.naver.com')) {
        const a = $(el).find('a').first();
        let href = (a.attr('href') || '').trim().replace(/(%E2%80%8B|[​‌‍﻿])+$/i, '');
        if (href.startsWith('http://')) href = 'https://' + href.slice(7);
        let title = '';
        $(el).find('p,span').each((_, el2) => {
          const t = cleanText($(el2).text());
          if (t && !t.startsWith('http')) { title = t; return false; }
        });
        if (href) blocks.push({type:'related', val:{href, title: title || '관련 글 보기'}});
        return;
      }
    }

    if (BLOCK_TAGS.has(tag)) {
      let textParts = [];
      $(el).contents().each((_, child) => {
        if (child.type === 'tag' && (child.name === 'img' || $(child).find('img').length)) {
          const t = cleanText(textParts.join(' '));
          if (t) { blocks.push({type:'text', val:t}); textParts = []; }
          walk(child);
        } else {
          textParts.push(child.type === 'text' ? (child.data || '') : $(child).text());
        }
      });
      const t = cleanText(textParts.join(' '));
      if (t) blocks.push({type:'text', val:t});
      return;
    }

    $(el).contents().each((_, child) => walk(child));
  }

  $.root().children().each((_, el) => walk(el));

  // 연속 중복 이미지 제거
  const out = [];
  let lastImg = null;
  for (const b of blocks) {
    if (b.type === 'img' && b.val === lastImg) continue;
    out.push(b);
    lastImg = b.type === 'img' ? b.val : null;
  }

  const parts = out.map(b => {
    if (b.type === 'text') return `<p>${esc(b.val)}</p>`;
    if (b.type === 'related') return `<p class="related-post-link"><a href="${b.val.href}" target="_blank" rel="noopener">${esc(b.val.title)} →</a></p>`;
    return `<img src="${b.val}" alt="${alt}" loading="lazy">`;
  });

  return { html: parts.join('\n        '), images };
}

// ── 페이지 템플릿 ──────────────────────────────────────────────
function navHtml(root, activeCat) {
  const a = (cat) => cat === activeCat ? 'active' : '';
  return `<nav class="gnb" id="gnb">
      <div class="gnb-header">
        <span class="gnb-title">Menu</span>
        <button class="gnb-close" id="gnbClose" aria-label="메뉴 닫기">&#x2715;</button>
      </div>
      <ul>
        <li class="has-sub ${a('cheekbone')}"><a href="${root}cheekbone/">광대성형</a>
          <ul class="sub-menu">
            <li><a href="${root}cheekbone/quick/">15분 광대축소술</a></li>
            <li><a href="${root}cheekbone/fat-graft/">심부볼·관자 지방이식</a></li>
            <li><a href="${root}cheekbone/liposuction/">광대라인 지방흡입</a></li>
            <li><a href="${root}cheekbone/rear/">뒷광대축소술</a></li>
            <li><a href="${root}cheekbone/revision/">광대 재수술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('nose')}"><a href="${root}nose/">코성형</a>
          <ul class="sub-menu">
            <li><a href="${root}nose/column/">진료단상</a></li>
            <li><a href="${root}nose/revision/">코재수술</a></li>
            <li><a href="${root}nose/rib-cartilage/">늑연골 명품코성형</a></li>
            <li><a href="${root}nose/septal/">비중격연골 코성형</a></li>
            <li><a href="${root}nose/scarless/">흉터없는 코성형</a></li>
            <li><a href="${root}nose/hump/">매부리코</a></li>
            <li><a href="${root}nose/bulbous/">복코</a></li>
            <li><a href="${root}nose/osteotomy/">절골술</a></li>
            <li><a href="${root}nose/long/">긴코</a></li>
            <li><a href="${root}nose/columella/">비주성형</a></li>
            <li><a href="${root}nose/cat/">비순각 고양이 입매교정</a></li>
            <li><a href="${root}nose/male/">남자의 코성형</a></li>
            <li><a href="${root}nose/rhinitis/">비염수술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('nostril')}"><a href="${root}nostril/">콧구멍성형</a>
          <ul class="sub-menu">
            <li><a href="${root}nostril/alar-lowering/">비공내리기</a></li>
            <li><a href="${root}nostril/alar-raising/">콧날개올리기</a></li>
            <li><a href="${root}nostril/v-shape/">V형 콧구멍교정</a></li>
            <li><a href="${root}nostril/reduction/">콧구멍축소술</a></li>
            <li><a href="${root}nostril/alar-base/">콧볼축소술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('forehead')}"><a href="${root}forehead/">이마성형</a>
          <ul class="sub-menu">
            <li><a href="${root}forehead/endoscopic/">내시경 이마거상술</a></li>
            <li><a href="${root}forehead/reduction/">이마축소술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('eye')}"><a href="${root}eye/">눈성형</a>
          <ul class="sub-menu">
            <li><a href="${root}eye/correction/">눈매교정술</a></li>
            <li><a href="${root}eye/incision/">트임성형</a></li>
            <li><a href="${root}eye/double/">쌍커풀 자연유착법</a></li>
            <li><a href="${root}eye/lower-fat/">눈밑지방 재배치</a></li>
            <li><a href="${root}eye/fat-graft/">꺼진눈 지방이식</a></li>
            <li><a href="${root}eye/brow-lift/">눈썹하거상술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('anti-aging')}"><a href="${root}anti-aging/">동안성형</a>
          <ul class="sub-menu">
            <li><a href="${root}anti-aging/chin/">무턱성형</a></li>
            <li><a href="${root}anti-aging/fat-graft/">미세지방이식</a></li>
            <li><a href="${root}anti-aging/blepharoplasty/">상·하안검성형</a></li>
            <li><a href="${root}anti-aging/lifting/">엘라스티꿈 실리프팅</a></li>
            <li><a href="${root}anti-aging/filler-botox/">필러·보톡스</a></li>
          </ul>
        </li>
        <li class="has-sub"><a href="${root}about/">About</a>
          <ul class="sub-menu">
            <li><a href="${root}about/">로코코 소개</a></li>
            <li><a href="${root}about/philosophy/">철학과 강점</a></li>
            <li><a href="${root}about/location/">오시는 길·진료시간</a></li>
          </ul>
        </li>
        <li><a href="${root}counsel/">상담·예약</a></li>
        <li><a href="${root}cases/" class="btn-consult">전후사진</a></li>
      </ul>
    </nav>`;
}

function generatePage({title, metaTitle, description, ogImage, ogUrl, date,
  catPath, catName, subDir, subName, subNameEn, heroImage, content, originUrl}) {
  const root = '../../../';
  const listRoot = '../';
  const titleJ = title.replace(/"/g,'\\"');
  const descJ  = description.replace(/"/g,'\\"');
  const catJ   = catName.replace(/"/g,'\\"');
  const subJ   = subName.replace(/"/g,'\\"');
  const originCard = originUrl
    ? `        <div class="sidebar-card">
          <p class="sidebar-title">원본 글 보기</p>
          <p class="sidebar-desc">로코코성형외과 블로그에서 이 글의 원본을 확인할 수 있습니다</p>
          <a href="${originUrl}" class="sidebar-btn" target="_blank" rel="noopener">원문 보러가기 →</a>
        </div>`
    : '';
  const nav = navHtml(root, catPath);
  return `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(metaTitle)}</title>
<meta name="description" content="${esc(description)}">
<meta property="og:title" content="${esc(metaTitle)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:image" content="${ogImage}">
<meta property="og:url" content="${ogUrl}">
<meta property="og:type" content="article">
<link rel="canonical" href="${ogUrl}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<script type="application/ld+json">
[{"@context":"https://schema.org","@type":"MedicalWebPage","headline":"${titleJ}","description":"${descJ}","url":"${ogUrl}","image":"${ogImage}","datePublished":"${date}","dateModified":"${date}","inLanguage":"ko-KR","author":{"@type":"Physician","name":"김상호","honorificPrefix":"원장","worksFor":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"}},"publisher":{"@type":"MedicalBusiness","name":"로코코성형외과","url":"${SITE_BASE}"},"medicalAudience":{"@type":"MedicalAudience","audienceType":"Patient"},"specialty":"Plastic Surgery","about":{"@type":"MedicalProcedure","name":"${subJ}"}},{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"${SITE_BASE}/"},{"@type":"ListItem","position":2,"name":"${catJ}","item":"${SITE_BASE}/${catPath}/"},{"@type":"ListItem","position":3,"name":"${subJ}","item":"${SITE_BASE}/${catPath}/${subDir}/"},{"@type":"ListItem","position":4,"name":"${titleJ}","item":"${ogUrl}"}]}]
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
      <a href="${root}${catPath}/">${catName}</a><span>›</span>
      <a href="${listRoot}">${subName}</a><span>›</span>
      <span>${esc(title.slice(0,24))}${title.length>24?'...':''}</span>
    </div>
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <span class="eyebrow">${subNameEn}</span>
        <h1 class="article-title">${esc(title)}</h1>
        <p class="article-summary">${esc(description)}</p>
        <div class="article-meta">
          <span class="meta-author">김상호 원장</span><span class="dot">·</span>
          <span class="meta-cat">${subName}</span><span class="dot">·</span>
          <span class="meta-clinic">로코코성형외과</span>
        </div>
      </div>
      <div class="article-hero-img"><img src="${heroImage}" alt="${esc(subName)} 로코코성형외과" loading="eager"></div>
    </div>
  </div>
</section>
<article class="article-body">
  <div class="container">
    <div class="article-layout">
      <div class="article-content">
        ${content}
        <div class="inline-cta">
          <p class="inline-cta-text">${subName}에 대해 더 궁금한 점이 있으신가요?</p>
          <a href="${root}counsel/?from=${subName}" class="inline-cta-btn">김상호 원장에게 직접 상담하기 →</a>
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
          <a href="${root}counsel/?from=${subName}" class="sidebar-btn">상담 신청하기 →</a>
        </div>
        <div class="sidebar-related">
          <p class="sidebar-title">${subName} 다른 글</p>
          <a href="${listRoot}" class="related-link">${subName} 목록 보기 →</a>
        </div>
${originCard}
      </aside>
    </div>
  </div>
</article>
<section class="cta-section">
  <div class="container">
    <div class="cta-grid">
      <a href="${root}cases/" class="cta-card"><div class="cta-card-inner"><span class="cta-label">${subName} 전후사진</span><h3 class="cta-title">실제 수술 결과를<br>직접 확인하세요</h3><p class="cta-desc">로코코에서 진행한 실제 케이스 사진을 확인하세요</p><span class="cta-btn">전후사진 보기 →</span></div></a>
      <a href="${root}counsel/?from=${subName}" class="cta-card"><div class="cta-card-inner"><span class="cta-label">온라인 상담</span><h3 class="cta-title">궁금한 점을<br>직접 물어보세요</h3><p class="cta-desc">김상호 원장이 직접 답변해 드립니다</p><span class="cta-btn">상담 신청하기 →</span></div></a>
    </div>
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
        <p>월·금 — 09:00 ~ 19:00</p><p>화·수·목 — 09:00 ~ 18:00</p>
        <p>토 — 09:00 ~ 13:00</p><p>일·공휴일 휴진</p>
      </div>
      <div class="footer-links">
        <p class="footer-title">바로가기</p>
        <a href="https://rococops.com" target="_blank">기존 홈페이지</a>
        <a href="${root}counsel/">온라인 상담</a>
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
</a>
</body>
</html>`;
}

// ── GitHub API ──────────────────────────────────────────────────
async function ghFetch(path, token, opts = {}) {
  const res = await fetch(`${GITHUB_API}/repos/${GITHUB_REPO}/contents/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    ...opts,
  });
  return res;
}

async function getNextSlug(catPath, subDir, token) {
  const res = await ghFetch(`${catPath}/${subDir}`, token);
  if (!res.ok) return '1001';
  const items = await res.json();
  let max = 1000;
  for (const item of items) {
    if (item.type === 'dir' && /^\d+$/.test(item.name)) {
      max = Math.max(max, parseInt(item.name, 10));
    }
  }
  return String(max + 1);
}

async function pushFile(filePath, content, message, token) {
  // 기존 파일 SHA 확인 (덮어쓰기용)
  const check = await ghFetch(filePath, token);
  const sha = check.ok ? (await check.json()).sha : undefined;

  const body = {
    message,
    content: Buffer.from(content, 'utf-8').toString('base64'),
    branch: 'main',
  };
  if (sha) body.sha = sha;

  const res = await ghFetch(filePath, token, {
    method: 'PUT',
    body: JSON.stringify(body),
  });
  return res.ok;
}

// ── 핸들러 ─────────────────────────────────────────────────────
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://journal.rococops.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { password, catPath, subDir, title, summary, date, content } = req.body || {};

  // 비밀번호 확인
  if (password !== process.env.ADMIN_PASSWORD) {
    return res.status(401).json({ error: '비밀번호가 올바르지 않습니다.' });
  }

  // 필수 항목
  if (!catPath || !subDir || !title || !content) {
    return res.status(400).json({ error: '필수 항목을 모두 입력해주세요.' });
  }

  const cfg = SUBCATS.find(c => c.catPath === catPath && c.subDir === subDir);
  if (!cfg) return res.status(400).json({ error: '올바르지 않은 카테고리입니다.' });

  const token = process.env.GITHUB_TOKEN;
  if (!token) return res.status(500).json({ error: 'GitHub 토큰이 설정되지 않았습니다.' });

  try {
    const slug = await getNextSlug(catPath, subDir, token);
    const {html: articleHtml, images} = buildArticleBlocks(content, cfg.keywords);
    const description = summary || cleanText(cheerio.load(content).text()).slice(0, 150);
    const ogUrl = `${SITE_BASE}/${catPath}/${subDir}/${slug}/`;
    const ogImage = images[0] || (THUMB_BASE + cfg.thumbPool[0]);
    const heroImage = images[0] || `../../../images/thumbnails/${cfg.thumbPool[0]}`;
    const catName = CAT_NAMES[catPath];
    const pageDate = date || new Date().toISOString().slice(0, 10);

    // 원문 링크 추출
    const $c = cheerio.load(content);
    let originUrl = null;
    $c('*').contents().filter((_, n) => n.type === 'text' && n.data.includes('원문')).each((_, n) => {
      const next = $c(n).next('a');
      if (next.length) { originUrl = next.attr('href') || null; return false; }
    });

    const pageHtml = generatePage({
      title, metaTitle: `${cfg.keywords} — 로코코성형외과 김상호 원장`,
      description, ogImage, ogUrl, date: pageDate,
      catPath, catName, subDir, subName: cfg.subName,
      subNameEn: cfg.subNameEn, heroImage,
      content: articleHtml, originUrl,
    });

    const filePath = `${catPath}/${subDir}/${slug}/index.html`;
    const ok = await pushFile(filePath, pageHtml, `새 글 추가: ${title}`, token);

    if (!ok) return res.status(500).json({ error: 'GitHub push 실패' });

    return res.status(200).json({
      ok: true,
      slug,
      url: ogUrl,
      message: `${filePath} 생성 완료`,
    });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: String(e.message) });
  }
}
