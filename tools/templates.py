"""상세/목록 페이지 HTML 템플릿. {root}는 사이트 루트까지의 상대경로(예: '../../' 또는 '../../../')."""

NAV_HTML = """<nav class="gnb" id="gnb">
      <ul>
        <li class="has-sub {active_cheekbone}"><a href="{root}cheekbone/">광대성형</a>
          <ul class="sub-menu">
            <li><a href="{root}cheekbone/quick/">15분 광대축소술</a></li>
            <li><a href="{root}cheekbone/fat-graft/">심부볼·관자 지방이식</a></li>
            <li><a href="{root}cheekbone/liposuction/">광대라인 지방흡입</a></li>
            <li><a href="{root}cheekbone/rear/">뒷광대축소술</a></li>
            <li><a href="{root}cheekbone/revision/">광대 재수술</a></li>
          </ul>
        </li>
        <li class="has-sub {active_nose}"><a href="{root}nose/">코성형</a>
          <ul class="sub-menu">
            <li><a href="{root}nose/column/">진료단상</a></li>
            <li><a href="{root}nose/revision/">코재수술</a></li>
            <li><a href="{root}nose/rib-cartilage/">늑연골 명품코성형</a></li>
            <li><a href="{root}nose/septal/">비중격연골 코성형</a></li>
            <li><a href="{root}nose/scarless/">흉터없는 코성형</a></li>
            <li><a href="{root}nose/hump/">매부리코</a></li>
            <li><a href="{root}nose/bulbous/">복코</a></li>
            <li><a href="{root}nose/osteotomy/">절골술</a></li>
            <li><a href="{root}nose/long/">긴코</a></li>
            <li><a href="{root}nose/columella/">비주성형</a></li>
            <li><a href="{root}nose/cat/">비순각 고양이 입매교정</a></li>
            <li><a href="{root}nose/male/">남자의 코성형</a></li>
            <li><a href="{root}nose/rhinitis/">비염수술</a></li>
          </ul>
        </li>
        <li class="has-sub {active_nostril}"><a href="{root}nostril/">콧구멍성형</a>
          <ul class="sub-menu">
            <li><a href="{root}nostril/alar-lowering/">비공내리기</a></li>
            <li><a href="{root}nostril/alar-raising/">콧날개올리기</a></li>
            <li><a href="{root}nostril/v-shape/">V형 콧구멍교정</a></li>
            <li><a href="{root}nostril/reduction/">콧구멍축소술</a></li>
            <li><a href="{root}nostril/alar-base/">콧볼축소술</a></li>
          </ul>
        </li>
        <li class="has-sub {active_forehead}"><a href="{root}forehead/">이마성형</a>
          <ul class="sub-menu">
            <li><a href="{root}forehead/endoscopic/">내시경 이마거상술</a></li>
            <li><a href="{root}forehead/reduction/">이마축소술</a></li>
          </ul>
        </li>
        <li class="has-sub {active_eye}"><a href="{root}eye/">눈성형</a>
          <ul class="sub-menu">
            <li><a href="{root}eye/correction/">눈매교정술</a></li>
            <li><a href="{root}eye/incision/">트임성형</a></li>
            <li><a href="{root}eye/double/">쌍커풀 자연유착법</a></li>
            <li><a href="{root}eye/lower-fat/">눈밑지방 재배치</a></li>
            <li><a href="{root}eye/fat-graft/">꺼진눈 지방이식</a></li>
            <li><a href="{root}eye/brow-lift/">눈썹하거상술</a></li>
          </ul>
        </li>
        <li class="has-sub {active_anti_aging}"><a href="{root}anti-aging/">동안성형</a>
          <ul class="sub-menu">
            <li><a href="{root}anti-aging/chin/">무턱성형</a></li>
            <li><a href="{root}anti-aging/fat-graft/">미세지방이식</a></li>
            <li><a href="{root}anti-aging/blepharoplasty/">상·하안검성형</a></li>
            <li><a href="{root}anti-aging/lifting/">엘라스티꿈 실리프팅</a></li>
            <li><a href="{root}anti-aging/filler-botox/">필러·보톡스</a></li>
          </ul>
        </li>
        <li class="has-sub"><a href="{root}about/">About</a>
          <ul class="sub-menu">
            <li><a href="{root}about/">로코코 소개</a></li>
            <li><a href="{root}about/philosophy/">철학과 강점</a></li>
            <li><a href="{root}about/location/">오시는 길·진료시간</a></li>
          </ul>
        </li>
        <li><a href="{root}counsel/">상담·예약</a></li>
        <li><a href="https://rococops.com/htm/community_photo.php" class="btn-consult" target="_blank">전후사진</a></li>
      </ul>
    </nav>"""

HEADER_HTML = """<header class="site-header" id="header">
  <div class="header-inner">
    <a href="{root}" class="logo">
      <span class="logo-main">ROCOCO</span>
      <span class="logo-sub">Journal</span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기">
      <span></span><span></span><span></span>
    </button>
    {nav}
  </div>
</header>"""

FOOTER_HTML = """<footer class="site-footer">
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
        <div class="footer-social">
          <a href="https://blog.naver.com/rococo2015" target="_blank" rel="noopener" aria-label="블로그">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"></path></svg>
          </a>
          <a href="https://www.youtube.com/channel/UCTljLxXSlZjMo--f9FmDx5g" target="_blank" rel="noopener" aria-label="유튜브">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
          </a>
          <a href="https://www.instagram.com/rococo_clinic/" target="_blank" rel="noopener" aria-label="인스타그램">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.5" y2="6.5"></line></svg>
          </a>
        </div>
        <a href="https://rococops.com" target="_blank">기존 홈페이지</a>
        <a href="{root}counsel/">온라인 상담</a>
        <a href="https://rococops.com/htm/community_photo.php" target="_blank">전후사진</a>
        <a href="{root}about/">About 로코코</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 Rococo Plastic Surgery. All rights reserved.</p>
      <a href="https://rococops.com/htm/intro_notice.php?cate=private" target="_blank">개인정보취급방침</a>
    </div>
  </div>
</footer>
<script src="{root}js/main.js"></script>
</body>
</html>"""

CTA_SECTION_HTML = """<!-- 하단 CTA -->
<section class="cta-section">
  <div class="container">
    <div class="cta-grid">
      <a href="https://rococops.com/htm/community_photo.php" class="cta-card" target="_blank">
        <div class="cta-card-inner">
          <span class="cta-label">{cat_name} 전후사진</span>
          <h3 class="cta-title">실제 수술 결과를<br>직접 확인하세요</h3>
          <p class="cta-desc">회원 로그인 후 전체 케이스를 열람할 수 있습니다</p>
          <span class="cta-btn">전후사진 보기 →</span>
        </div>
      </a>
      <a href="{root}counsel/?from={cat_name}" class="cta-card">
        <div class="cta-card-inner">
          <span class="cta-label">온라인 상담</span>
          <h3 class="cta-title">궁금한 점을<br>직접 물어보세요</h3>
          <p class="cta-desc">김상호 원장이 직접 답변해 드립니다</p>
          <span class="cta-btn">상담 신청하기 →</span>
        </div>
      </a>
    </div>
  </div>
</section>"""


DETAIL_PAGE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta_title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{meta_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="article">
<link rel="canonical" href="{canonical_url}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "headline": "{title_json}",
  "description": "{description_json}",
  "url": "{og_url}",
  "author": {{
    "@type": "Physician",
    "name": "김상호",
    "worksFor": {{"@type": "MedicalBusiness", "name": "로코코성형외과"}}
  }},
  "publisher": {{
    "@type": "MedicalBusiness",
    "name": "로코코성형외과",
    "url": "https://journal.rococops.com"
  }},
  "medicalAudience": "Patient",
  "specialty": "Plastic Surgery"
}}
</script>
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="{root}css/style.css">
</head>
<body>

{header}

<!-- 아티클 히어로 -->
<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb">
      <a href="{root}">홈</a>
      <span>›</span>
      <a href="{root}{cat_path}/">{cat_name}</a>
      <span>›</span>
      <a href="{list_root}">{sub_name}</a>
      <span>›</span>
      <span>{title_short}</span>
    </div>
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <span class="eyebrow">{sub_name_en}</span>
        <h1 class="article-title">{title}</h1>
        <p class="article-summary">{description}</p>
        <div class="article-meta">
          <span class="meta-author">김상호 원장</span>
          <span class="dot">·</span>
          <span class="meta-cat">{sub_name}</span>
          <span class="dot">·</span>
          <span class="meta-clinic">로코코성형외과</span>
        </div>
      </div>
      <div class="article-hero-img">
        <img src="{hero_image}" alt="{img_alt}" loading="eager">
      </div>
    </div>
  </div>
</section>

<!-- 아티클 본문 -->
<article class="article-body">
  <div class="container">
    <div class="article-layout">
      <div class="article-content">
        {content}

        <!-- 상담 인라인 CTA -->
        <div class="inline-cta">
          <p class="inline-cta-text">{sub_name}에 대해 더 궁금한 점이 있으신가요?</p>
          <a href="{root}counsel/?from={sub_name}" class="inline-cta-btn">김상호 원장에게 직접 상담하기 →</a>
        </div>
      </div>

      <!-- 사이드바 -->
      <aside class="article-sidebar">
        <div class="sidebar-card">
          <p class="sidebar-title">전후사진 보기</p>
          <p class="sidebar-desc">로코코에서 수술하신 분들의 실제 케이스를 확인하세요</p>
          <a href="https://rococops.com/htm/community_photo.php" class="sidebar-btn" target="_blank">전후사진 열람 →</a>
        </div>
        <div class="sidebar-card">
          <p class="sidebar-title">온라인 상담</p>
          <p class="sidebar-desc">02-2135-2702<br>월·금 09:00~19:00<br>화·수·목 09:00~18:00<br>토 09:00~13:00</p>
          <a href="{root}counsel/?from={sub_name}" class="sidebar-btn">상담 신청하기 →</a>
        </div>
        <div class="sidebar-related">
          <p class="sidebar-title">{sub_name} 다른 글</p>
          <a href="{list_root}" class="related-link">{sub_name} 목록 보기 →</a>
        </div>
      </aside>
    </div>
  </div>
</article>

{cta_section}

{footer}
"""


LIST_PAGE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{sub_name} | 로코코 저널</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{sub_name} | 로코코 저널">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="website">
<link rel="canonical" href="{og_url}">
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="{root}css/style.css">
</head>
<body>

{header}

<!-- 아티클 히어로 -->
<section class="article-hero">
  <div class="container">
    <div class="article-breadcrumb">
      <a href="{root}">홈</a>
      <span>›</span>
      <a href="{root}{cat_path}/">{cat_name}</a>
      <span>›</span>
      <span>{sub_name}</span>
    </div>
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <span class="eyebrow">{sub_name_en}</span>
        <h1 class="article-title">{sub_name}</h1>
        <p class="article-summary">{description}</p>
        <div class="article-meta">
          <span class="meta-author">김상호 원장</span>
          <span class="dot">·</span>
          <span class="meta-cat">{cat_name}</span>
          <span class="dot">·</span>
          <span class="meta-clinic">로코코성형외과</span>
        </div>
      </div>
      <div class="article-hero-img">
        <img src="{hero_src}" alt="{sub_name}" loading="eager">
      </div>
    </div>
  </div>
</section>

<!-- 글 목록 -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <h2 class="section-label">{sub_name} 케이스 ({count}개)</h2>
    </div>
    <div class="card-grid">
{cards}
    </div>
  </div>
</section>

{cta_section}

{footer}
"""


CARD_HTML = """      <a href="{num}/" class="card">
        <div class="card-img">
          <img src="{img}" alt="{title}" loading="lazy">
          <span class="card-tag">{sub_name}</span>
        </div>
        <div class="card-body">
          <p class="card-title">{title}</p>
          <p class="card-desc">{desc}</p>
        </div>
      </a>"""
