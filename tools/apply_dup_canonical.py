"""같은 글이 여러 카테고리에 올라간 케이스 페이지의 canonical 을 대표 주소 하나로 모은다 (11/24, 중복 사례 1안).

- 대상: 한국어 숫자 페이지(예: nose/revision/315/) 중 제목과 메타 설명이 둘 다 같은 묶음.
- 대표: 묶음 안에서 rococops.com 원글을 가리키는 페이지가 있으면, 그중 원글 id 가 가장 작은 원글 URL.
         원글이 하나도 없으면(칼럼 등) 번호가 가장 작은 저널 페이지 자기 주소.
- 카테고리 목록·페이지 주소·화면은 바꾸지 않는다. canonical 한 줄만 바꾼다.
- 기본은 미리보기. 실제로 쓰려면 --write. 줄바꿈은 파일 원래대로 둔다.

사용:
  python tools/apply_dup_canonical.py           # 미리보기
  python tools/apply_dup_canonical.py --write   # 적용
"""
import os, re, sys, argparse, collections

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SKIP = ('.claude', 'en', 'ja', 'zh', 'node_modules', '.git')
CANON_RE = re.compile(r'(<link rel="canonical" href=")([^"]*)(")')
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
MAIN_ID_RE = re.compile(r'rococops\.com/htm/sitecontents_read\.php\?id=(\d+)')


def pages():
    for top in sorted(os.listdir(BASE)):
        if top in SKIP or not os.path.isdir(os.path.join(BASE, top)):
            continue
        for root, _, files in os.walk(os.path.join(BASE, top)):
            rel = os.path.relpath(root, BASE).replace(os.sep, '/')
            if 'index.html' in files and re.search(r'/\d+$', rel):
                yield rel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--list', action='store_true', help='묶음별 대표와 대상 출력')
    a = ap.parse_args()

    groups = collections.defaultdict(list)
    for rel in pages():
        s = open(os.path.join(BASE, rel, 'index.html'), 'rb').read().decode('utf-8')
        t, d, c = TITLE_RE.search(s), DESC_RE.search(s), CANON_RE.search(s)
        if not (t and d and c):
            continue
        groups[(t.group(1).strip(), d.group(1).strip())].append((rel, c.group(2)))

    stat = collections.Counter()
    for (title, _), items in sorted(groups.items()):
        if len(items) < 2:
            continue
        stat['묶음'] += 1
        mains = [(int(m.group(1)), url) for _, url in items if (m := MAIN_ID_RE.search(url))]
        if mains:
            rep = min(mains)[1]
        else:
            rel0 = min(items, key=lambda x: int(x[0].rsplit('/', 1)[1]))[0]
            rep = f'https://journal.rococops.com/{rel0}/'
        if a.list:
            print(f'\n[{len(items)}] {title[:60]}\n  대표: {rep}')
        for rel, url in items:
            if url == rep:
                stat['이미 대표'] += 1
                continue
            stat['변경'] += 1
            if a.list:
                print(f'  {rel}: {url} -> 대표')
            if a.write:
                f = os.path.join(BASE, rel, 'index.html')
                s = open(f, 'rb').read().decode('utf-8')
                m = CANON_RE.search(s)
                s = s[:m.start(2)] + rep + s[m.end(2):]
                open(f, 'wb').write(s.encode('utf-8'))
    for k, n in stat.items():
        print(f'{k}: {n}')
    print('(파일 수정됨)' if a.write else '(미리보기)')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
