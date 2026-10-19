"""대표페이지 데이터(data/landing/*.json)의 모든 인용이 원문 칼럼과 일치하는지 대조.

원장님 글은 재작성 금지이므로, 데이터 파일에 들어간 문장을 문장 단위로 잘라
src 칼럼 본문(article-content)에 그대로 들어있는지 확인한다. 하나라도 어긋나면 종료코드 1.

사용: python tools/verify_landing_quotes.py [data/landing/nose-hump.json ...]
"""
import sys, os, re, json, glob, html

sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

_cache = {}


def article_text(src):
    """칼럼 본문을 태그 제거·공백 정규화한 텍스트로 반환."""
    if src not in _cache:
        raw = open(os.path.join(BASE, src, 'index.html'), encoding='utf-8-sig').read()
        m = re.search(r'<div class="article-content">(.*?)</article>', raw, re.S)
        body = m.group(1) if m else ''
        _cache[src] = (raw, re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body))))
    return _cache[src]


def check(label, src, text, results):
    """text 를 문장 단위로 잘라 원문에 모두 있는지 확인."""
    _, body = article_text(src)
    missing = [f for f in (re.sub(r'\s+', ' ', s).strip() for s in re.split(r'(?<=[.?])\s+', text))
               if f and f not in body]
    results.append((not missing, label, src, missing))


def verify(data):
    r = []
    h = data['hero']
    check('hero.summary', h['summary']['src'], h['summary']['text'], r)
    for i, s in enumerate(h['stats']):
        check(f'hero.stats[{i}].quote', s['src'], s['quote'], r)
    f = data['features']
    for i, t in enumerate(f['items']):
        check(f'features.items[{i}]', f['src'], t, r)
    check('features.note', f['src'], f['note'], r)
    for bi, b in enumerate(data['story']['blocks']):
        for pi, p in enumerate(b['paras']):
            check(f'story[{bi}].paras[{pi}]', b['src'], p, r)
    m = data['method']
    for i, s in enumerate(m['steps']):
        check(f'method.steps[{i}]', m['steps_src'], s['text'], r)
    check('method.note', m['note']['src'], m['note']['text'], r)
    for i, p in enumerate(m['pros_cons']['paras']):
        check(f'method.pros_cons[{i}]', m['pros_cons']['src'], p, r)
    rec = data['recovery']
    for it in rec['items']:
        for li, line in enumerate(it['lines']):
            check(f'recovery[{it["label"]}][{li}]', it['src'], line, r)
    check('recovery.note', rec['note']['src'], rec['note']['text'], r)
    for i, q in enumerate(data['faq']):
        check(f'faq[{i}]', q['src'], q['a'], r)
    # 전후사진: 이미지 URL 과 캡션이 해당 칼럼 원본 HTML 에 있어야 함
    for it in data['before_after']['items'] + [data['hero']['case']]:
        raw, body = article_text(it['src'])
        missing = [x for x in (it['image'], it.get('caption')) if x and x not in raw and x not in body]
        r.append((not missing, 'before_after', it['src'], missing))
    return r


def main():
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(BASE, 'data', 'landing', '*.json')))
    bad = 0
    for p in paths:
        data = json.load(open(p, encoding='utf-8'))
        print(f'== {os.path.basename(p)}')
        for ok, label, src, missing in verify(data):
            print(f'  {"OK  " if ok else "MISS"} {label:28} {src}' + ('' if ok else f'  {missing}'))
            bad += not ok
    print(f'\n불일치 {bad}건')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
