// 메타 설명(meta description) 만들기 — 본문 앞부분 원문 문장을 이어 붙여 120~160자로 맞춘다.
// 원칙: 새 문장을 지어내지 않는다(원문 그대로 발췌). 인사말·날짜·자기소개 줄과
//       가격·할인·효과 단정 표현이 든 문장은 건너뛴다.
// 사용처: api/publish.js(케이스 글), tools/guide.mjs(성형 가이드), tools/fix_meta_desc.mjs(기존 페이지 일괄 반영)
// tools/meta_desc.py 는 이 파일의 파이썬판(build_pages.py용) — 규칙을 바꾸면 둘 다 고친다.

export const META_MIN = 120;
export const META_MAX = 160;

// 가격·할인·효과 단정 표현 (이런 문장은 설명에 넣지 않음)
const BANNED = /(\d[\d,.]*\s*만?\s*원(?![가-힣])|가격|비용|할인|이벤트|저렴|무료|최저가|100\s*%|완벽|최고|최초|유일|반드시|확실|보장|(?:부작용|통증|붓기|흉터|멍)\s*(?:이|가|은|는|도)?\s*(?:전혀\s*|거의\s*)?(?:없|남지\s*않|보이지\s*않|안\s*보))/;

// 설명으로 쓸 수 없는 줄: 날짜, 인사말, 자기소개, 구분선, 원문 표시 등
function isJunk(s) {
  const t = s.trim();
  if (t.length < 6) return true;
  if (/^[\d\s.\-\/년월일()]+$/.test(t)) return true;                       // 날짜만
  if (/^[-=*~_·•\s]+$/.test(t) || /^-{3,}/.test(t)) return true;            // 구분선
  if (/^(원문|출처|※|\*\*)/.test(t)) return true;
  if (t.length < 30 && /^(안녕하세요|안녕하십니까|반갑습니다)/.test(t)) return true;
  if (t.length < 40 && /(김상호|로코코|원장)[^.!?]{0,20}(입니다|이에요|예요)[.!~^\s]*$/.test(t)) return true;
  return false;
}

function norm(s) { return s.replace(/\s+/g, '').replace(/[.…]+$/, ''); }

function decodeEntities(s) {
  return s.replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#0?39;|&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
    .replace(/&amp;/g, '&');
}

// 본문 HTML → 문단 텍스트 배열 (<p>, <li>만; 요약 상자·안내문·스크립트 제외)
export function paragraphsFromHtml(html) {
  let h = String(html || '')
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<div class="(?:tldr-box|translate-notice)"[\s\S]*?<\/div>/gi, '')
    .replace(/<figcaption[\s\S]*?<\/figcaption>/gi, '');
  const out = [];
  const rx = /<(p|li)\b[^>]*>([\s\S]*?)<\/\1>/gi;
  let m;
  while ((m = rx.exec(h))) {
    const t = decodeEntities(m[2].replace(/<br\s*\/?>/gi, ' ').replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
    if (t) out.push(t);
  }
  return out;
}

// 본문 줄 다듬기: 소제목 줄(마침표 없고 '+'·' - '가 있거나 짧은 줄)은 빼고,
// 문장 중간에서 끊긴 줄(쉼표·연결어미로 끝남)은 다음 줄과 이어 붙인다.
const TERMINAL = /[.!?。…~^)\]"'”’]$|[다요죠까네]$/;
const CONNECT = /[,，]$|[면고며서데는은을를에와과며니만게듯도]$/;
function tidyLines(lines) {
  const out = [];
  let buf = '';
  for (const raw of lines) {
    const l = raw.trim();
    if (!l) continue;
    const isHeading = !TERMINAL.test(l) && !CONNECT.test(l) && (/\s[+\-–]\s|\+/.test(l) || l.length < 40);
    if (isHeading && !buf) continue;
    if (isHeading) { out.push(buf); buf = ''; continue; }
    buf = buf ? `${buf} ${l}` : l;
    if (!CONNECT.test(l)) { out.push(buf); buf = ''; }
  }
  if (buf) out.push(buf);
  return out;
}

function sentences(p) {
  // 마침표 뒤, 또는 마침표 없이 끝난 존댓말 어미(~니다, ~세요, ~어요 등) 뒤에서 나눈다
  return p.split(/(?<=[.!?。]|니다|세요|어요|에요|예요|해요|네요|군요)\s+/)
    .map(s => s.trim().replace(/^[&*·•\-–\s]+/, '')).filter(Boolean);
}

// lead: 기존 요약(있으면 맨 앞에). 끝이 '..'/'…'로 잘린 요약이나 인사말이면 쓰지 않는다.
// paragraphs: 본문 문단 텍스트 배열. title: 본문이 너무 짧을 때만 앞에 붙인다.
export function buildMetaDescription({ lead = '', paragraphs = [], title = '' } = {}) {
  const parts = [];
  const seen = [];
  let len = 0;
  const add = (s) => { parts.push(s); seen.push(norm(s)); len += (parts.length > 1 ? 1 : 0) + s.length; };
  const dup = (s) => { const n = norm(s); return !n || seen.some(x => x.includes(n) || n.includes(x)); };

  const leadT = String(lead || '').replace(/\s+/g, ' ').trim();
  const pool = [];
  if (leadT && !/(\.\.|…)$/.test(leadT) && !isJunk(leadT)) pool.push(...sentences(leadT));
  for (const p of tidyLines(paragraphs)) pool.push(...sentences(p));

  for (const s of pool) {
    if (len >= META_MIN) break;
    if (isJunk(s) || BANNED.test(s) || dup(s)) continue;
    const extra = (parts.length ? 1 : 0) + s.length;
    if (len + extra <= META_MAX) { add(s); continue; }
    // 이 문장을 다 넣으면 160자를 넘는다 → 아직 120자 미만이면 단어 경계에서 잘라 넣는다
    const room = META_MAX - len - (parts.length ? 1 : 0) - 1;
    if (room >= 15) {
      let cut = s.slice(0, room);
      const sp = cut.lastIndexOf(' ');
      if (sp > room * 0.6) cut = cut.slice(0, sp);
      add(cut.replace(/[,·\s]+$/, '') + '…');
    }
    break;
  }
  let out = parts.join(' ');
  // 본문이 너무 짧으면 제목을 앞에 붙인다
  const t = String(title || '').replace(/\s+/g, ' ').trim();
  if (out.length < META_MIN && t && !out.includes(t)) {
    out = out ? `${t} — ${out}` : t;
    if (out.length > META_MAX) out = out.slice(0, META_MAX - 1).replace(/\s+\S*$/, '') + '…';
  }
  return out;
}
