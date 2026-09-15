// postscript.sql / postscript_cmt.sql → 안전 파싱 + 개인정보 제거 + 공개글만 필터
import { readFileSync, writeFileSync } from 'node:fs';

const COLS = ['num','category','userid','writer','email','hp','subject','contents','Pwd',
  'attach1','attach2','attach3','attach4','attach5','attach6','visited','udate',
  'isbest','isauth','isnoti','ishtml','ip','isopen','isreply','url','ismobile',
  'writegubun','sns','branch','recommend','isselca'];

function parseInsertValues(sqlText) {
  const rows = [];
  const inserts = sqlText.split(/INSERT INTO `postscript`[^V]*VALUES\s*/).slice(1);
  for (const block of inserts) {
    let i = 0, n = block.length;
    while (i < n) {
      while (i < n && /[\s,]/.test(block[i])) i++;
      if (block[i] !== '(') break;
      i++; // skip (
      const vals = [];
      while (true) {
        while (i < n && /\s/.test(block[i])) i++;
        if (block[i] === "'") {
          i++; let s = '';
          const ESC = { n: '\n', r: '\r', t: '\t', '0': '\0', 'Z': '\x1a', '\\': '\\', "'": "'", '"': '"' };
          while (i < n) {
            if (block[i] === '\\') {
              const c = block[i+1];
              s += (c in ESC) ? ESC[c] : c;
              i += 2; continue;
            }
            if (block[i] === "'" ) {
              if (block[i+1] === "'") { s += "'"; i += 2; continue; }
              i++; break;
            }
            s += block[i]; i++;
          }
          vals.push(s);
        } else if (block.startsWith('NULL', i)) {
          vals.push(null); i += 4;
        } else {
          let s = '';
          while (i < n && block[i] !== ',' && block[i] !== ')') { s += block[i]; i++; }
          vals.push(s.trim());
        }
        while (i < n && /\s/.test(block[i])) i++;
        if (block[i] === ',') { i++; continue; }
        if (block[i] === ')') { i++; break; }
        break;
      }
      if (vals.length === COLS.length) {
        const row = {};
        COLS.forEach((c, idx) => row[c] = vals[idx]);
        rows.push(row);
      }
      while (i < n && /[\s,;]/.test(block[i])) i++;
      if (block[i] === undefined || block.slice(i, i+11).toUpperCase() === 'INSERT INTO') break;
    }
  }
  return rows;
}

const sql = readFileSync('postscript.sql', 'utf8');
const all = parseInsertValues(sql);
console.log('파싱된 전체 행: ' + all.length);

const stripHtml = s => (s || '')
  .replace(/<br\s*\/?>/gi, '\n')
  .replace(/<\/p>/gi, '\n')
  .replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"')
  .replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim();

// isopen='Y' 인 것만 (비공개 처리된 글 제외 — 원 작성자가 공개 안 하기로 한 것)
const publicRows = all.filter(r => r.isopen === 'Y');
console.log('공개(isopen=Y): ' + publicRows.length + ' / 비공개 제외: ' + (all.length - publicRows.length));

// 개인정보 컬럼 완전 제거한 안전본 생성 (hp, email, userid, ip, Pwd 제거)
const safe = publicRows.map(r => ({
  num: r.num,
  category: r.category,
  writer: r.writer,               // 화면에 원래 노출되던 닉네임/이름 — 저널 사용 시 별도 익명화 예정
  subject: r.subject,
  contents_text: stripHtml(r.contents),
  contents_len: stripHtml(r.contents).length,
  photos: [r.attach1, r.attach2, r.attach3, r.attach4, r.attach5, r.attach6].filter(Boolean),
  visited: Number(r.visited) || 0,
  udate: r.udate,
  isbest: r.isbest,
  isauth: r.isauth,
}));

writeFileSync('postscript_safe.json', JSON.stringify(safe, null, 1), 'utf8');
console.log('저장: postscript_safe.json (개인정보 컬럼 제거됨: hp/email/userid/ip/Pwd)');
console.log('평균 본문 길이: ' + Math.round(safe.reduce((a,b)=>a+b.contents_len,0)/safe.length) + '자');
console.log('사진 있는 글: ' + safe.filter(s=>s.photos.length).length + '개');
