// 전체 사이트 GNB 일괄 교체: 옛 "온라인상담/예약신청" 분리 메뉴 → navHtml()의 "상담·예약" 통합 메뉴 + "수술후기" 신규 항목.
// 각 파일의 기존 nav 블록에서 root(상대경로 prefix)를 직접 추출해 재사용하므로 depth 계산 실수 위험이 없음.
// 활성 카테고리는 파일 경로(최상위 디렉터리)로 판정.
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { navHtml, CAT_NAMES } from './nav.mjs';

const ROOT = process.cwd();
const SKIP_DIRS = new Set(['.git', 'node_modules', '.claude']);
const NAV_RE = /<nav class="gnb" id="gnb">[\s\S]*?<\/nav>/;
const ROOT_EXTRACT_RE = /<a href="([./]*)cheekbone\/">광대성형<\/a>/;

function walk(dir, out) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) walk(p, out);
    else if (name.endsWith('.html')) out.push(p);
  }
}

const files = [];
walk(ROOT, files);
console.log(`검사 대상 HTML 파일: ${files.length}개`);

let changed = 0, noNav = 0, unchanged = 0;
const catKeys = Object.keys(CAT_NAMES);

for (const filePath of files) {
  const html = readFileSync(filePath, 'utf8');
  if (!NAV_RE.test(html)) { noNav++; continue; }

  const rootMatch = html.match(ROOT_EXTRACT_RE);
  if (!rootMatch) {
    console.warn(`  ⚠ root 추출 실패, 건너뜀: ${relative(ROOT, filePath)}`);
    continue;
  }
  const root = rootMatch[1];

  const relSegments = relative(ROOT, filePath).split(sep);
  const activeCat = catKeys.includes(relSegments[0]) ? relSegments[0] : null;

  const newNav = navHtml(root, activeCat);
  const newHtml = html.replace(NAV_RE, newNav);

  if (newHtml === html) { unchanged++; continue; }
  writeFileSync(filePath, newHtml, 'utf8');
  changed++;
}

console.log(`완료 — 교체: ${changed}, 이미 최신: ${unchanged}, nav 없음: ${noNav}`);
