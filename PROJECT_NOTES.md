# 로코코 저널 — 작업 현황 (2026-06-17)

## 완료

### 콘텐츠 / 페이지 생성
- `sitecontents.sql`(583건) + `mcolumn.sql`(238건) → 869개 상세페이지 + 36개 카테고리 목록 자동 생성 (`tools/build_pages.py`)
- `cases/index.html` — 601개 케이스 통합 페이지
- About 3페이지 (소개 / 철학 / 오시는길)
- 중복 글 dedup + canonical 적용
- 본문 이미지 http → https 전환 (Mixed Content 전면 해결)
- 네이버 블로그 관련글 박스 → 인라인 링크로 변환
- 카드 썸네일: attach1 우선, 없으면 카테고리별 풀 분배

### 홈페이지
- 히어로: 좌측 이미지 + 우측 텍스트 동일 글로 통일
- 고정 카드: cheekbone/quick/580, nose/rib-cartilage/602, nostril/alar-lowering/627, nose/column/621

### 상담
- `/counsel/` 상담 폼 + `api/consult.js` (Vercel + Resend + Supabase)
- 카카오채널 플로팅 버튼 (https://pf.kakao.com/_xdBpRl)

### 다국어 (`/en/`, `/ja/`, `/zh/`)
- 3개 언어 랜딩 페이지 생성 (의사 소개, 시술, 위치, 상담, FAQ, 구글맵)
- 시술별 조회수 상위 + 최신글 각 10개 카드 (6개 카테고리 × 10개)
- 헤더 GLOBAL ▾ 언어 스위처 (전 페이지 공통)
- 브라우저 언어 감지 자동 리다이렉트 (zh/ja/기타 → 해당 언어 페이지)
- 전 글 상단 번역 안내 배너 (브라우저 자동번역 안내)
- 언어 지원: 영어(원장 직접) / 중국어(전담 스태프) / 일본어(통역 동반 환영)

### 어드민 (`/admin/`)
- GitHub API 연동 글 등록/삭제
- localStorage 세션 유지
- 글 목록: 고유 제목 파싱, 순서 정렬 (순수 숫자 슬러그 우선)

### SEO / 기술
- sitemap.xml (869개), robots.txt, llms.txt
- canonical, og:*, JSON-LD (MedicalWebPage / BreadcrumbList / MedicalBusiness 등)
- Google Search Console ✅ / 네이버 서치어드바이저 ✅ / Bing Webmaster ✅
- GitHub Pages + 커스텀 도메인 `journal.rococops.com` + HTTPS

---

## 남은 작업

| 항목 | 우선순위 | 내용 |
|---|---|---|
| **RealSelf 등록** | ★★★ | 성형외과 특화, 영어권 환자 유입 |
| **WhatClinic 등록** | ★★★ | 글로벌 클리닉 디렉토리 |
| **Expat Health Seoul 등록** | ★★☆ | 서울 거주 외국인 대상 |
| **Bookimed 등록** | ★★☆ | 의료관광 전문 |
| **Visit Medical Korea 등록** | ★★☆ | 한국 의료관광 공식 플랫폼 |
| **어드민 글 수정 기능** | ★★☆ | 현재 등록/삭제만 가능, git pull 충돌 이슈 |
| **이미지 자체 호스팅** | ★☆☆ | rococops.com 핫링크 의존 — 원본 서버 셧다운 시 전체 이미지 깨짐 |

---

## 기술 스택

- 정적 HTML/CSS/JS (빌드툴 없음)
- 페이지 생성: Python + BeautifulSoup4
- 상담 백엔드: Vercel Functions + Resend + Supabase
- 호스팅: GitHub Pages → `journal.rococops.com`
- 이미지: `rococops.com` 핫링크 (자체 호스팅 미완)
