// 기존 글 상세 페이지의 짧은 메타 설명(120자 미만)을 본문 앞부분 원문 발췌(120~160자)로 바꾼다.
// 대상: 케이스 글(카테고리/하위/번호) + 성형 가이드(guide/슬러그). 목록·대표페이지·후기·외국어 페이지는 제외.
// 바꾸는 곳: <meta name="description">, og:description, twitter:description, JSON-LD "description".
// 화면에 보이는 요약(article-summary, tldr-box)은 건드리지 않는다.
// 사용: node tools/fix_meta_desc.mjs            (미리보기, 파일 안 바꿈)
//       node tools/fix_meta_desc.mjs --write    (실제 반영)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildMetaDescription, paragraphsFromHtml, META_MIN } from './meta_desc.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const WRITE = process.argv.includes('--write');
const CATS = ['nose', 'nostril', 'cheekbone', 'eye', 'forehead', 'anti-aging', 'etc'];

function targets() {
  const out = [];
  for (const c of CATS) {
    const cd = path.join(ROOT, c);
    if (!fs.existsSync(cd)) continue;
    for (const sub of fs.readdirSync(cd)) {
      const sd = path.join(cd, sub);
      if (!fs.statSync(sd).isDirectory()) continue;
      for (const slug of fs.readdirSync(sd)) {
        if (!/^c?\d+$/.test(slug)) continue;
        const f = path.join(sd, slug, 'index.html');
        if (fs.existsSync(f)) out.push(f);
      }
    }
  }
  const gd = path.join(ROOT, 'guide');
  for (const slug of fs.readdirSync(gd)) {
    const f = path.join(gd, slug, 'index.html');
    if (fs.existsSync(f)) out.push(f);
  }
  return out;
}

const htmlUnesc = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#0?39;/g, "'").replace(/&amp;/g, '&');
const htmlEsc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const jsonEsc = s => JSON.stringify(s).slice(1, -1).replace(/</g, '\\u003c');
const loose = s => s.replace(/\\(.)/g, '$1').replace(/\s+/g, '');

const META_RX = /(<meta\s+name="description"\s+content=")([^"]*)(")/i;
const stats = { scanned: 0, short: 0, changed: 0, stillShort: [], jsonMiss: [] };
const samples = [];

for (const f of targets()) {
  stats.scanned++;
  let s = fs.readFileSync(f, 'utf8');
  const m = s.match(META_RX);
  if (!m) continue;
  const old = htmlUnesc(m[2]).trim();
  if (old.length >= META_MIN) continue;
  stats.short++;

  const a = s.indexOf('<div class="article-content">');
  if (a < 0) { stats.stillShort.push([f, old.length, 'no-body']); continue; }
  const ends = ['<div class="guide-sources"', '<!-- 상담 인라인 CTA -->', '<div class="inline-cta"', '</article>']
    .map(k => s.indexOf(k, a)).filter(i => i > 0);
  const body = s.slice(a, Math.min(...ends));
  const t = s.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  const title = t ? htmlUnesc(t[1].replace(/<[^>]+>/g, '')).trim() : '';

  const desc = buildMetaDescription({ lead: old, paragraphs: paragraphsFromHtml(body), title });
  if (desc.length <= old.length) { stats.stillShort.push([f, old.length, 'no-better']); continue; }
  if (desc.length < META_MIN) stats.stillShort.push([f, desc.length, 'short-body']);

  const e = htmlEsc(desc);
  s = s.replace(META_RX, `$1${e}$3`);
  s = s.replace(/(<meta\s+property="og:description"\s+content=")[^"]*(")/i, `$1${e}$2`);
  s = s.replace(/(<meta\s+name="twitter:description"\s+content=")[^"]*(")/i, `$1${e}$2`);
  // JSON-LD: 기존 설명과 같은 값의 "description"만 교체 (다른 객체의 설명은 그대로)
  let hit = 0;
  s = s.replace(/("description"\s*:\s*")((?:[^"\\]|\\.)*)(")/g, (all, p1, v, p3) => {
    if (loose(v) === loose(old) || loose(htmlUnesc(v)) === loose(old)) { hit++; return p1 + jsonEsc(desc) + p3; }
    return all;
  });
  if (!hit) {
    // JSON-LD 설명이 메타와 다르게 적힌 페이지: 첫 번째 "description" 하나만 교체
    stats.jsonMiss.push(f);
    s = s.replace(/("description"\s*:\s*")((?:[^"\\]|\\.)*)(")/,(all, p1, v, p3) => p1 + jsonEsc(desc) + p3);
  }

  stats.changed++;
  samples.push([path.relative(ROOT, f).replace(/\\/g, '/'), old, desc]);
  if (WRITE) fs.writeFileSync(f, s, 'utf8');
}

const rel = f => path.relative(ROOT, f).replace(/\\/g, '/');
console.log(JSON.stringify({ mode: WRITE ? 'write' : 'dry-run', scanned: stats.scanned, short: stats.short, changed: stats.changed,
  stillShort: stats.stillShort.length, jsonMiss: stats.jsonMiss.length }));
fs.writeFileSync(path.join(process.env.TEMP || '.', 'meta_desc_report.json'), JSON.stringify({
  samples, stillShort: stats.stillShort.map(([f, n, why]) => [rel(f), n, why]), jsonMiss: stats.jsonMiss.map(rel) }, null, 1), 'utf8');
