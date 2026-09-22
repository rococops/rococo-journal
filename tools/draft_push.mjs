// 로컬에서 작성한 성형 가이드 초안(JSON)을 관리자 "초안함"으로 보냄.
//   node tools/draft_push.mjs drafts_local/구축코-원인.json
//
// 인증: 초안 "생성"만 가능한 별도 토큰(DRAFT_API_TOKEN). 관리자 비밀번호와 달리
// 발행·조회·삭제는 못 하므로, 이 토큰이 유출돼도 피해는 초안함에 글이 쌓이는 정도.
// 토큰은 환경변수 DRAFT_API_TOKEN 또는 저장소 루트의 .draft_token 파일(gitignore)에서 읽음.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const API = 'https://rococo-journal-api.vercel.app/api/publish?action=draft-create';

const file = process.argv[2];
if (!file) { console.error('사용법: node tools/draft_push.mjs <초안.json>'); process.exit(1); }

const tokenFile = join(ROOT, '.draft_token');
const token = process.env.DRAFT_API_TOKEN || (existsSync(tokenFile) ? readFileSync(tokenFile, 'utf8').trim() : '');
if (!token) { console.error('DRAFT_API_TOKEN 이 없습니다 (.draft_token 파일 또는 환경변수).'); process.exit(1); }

const draft = JSON.parse(readFileSync(file, 'utf8'));
const res = await fetch(API, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'X-Draft-Token': token },
  body: JSON.stringify(draft),
});
const data = await res.json().catch(() => ({}));
if (!res.ok) { console.error(`실패 (${res.status}):`, data.error || data); process.exit(1); }
console.log(`초안함에 등록됨: ${draft.title}\n  id: ${data.id}`);
