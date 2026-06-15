# 로코코 저널 — 작업 정리 (2026-06-15)

## 1. 완료된 작업 요약

### 사이트 생성 / 콘텐츠
- `sitecontents.sql`(583건) + `mcolumn.sql`(238건) → 시술 상세페이지 + 36개 카테고리 목록페이지 자동 생성 (`tools/build_pages.py`)
- 중복 글 dedup + `<link rel="canonical">` 적용
- About 3페이지(소개/철학/오시는길) 작성 완료, 원장 프로필·인테리어 이미지 적용 완료
- 카드 썸네일: 본문 이미지 없는 글은 카테고리별 썸네일 풀(`thumb_pool`)에서 분배, 있는 글은 `attach1`(전후사진 대표컷) 우선 사용 → 동일 이미지 반복 노출 문제 해결
- `cases/index.html`: 전체 601개 케이스 통합 페이지 (최신순/조회수순 토글)
- 홈페이지 히어로: `data/top-cases.json`(조회수 상위 40개) 기반 랜덤 노출
- footer SNS(블로그/유튜브/인스타) 아이콘 — 전체 페이지 적용 완료 (이번에 index.html도 추가)

### 상담/예약
- `/counsel/index.html` 상담 폼 + `api/consult.js` (Vercel + Resend + Supabase) 구축 완료
- 모든 서브카테고리 nav "상담·예약"은 `counsel/`로 연결됨

### SEO
- `sitemap.xml`, `robots.txt` 추가 완료
- `canonical`, `og:*`, JSON-LD(MedicalWebPage/Physician/LocalBusiness) 적용 완료

### 배포
- GitHub repo `rococops/rococo-journal`, `main` 브랜치 push, GitHub Pages(`main`/root) 활성화

---

## 2. 이번 라운드 변경사항 (2026-06-15)

- 카테고리 랜딩 6페이지(`anti-aging/`, `cheekbone/`, `eye/`, `forehead/`, `nose/`, `nostril/`) 로고 링크 `href="/"` → `href="../"` (GitHub Pages 프로젝트 페이지에서 깨지던 문제 수정)
- `index.html`
  - "최근 케이스 리뷰 → 전체 보기"를 `cases/`로 연결 (예전 `rococops.com/htm/community_photo.php` 외부링크였음)
  - 히어로 섹션 조회수 상위 케이스 랜덤 노출 JS 추가
  - "원장 칼럼" → "김상호원장의 칼럼"으로 변경
  - footer에 누락되어 있던 SNS(블로그/유튜브/인스타) 아이콘 추가 (서브페이지엔 이미 있었으나 루트 index.html만 빠져 있었음)
  - CTA "온라인 상담" 카드 + footer "온라인 상담" 링크: 외부 `rococops.com/htm/counsel_normal.php` → 내부 `counsel/`로 변경
  - nav "상담·예약" 하위에 남아있던 구 홈페이지 외부링크 서브메뉴(온라인상담/카톡상담/수술후상담/FAQ)를 제거 — 서브페이지 nav와 동일하게 단일 링크(`counsel/`)로 정리. (이 서브메뉴는 `/counsel/` 페이지가 생기기 전 임시로 남아있던 코드)

## 3. mcolumn 칼럼 → 서브카테고리 선별 기준

`tools/mcolumn_map.py`의 `classify(category, subject)`가 글 제목(subject)을 기준으로 분류합니다.

1. **1차: 제목 키워드 규칙** (`_rules`) — "비공내리기", "쌍커풀", "무턱", "15분" 등 시술명 키워드가 제목에 있으면 해당 서브카테고리로 매칭 (우선순위 순서대로 검사)
2. **2차: 카테고리 코드 기본값** (`CODE_DEFAULT`) — 제목에서 키워드를 못 찾으면, mcolumn의 4자리 category 코드별로 사전에 정해둔 기본 서브카테고리로 배정 (코드별 실제 글 내용을 확인해서 수동으로 정한 매핑)

즉 "이 칼럼이 왜 이 서브메뉴에 있는가"는 기본적으로 **글 제목에 포함된 시술명 키워드** 기준이고, 제목만으로 판단 안 되는 경우(날짜만 있는 제목 등)에는 원래 mcolumn 카테고리 코드의 주제로 들어갑니다.

---

## 4. 남은 작업 (우선순위 제안)

| 항목 | 내용 |
|---|---|
| 도메인 연결 | `journal.rococops.com` → GitHub Pages CNAME 설정 (사용자가 DNS 작업 필요) |
| 다국어 페이지 | 홈/About/주요 카테고리만 우선 (일/영/중) — 범위·번역 방식 결정 필요 |
| 콘텐츠별 문의 기능 | 시술 상세페이지에 "이 시술 상담 신청" 인라인 폼 — `/counsel/` 백엔드 재사용 가능 |
| 이미지 핫링크 리스크 | 모든 이미지가 `rococops.com` 의존 — 장기적으로 자체 호스팅/CDN 이전 검토 |
