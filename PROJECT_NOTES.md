# 로코코 저널 — 작업 정리 (2026-06-16)

## 1. 완료된 작업 요약

### 사이트 생성 / 콘텐츠
- `sitecontents.sql`(583건) + `mcolumn.sql`(238건) → 시술 상세페이지 + 36개 카테고리 목록페이지 자동 생성 (`tools/build_pages.py`)
- 총 869개 개별 페이지 + `cases/index.html`(601개 케이스 통합)
- 중복 글 dedup + `<link rel="canonical">` 적용
- About 3페이지(소개/철학/오시는길) 작성 완료
- 카드 썸네일: attach1(전후사진 대표컷) 우선, 없으면 카테고리별 썸네일 풀 분배
- 네이버 블로그 관련글 박스(se2_quote blockquote) → `.related-post-link` 인라인 링크로 변환
- 본문 이미지 `http://` → `https://` 강제 변환 (Mixed Content 전면 해결, 809개)

### 홈페이지 히어로
- 왼쪽 이미지 + 오른쪽 텍스트 = 동일 글로 통일 (이전엔 서로 다른 글이라 혼란)
- 각 카테고리 최신글 고정:
  - 히어로: `cheekbone/quick/580/` — 변형 15분 광대축소술 흉터에 대해
  - 서브1: `nose/rib-cartilage/602/` — 자가늑연골 뾰족코 수술
  - 서브2: `nostril/alar-lowering/627/` — 코끝 연골비침·휜코 교정 비공내리기
  - 카드1: `nose/column/621/` — 비주말린 코 비개방 코성형

### 상담/예약
- `/counsel/index.html` 상담 폼 + `api/consult.js` (Vercel + Resend + Supabase) 구축 완료

### 모바일 메뉴
- 우측 슬라이드 패널 (화면의 82%, max 340px)
- 서브메뉴 클릭 accordion (max-height 애니메이션)
- 오버레이 클릭으로 닫기
- PC에서 "Menu X" 숨김 처리

### SEO / GEO
- `sitemap.xml` (869개 URL, 글별 lastmod 반영)
- `robots.txt` (AI 크롤러 명시적 허용: GPTBot, ClaudeBot, PerplexityBot 등)
- `llms.txt` (AI 검색 최적화 가이드)
- `canonical`, `og:*`, JSON-LD(MedicalWebPage / BreadcrumbList / Physician / MedicalBusiness / WebSite) 전체 적용
- `404.html` 커스텀 에러 페이지

### 검색엔진 등록
- Google Search Console: 소유확인 ✅, 사이트맵 제출 ✅ (869페이지 발견)
- 네이버 서치어드바이저: 소유확인 ✅, 사이트맵 제출 ✅
- Bing Webmaster Tools: 소유확인 ✅, 사이트맵 제출 ✅ (Processing)

### 도메인 / 배포
- GitHub Pages (`main` / root) 호스팅
- 커스텀 도메인 `journal.rococops.com` 연결 완료 (Cafe24 CNAME → GitHub Pages)
- HTTPS Enforce 활성화

---

## 2. 남은 작업 (우선순위 제안)

| 항목 | 우선순위 | 내용 |
|---|---|---|
| 카카오 채널 상담 연동 | ★★★ | 카카오 채널 버튼을 플로팅 또는 CTA에 추가 — 별도 백엔드 불필요, 채널 URL만 있으면 됨 |
| 홈 히어로 업데이트 주기 | ★★☆ | 새 글 올라올 때마다 수동으로 index.html 수정 필요 — 자동화 고려 |
| 이미지 자체 호스팅 | ★★☆ | 현재 rococops.com 핫링크 의존 — 기존 홈페이지 셧다운 시 전체 이미지 깨짐 |
| 다국어 페이지 | ★☆☆ | 홈/About/주요 카테고리 일/영/중 — 범위·번역 방식 결정 필요 |
| 검색창 추가 | ★☆☆ | 키워드로 869개 글 검색 — 정적 사이트라 별도 인덱스 필요 (Fuse.js 또는 Pagefind) |

---

## 3. mcolumn 칼럼 서브카테고리 분류 기준

`tools/mcolumn_map.py`의 `classify(category, subject)`
1. **1차: 제목 키워드 규칙** — 시술명 키워드로 서브카테고리 매칭
2. **2차: 카테고리 코드 기본값** — 키워드 미매칭 시 mcolumn 코드별 기본 서브카테고리

---

## 4. 기술 스택

- 순수 정적 HTML/CSS/JS (빌드툴 없음)
- 페이지 생성: Python + BeautifulSoup4 (`tools/build_pages.py`)
- 상담 폼 백엔드: Vercel Functions + Resend(메일) + Supabase(DB)
- 호스팅: GitHub Pages → `journal.rococops.com`
- 이미지: `rococops.com` 핫링크 (자체 호스팅 이전 미완)
