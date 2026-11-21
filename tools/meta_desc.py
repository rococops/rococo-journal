"""메타 설명 만들기 — tools/meta_desc.mjs 의 파이썬판 (build_pages.py용).
본문 앞부분 원문 문장을 이어 붙여 120~160자로 맞춘다. 새 문장을 지어내지 않는다.
인사말·날짜·자기소개·소제목 줄, 가격·할인·효과 단정 표현이 든 문장은 건너뛴다.
규칙을 바꾸면 meta_desc.mjs 도 같이 고친다."""
import html
import re

META_MIN = 120
META_MAX = 160

BANNED = re.compile(
    r'(\d[\d,.]*\s*만?\s*원(?![가-힣])|가격|비용|할인|이벤트|저렴|무료|최저가|100\s*%|완벽|최고|최초|유일|반드시|확실|보장|'
    r'(?:부작용|통증|붓기|흉터|멍)\s*(?:이|가|은|는|도)?\s*(?:전혀\s*|거의\s*)?(?:없|남지\s*않|보이지\s*않|안\s*보))')
TERMINAL = re.compile(r'[.!?。…~^)\]"\'”’]$|[다요죠까네]$')
CONNECT = re.compile(r'[,，]$|[면고며서데는은을를에와과며니만게듯도]$')
SPLIT = re.compile(r'(?:(?<=[.!?。])|(?<=니다)|(?<=세요)|(?<=어요)|(?<=에요)|(?<=예요)|(?<=해요)|(?<=네요)|(?<=군요))\s+')


def _is_junk(s):
    t = s.strip()
    if len(t) < 6:
        return True
    if re.fullmatch(r'[\d\s.\-/년월일()]+', t):
        return True
    if re.fullmatch(r'[-=*~_·•\s]+', t) or t.startswith('---'):
        return True
    if re.match(r'(원문|출처|※|\*\*)', t):
        return True
    if len(t) < 30 and re.match(r'(안녕하세요|안녕하십니까|반갑습니다)', t):
        return True
    if len(t) < 40 and re.search(r'(김상호|로코코|원장)[^.!?]{0,20}(입니다|이에요|예요)[.!~^\s]*$', t):
        return True
    return False


def _norm(s):
    return re.sub(r'[.…]+$', '', re.sub(r'\s+', '', s))


def paragraphs_from_html(h):
    h = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', h or '', flags=re.I)
    h = re.sub(r'<div class="(?:tldr-box|translate-notice)"[\s\S]*?</div>', '', h, flags=re.I)
    h = re.sub(r'<figcaption[\s\S]*?</figcaption>', '', h, flags=re.I)
    out = []
    for m in re.finditer(r'<(p|li)\b[^>]*>([\s\S]*?)</\1>', h, flags=re.I):
        t = re.sub(r'<br\s*/?>', ' ', m.group(2), flags=re.I)
        t = html.unescape(re.sub(r'<[^>]+>', '', t)).replace('\xa0', ' ')
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            out.append(t)
    return out


def _tidy(lines):
    out, buf = [], ''
    for raw in lines:
        l = raw.strip()
        if not l:
            continue
        heading = (not TERMINAL.search(l) and not CONNECT.search(l)
                   and (re.search(r'\s[+\-–]\s|\+', l) or len(l) < 40))
        if heading:
            if buf:
                out.append(buf)
                buf = ''
            continue
        buf = f'{buf} {l}' if buf else l
        if not CONNECT.search(l):
            out.append(buf)
            buf = ''
    if buf:
        out.append(buf)
    return out


def _sentences(p):
    out = []
    for s in SPLIT.split(p):
        s = re.sub(r'^[&*·•\-–\s]+', '', s.strip())
        if s:
            out.append(s)
    return out


def build_meta_description(lead='', paragraphs=(), title=''):
    parts, seen = [], []
    length = 0

    def add(s):
        nonlocal length
        length += (1 if parts else 0) + len(s)
        parts.append(s)
        seen.append(_norm(s))

    def dup(s):
        n = _norm(s)
        return (not n) or any(x in n or n in x for x in seen)

    lead_t = re.sub(r'\s+', ' ', lead or '').strip()
    pool = []
    if lead_t and not re.search(r'(\.\.|…)$', lead_t) and not _is_junk(lead_t):
        pool += _sentences(lead_t)
    for p in _tidy(list(paragraphs)):
        pool += _sentences(p)

    for s in pool:
        if length >= META_MIN:
            break
        if _is_junk(s) or BANNED.search(s) or dup(s):
            continue
        extra = (1 if parts else 0) + len(s)
        if length + extra <= META_MAX:
            add(s)
            continue
        room = META_MAX - length - (1 if parts else 0) - 1
        if room >= 15:
            cut = s[:room]
            sp = cut.rfind(' ')
            if sp > room * 0.6:
                cut = cut[:sp]
            add(re.sub(r'[,·\s]+$', '', cut) + '…')
        break
    out = ' '.join(parts)
    t = re.sub(r'\s+', ' ', title or '').strip()
    if len(out) < META_MIN and t and t not in out:
        out = f'{t} — {out}' if out else t
        if len(out) > META_MAX:
            out = re.sub(r'\s+\S*$', '', out[:META_MAX - 1]) + '…'
    return out


def apply_meta_description(page, desc):
    """생성된 상세 페이지 HTML의 메타 설명·og:description·JSON-LD 첫 description을 desc로 바꾼다.
    (화면 요약 article-summary·tldr-box는 그대로 둔다)"""
    if not desc:
        return page
    e = html.escape(desc, quote=True)
    page = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + e + m.group(2), page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + e + m.group(2), page, count=1)
    j = json_escape(desc)
    page = re.sub(r'("description"\s*:\s*")((?:[^"\]|\.)*)(")', lambda m: m.group(1) + j + m.group(3), page, count=1)
    return page


def json_escape(s):
    import json
    return json.dumps(s, ensure_ascii=False)[1:-1].replace('<', '\u003c')
