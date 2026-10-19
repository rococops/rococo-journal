"""대표페이지 제작 보조 도구: 칼럼 본문을 '줄 번호'로 다루고, 줄 범위를 그대로 이어붙여 원문 인용을 만든다.

원장님 글은 재작성 금지이므로 문장을 직접 타이핑하지 않고, 칼럼 본문의 줄 범위를 seg()로 가져온다.
(만든 데이터는 tools/verify_landing_quotes.py 로 원문과 대조한다.)

명령줄:
  python tools/landing_lib.py list  cheekbone/quick            # 하위 메뉴의 칼럼 목록 (번호 | 제목 | 글자수 | 이미지 수)
  python tools/landing_lib.py scan  cheekbone/quick [N]        # 설명 위주 글 후보를 점수순으로 N개 (기본 25)
  python tools/landing_lib.py dump  cheekbone/quick/19 [시작 끝] # 본문을 줄 번호와 함께 출력
  python tools/landing_lib.py win   cheekbone/quick/19 키워드 [앞 뒤]   # 키워드가 처음 나오는 곳 주변 줄
  python tools/landing_lib.py grep  cheekbone/quick 키워드      # 하위 메뉴 전체 칼럼에서 키워드가 든 줄 (많이 반복되는 문장순)
  python tools/landing_lib.py images cheekbone/quick/19        # 칼럼의 이미지 URL과 바로 뒤 캡션 (전후사진·히어로 후보)

파이썬에서:
  from landing_lib import seg, lines
  seg('cheekbone/quick/19', (3, 6), 10)   # 3~6줄과 10번째 줄을 공백 한 칸으로 이어붙인 문자열
"""
import sys, os, re, glob, html

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
_NOTICE = ('🌐', 'This article', '!function')
_cache = {}


def _read(src):
    return open(os.path.join(BASE, src, 'index.html'), encoding='utf-8-sig').read()


def lines(src):
    """칼럼 src(예: 'cheekbone/quick/19')의 본문을 줄 단위 리스트로. 이미지 자리·번역 안내문 제외."""
    if src not in _cache:
        s = _read(src)
        i = s.find('<div class="article-content">')
        if i < 0:
            i = s.find('<article')
        j = s.find('</article>', i)
        seg_ = re.sub(r'<script.*?</script>', '', s[i:j], flags=re.S)
        seg_ = re.sub(r'<img[^>]*>', '\n[IMG]\n', seg_)
        seg_ = re.sub(r'</(p|div|h[1-6]|li|blockquote)>|<br\s*/?>', '\n', seg_)
        t = html.unescape(re.sub(r'<[^>]+>', '', seg_))
        L = [l.strip() for l in t.split('\n') if l.strip()]
        _cache[src] = [l for l in L if l != '[IMG]' and not l.startswith(_NOTICE)]
    return _cache[src]


def seg(src, *ranges):
    """줄 범위(양 끝 포함, 'a,b' 튜플 또는 정수 하나)들을 공백 한 칸으로 이어붙임. 줄머리의 '- ', '1. ' 번호는 뗀다."""
    out = []
    L = lines(src)
    for r in ranges:
        lo, hi = (r, r) if isinstance(r, int) else r
        for l in L[lo:hi + 1]:
            out.append(re.sub(r'^(-|\d+\.)\s+', '', l))
    return ' '.join(out)


def title(src):
    """칼럼 H1(원장님이 붙인 원래 제목)."""
    raw = _read(src)
    m = re.search(r'<h1 class="article-title">(.*?)</h1>', raw, re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''


def articles(sub):
    """하위 메뉴('cheekbone/quick')의 칼럼 src 목록."""
    out = []
    for d in glob.glob(os.path.join(BASE, sub, '*', 'index.html')):
        name = os.path.basename(os.path.dirname(d))
        if name != 'reviews':
            out.append(f'{sub}/{name}')
    return sorted(out, key=lambda x: (not x.split('/')[-1].lstrip('c').isdigit(), int(re.sub(r'\D', '', x.split('/')[-1]) or 0)))


_EXPL = ['이유', '방법', '총정리', '부작용', '?', '차이', '원리', '종류', '단점', '장점', '비교', '궁금', '설명', '기준', '주의',
         '가능한가', '정리', '한계', '질문', '회복', '효과']


def _cmd_list(sub):
    for a in articles(sub):
        L = lines(a)
        print(f'{a.split("/")[-1]:>6} | {title(a)[:60]} | {sum(len(x) for x in L)}자 | 이미지 {len(re.findall("<img", _read(a)))}')


def _cmd_scan(sub, n=25):
    rows = []
    for a in articles(sub):
        L = lines(a)
        chars = sum(len(x) for x in L)
        t = title(a)
        score = sum(2 for k in _EXPL if k in t) + chars / 1500 + sum(1 for x in L if re.search(r'(저는|제가|개인적으로)', x)) / 10
        rows.append((score, a, t, chars))
    for sc, a, t, chars in sorted(rows, reverse=True)[:n]:
        print(f'{sc:5.1f} | {a.split("/")[-1]:>6} | {t[:56]} | {chars}자')


def _cmd_dump(src, lo=0, hi=9999):
    L = lines(src)
    print(f'##### {src} | {title(src)} | {len(L)}줄')
    for i, l in enumerate(L[lo:hi + 1], lo):
        print(f'{i:3d} {l[:170]}')


def _cmd_win(src, kw, b=4, f=8):
    L = lines(src)
    print(f'##### {src} | {title(src)}')
    for i, l in enumerate(L):
        if kw in l:
            for j in range(max(0, i - b), min(len(L), i + f + 1)):
                print(f'{j:3d} {L[j][:170]}')
            return
    print('(없음)')


def _cmd_grep(sub, kw):
    hits = {}
    for a in articles(sub):
        for i, l in enumerate(lines(a)):
            if kw in l and 10 < len(l) < 140:
                hits.setdefault(l, []).append((a.split('/')[-1], i))
    for l, ns in sorted(hits.items(), key=lambda x: -len(x[1]))[:60]:
        print(f'{len(ns):2d}회 {ns[0][0]:>6}:{ns[0][1]:<3} | {l}')


def _cmd_images(src):
    raw = _read(src)
    i = raw.find('<div class="article-content">')
    body = raw[i:raw.find('</article>', i)]
    seq = []
    for m in re.finditer(r'<img[^>]*?src="([^"]+)"[^>]*>|<p>(.*?)</p>', body, re.S):
        if m.group(1):
            seq.append(('img', m.group(1)))
        else:
            t = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
            if t:
                seq.append(('t', t))
    for k, (a, v) in enumerate(seq):
        if a == 'img':
            cap = seq[k + 1][1] if k + 1 < len(seq) and seq[k + 1][0] == 't' else ''
            print(f'{v} | {cap[:60]}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    cmds = {'list': _cmd_list, 'scan': _cmd_scan, 'dump': _cmd_dump, 'win': _cmd_win, 'grep': _cmd_grep, 'images': _cmd_images}
    if len(sys.argv) < 3 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    args = [int(x) if x.isdigit() and sys.argv[1] in ('scan', 'dump') else x for x in sys.argv[3:]]
    if sys.argv[1] == 'win':
        args = [sys.argv[3]] + [int(x) for x in sys.argv[4:]]
    cmds[sys.argv[1]](sys.argv[2], *args)
