# 로코코 저널 — 작업 정리 (2026-06-15)

## 1. 현재까지 완료된 작업

### 사이트 생성
- `sitecontents.sql`(583건) + `mcolumn.sql`(238건) → 총 857개 시술 상세페이지 + 36개 카테고리 목록페이지 자동 생성 (`tools/build_pages.py`)
- 중복 글 220건에 `<link rel="canonical">` 적용 (사이트 양쪽 테이블 통합 dedup)
- About 섹션 3페이지 신규 작성
  - `about/index.html` — 원장 인사말 (Physician + MedicalBusiness JSON-LD)
  - `about/philosophy/index.html` — 약속 10가지 + 경쟁력 5가지 (MedicalWebPage JSON-LD)
  - `about/location/index.html` — 오시는 길/진료시간 (LocalBusiness + openingHoursSpecification JSON-LD, 카카오맵 딥링크)
- `css/style.css`에 About 페이지용 클래스 추가 (`.about-profile`, `.promise-item`, `.location-grid`, `.map-frame`, `.gallery-grid` 등)

### 배포
- GitHub repo `rococops/rococo-journal` 생성, `main` 브랜치 push 완료 (881개 파일, ~18MB)
- `.gitignore`로 `*.sql`(원본 DB 덤프, 48MB), `.claude/`(로컬 설정) 제외
- GitHub Pages 활성화 (`main` / root) → `https://rococops.github.io/rococo-journal/`

---

## 2. 남은 작업 — 우선순위별 정리

### 🔴 P0 — 당장 막혀있는 것
| 항목 | 내용 | 상태 |
|---|---|---|
| 원장 프로필 사진 | about/index.html에 placeholder 이미지 경로(`/images/intro/doctor/1.jpg`)가 깨짐. 실제 경로 확인 또는 사진 직접 전달 필요 | 보류 — 사진 받으면 리사이즈/톤보정해서 적용 (Pillow 사용) |
| 토큰 보안 | 채팅에 노출된 GitHub PAT(`ghp_TeWuc...`)는 **즉시 Revoke 후 재발급** 권장 | 미완료 |

### 🟡 P1 — 다음 작업 단위 (이번 라운드 우선 진행 권장)

#### (6) 상담·예약 / 전후사진 — 기존 홈페이지 외부링크 문제
- 현재 헤더 nav의 "상담·예약" 상위 메뉴는 `{root}counsel/`로 연결되지만 실제 `/counsel/` 폴더가 없음 → **404**
- 서브메뉴(온라인상담/카톡상담/수술후상담/FAQ) 및 "전후사진" 버튼은 모두 `rococops.com` 구 홈페이지로 `target="_blank")` 외부 이동
- → **(5) 온라인 상담 폼**을 `/counsel/index.html`에 만들면 상위메뉴 404가 자연스럽게 해결됨
- 전후사진은 회원 로그인 기반 시스템이라 저널 사이트에 직접 이전하기보다 일단 외부 링크 유지가 합리적 (재구축 비용 大)

#### (5) 온라인 상담 폼
- 구조: `/counsel/index.html`(바닐라 JS 폼) → Vercel API(`/api/consult`) → 이메일 발송
  - 알림 채널은 **이메일로 시작** (카카오 알림톡은 대행사 가입/템플릿 심사 필요해 보류, 추후 전환 가능한 구조로)
- 필요 정보: 알림 받을 이메일 주소, 이메일 발송 서비스(Resend 등) 선택
- (선택) Supabase에 상담 내역 저장 → 추후 관리자 페이지에서 조회

#### (7) 카드 썸네일 중복 문제
- 원인: `tools/build_pages.py`의 `DEFAULT_IMG = 'https://rococops.com/images/main/mcs/2.jpg'` — 본문에 이미지가 없는 글은 전부 이 한 장으로 통일되어, 카테고리 목록 페이지에서 같은 썸네일이 반복 노출됨
- **(4)와 연결되는 해결책**: 이미지가 없는 글들의 제목/요약을 기반으로 GPT(이미지 생성)에 프롬프트를 던져 카테고리별 대표 이미지를 다양하게 생성 → `images/generated/` 같은 폴더에 저장 후 `DEFAULT_IMG`를 글마다 다른 이미지로 매핑
- 작업 순서 제안:
  1. 이미지 없는 글 목록 추출 (카테고리/제목별로 그룹화)
  2. 카테고리별 또는 글 그룹별로 이미지 생성 프롬프트 작성 (예: "광대축소술 전후 일러스트, 미니멀 라인아트, 골드+블랙 톤")
  3. 생성된 이미지를 리사이즈/최적화 후 적용
  4. `build_pages.py`의 `DEFAULT_IMG` 로직을 "카테고리별 이미지 풀에서 글 num 기준 분배"로 수정

---

## 3. 검색 노출 / AI 검색 최적화 (3)

### 즉시 적용 가능 (코드 작업)
- [ ] `sitemap.xml` 자동 생성 — `build_pages.py`에서 867개 URL 추출해서 생성
- [ ] `robots.txt` 추가 (sitemap 경로 명시)
- [ ] FAQ 스키마(JSON-LD) — 시술 상세페이지에 자주 묻는 질문 추가 시 AI 검색(Perplexity/ChatGPT/Google AI Overview) 인용 가능성 ↑

### 이미 적용된 것 (확인용)
- ✅ `canonical`, `og:*`, JSON-LD(MedicalWebPage/Physician/LocalBusiness) 적용 완료

### 등록 작업 (배포 후 1회, 사용자 직접)
- [ ] Google Search Console 등록 + sitemap 제출
- [ ] 네이버 서치어드바이저 등록 (한국 검색 비중 고려 시 필수)
- [ ] Bing Webmaster Tools 등록 (ChatGPT 검색 인덱스 기반)

---

## 4. 도메인 연결

- `journal.rococops.com` → GitHub Pages 연결 필요
  1. `rococops.com` DNS 관리 화면에서 `journal` 서브도메인에 **CNAME → rococops.github.io** 추가
  2. GitHub repo Settings → Pages → Custom domain에 `journal.rococops.com` 입력 → Save
  3. "Enforce HTTPS" 체크 (DNS 전파 후 자동 인증서 발급)
- DNS 설정은 사용자가 직접 (도메인 관리 계정 접근 필요)

---

## 5. 글로벌(다국어) 홈페이지 (1)

- 867페이지 전체 번역은 비효율적 — **핵심 페이지만 우선 다국어화** 권장
  - 대상: 홈, About 3페이지, 대표 시술 카테고리 목록(광대/코/콧구멍/눈 등)
  - 언어: 일본어, 영어, 중국어(간체) — 강남 성형외과 표준 3종
- 구조 제안: `/en/`, `/ja/`, `/zh/` 폴더 + `<link rel="alternate" hreflang="...">` 상호 연결
- **결정 필요**: 번역 품질(기계번역 vs 전문번역), 대상 페이지 범위, 우선순위(트래픽 분석 후 결정 추천)

---

## 6. 컨텐츠별 댓글/문의 기능 (2) — 논의 필요

- 각 시술 상세페이지 하단에 "이 시술에 대해 질문하기" 같은 인라인 폼 → (5)의 상담 폼과 동일한 백엔드 재사용 가능
- 고려사항:
  - 단순 "문의 폼"(현재 사이드바 인라인 CTA 확장) vs 진짜 "댓글(공개 게시판)" — 후자는 스팸/검수 부담 큼
  - **추천**: 댓글보다는 "이 글에 대해 상담 신청" 형태의 1:1 문의 폼이 의료광고법/스팸 관리 측면에서 안전
- 결정 필요: 댓글형 vs 문의형

---

## 7. 추가로 고려해볼 것 (제안)

- **이미지 핫링킹 리스크**: 모든 이미지가 `rococops.com` 원본 서버에 의존 — 그 사이트가 개편/다운되면 저널 사이트 전체 이미지가 깨짐. 장기적으로 Supabase Storage나 GitHub Pages 자체 호스팅으로 이전 검토
- **이미지 용량/속도**: 외부 이미지 lazy-load는 적용되어 있으나(`loading="lazy"`), 원본 이미지 크기가 클 경우 모바일 속도 저하 가능 — 추후 이미지 최적화(WebP 변환 등) 검토
- **개인정보/의료광고법 검토**: 상담 폼 도입 시 개인정보 수집 동의 문구, 의료광고 심의 대상 여부(특히 "수면마취 무사고" 같은 통계 문구) 확인 권장
- **PetReview와의 작업 분리**: 이번에 `rococops` GitHub organization으로 분리한 것처럼, Vercel/Supabase 프로젝트도 별도 계정/프로젝트로 분리 권장 (이미 합의됨)

---

## 8. 다음 라운드 작업 순서 제안

1. 도메인 연결 (`journal.rococops.com`) — 가장 빠르게 끝남, 실제 운영 URL 확보
2. `/counsel/` 상담 폼 + Vercel 프록시 (이메일 알림) — 헤더 404 해결 + 핵심 기능
3. `sitemap.xml` / `robots.txt` 생성 + 검색엔진 등록
4. 원장 프로필 사진 적용 (사진 받는 대로)
5. 카드 썸네일 중복 문제 — 이미지 생성 프롬프트 작업
6. 다국어 페이지 범위 확정 → 작업 착수
7. 컨텐츠별 문의 폼 — (2)번과 (5)번 통합 설계
