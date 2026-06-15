# 로코코 저널 (rococo-journal) 프로젝트 지침

## 프로젝트 개요
- 로코코성형외과 시술 후기/칼럼 정적 사이트 (sitecontents.sql, mcolumn.sql 기반 자동 생성)
- 순수 정적 HTML/CSS/JS — 빌드 툴 없음
- GitHub repo: https://github.com/rococops/rococo-journal.git (branch: main)
- 호스팅: GitHub Pages (main / root) → 추후 journal.rococops.com 커스텀 도메인 연결 예정

## 파일 구조
```
/
├── index.html
├── css/style.css
├── assets/ (이미지 등)
├── about/                ← 원장 인사말, 철학, 오시는 길
├── nostril/, nose/, cheekbone/, eye/, forehead/, anti-aging/ 등 ← 시술 카테고리별 목록+상세 페이지
├── tools/build_pages.py  ← sql → html 자동 생성 스크립트
├── PROJECT_NOTES.md       ← 작업 현황/로드맵 정리
└── CLAUDE.md
```

## 코딩 규칙
- 바닐라 JS/HTML/CSS 기본, 프레임워크/빌드툴 도입 전 먼저 확인 요청
- CSS는 css/style.css에 기존 클래스 네이밍 패턴(.card, .article-content, .section-head 등) 따라 추가
- 함수/변수명은 영어, 주석은 한국어
- 코드 수정 시 기존 로직 함부로 삭제하지 말 것 — 변경 전 반드시 설명 먼저
- 이미지는 현재 rococops.com 원본 서버에 의존(핫링크) — 경로 추측 금지, 모르면 사용자에게 확인

## 작업 방식
- 큰 변경 전에는 무엇을 왜 바꾸는지 먼저 설명하고 진행
- 파일 여러 개 동시에 수정할 때는 어떤 파일을 건드리는지 목록 먼저 제시
- 모르는 부분 있으면 추측으로 진행하지 말고 질문할 것
- 작업 완료 후 테스트 방법도 함께 안내

## 협업 원칙
- 모든 작업은 main 브랜치까지 push 완료할 것 (커밋만 하고 끝내지 말 것)
- 빈느님 의견에 무조건 동의하거나 칭찬하지 말 것 — 장점과 단점을 냉정하게 분석하고 이유와 함께 설명할 것
- 더 나은 아이디어가 있으면 항상 먼저 제시할 것

## 보안 / 주의사항
- *.sql (sitecontents.sql, mcolumn.sql 원본 DB 덤프)은 .gitignore로 제외 — 절대 커밋하지 말 것
- GitHub PAT 등 민감한 토큰을 코드/커밋/파일에 절대 남기지 말 것
- 상담 폼 등 백엔드 연동 시 API 키는 Vercel 환경변수로 관리, 프론트에 하드코딩 금지
- GitHub Pages는 서버사이드 코드 실행 불가 — 백엔드 로직은 반드시 별도 프록시(Vercel 등)로
