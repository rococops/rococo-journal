// {cat}/{subdir}/reviews/ 가 있는 모든 서브카테고리의 케이스 목록 페이지(index.html)에
// hero와 글 목록 사이에 "수술후기 보러가기" 배너를 삽입. 기존 카드그리드는 절대 건드리지 않음.
// 이미 배너가 있으면(cheekbone/quick 등) 건너뜀 — 재실행해도 안전(idempotent).
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { CAT_NAMES } from './nav.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const MARKER = '<!-- 수술후기 진입 배너 -->';
const INSERT_BEFORE = '<!-- 글 목록 -->';

function banner(subName) {
  return `${MARKER}
<section class="section" style="padding-top:0;">
  <div class="container">
    <a href="reviews/" class="cta-card" style="display:block;">
      <div class="cta-card-inner">
        <span class="cta-label">PATIENT REVIEWS · 환자 후기</span>
        <h3 class="cta-title">${subName}을 받은 환자분들의<br>진짜 수술후기</h3>
        <p class="cta-desc">직접 남기신 생생한 후기를 확인해보세요</p>
        <span class="cta-btn">수술후기 보러가기 →</span>
      </div>
    </a>
  </div>
</section>

`;
}

let inserted = 0, skipped = 0, noMarker = 0;

for (const catPath of Object.keys(CAT_NAMES)) {
  const catDir = join(ROOT, catPath);
  if (!existsSync(catDir)) continue;
  for (const subDir of readdirSync(catDir)) {
    const reviewsIdx = join(catDir, subDir, 'reviews', 'index.html');
    const pageIdx = join(catDir, subDir, 'index.html');
    if (!existsSync(reviewsIdx) || !existsSync(pageIdx)) continue;

    let html = readFileSync(pageIdx, 'utf8');
    if (html.includes(MARKER)) { skipped++; continue; }
    if (!html.includes(INSERT_BEFORE)) {
      console.warn(`  ⚠ 삽입 기준점 없음, 건너뜀: ${catPath}/${subDir}/index.html`);
      noMarker++;
      continue;
    }
    const m = html.match(/<h1 class="article-title">([\s\S]*?)<\/h1>/);
    const subName = m ? m[1].trim() : subDir;

    html = html.replace(INSERT_BEFORE, banner(subName) + INSERT_BEFORE);
    writeFileSync(pageIdx, html, 'utf8');
    console.log(`  + ${catPath}/${subDir}/index.html`);
    inserted++;
  }
}

console.log(`\n완료 — 삽입 ${inserted}, 이미 있음(건너뜀) ${skipped}, 기준점 없음 ${noMarker}`);
