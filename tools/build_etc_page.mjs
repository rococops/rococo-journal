// etc/general/index.html — 자동 분류 실패한 후기들을 위한 최소 플레이스홀더 케이스 페이지.
// 실제 시술 케이스 글이 없는 가상 카테고리라 전용 목록 페이지는 없고, 후기 사이드바/브레드크럼의
// "케이스 글 보기" 링크가 404 안 나게만 해주는 용도.
import { writeFileSync, mkdirSync } from 'node:fs';
import { navHtml } from './nav.mjs';
import { FOOTER } from './review_utils.mjs';

const root = '../../';
const nav = navHtml(root, 'etc');

const html = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>기타 — 로코코성형외과 김상호 원장</title>
<meta name="description" content="자동으로 시술 카테고리를 특정하지 못한 환자 후기 모음.">
<link rel="canonical" href="https://journal.rococops.com/etc/general/">
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
      <span>기타</span>
    </div>
    <div class="article-hero-inner" style="grid-template-columns: 1fr;">
      <div class="article-hero-text">
        <h1 class="article-title">기타</h1>
        <p class="article-summary">특정 시술로 자동 분류되지 않은 환자 후기 모음입니다.</p>
      </div>
    </div>
  </div>
</section>
${FOOTER(root)}
</body>
</html>
`;

mkdirSync('etc/general', { recursive: true });
writeFileSync('etc/general/index.html', html, 'utf8');
console.log('생성 완료: etc/general/index.html');
