#!/usr/bin/env python3
"""검색 노출용 후처리 (여러 번 실행해도 같은 결과). 사이트맵에 있는 페이지만 다룬다.

1. 글꼴 CDN 미리 연결(preconnect) 한 줄 추가 — 첫 화면 글자 표시가 빨라짐
2. 대표페이지 구조화데이터(MedicalWebPage·CollectionPage)에 dateModified 가 없으면
   그 파일의 마지막 git 커밋 날짜로 채움 (이미 있으면 건드리지 않음)
3. 성형 가이드 본문 사진(guide-figure)에 width/height 를 넣음 — 로딩 중 화면 밀림 방지.
   원본 서버 사진 크기는 data/img_dims.json 에 저장해 두고 다시 받지 않음

사용: python tools/seo_postprocess.py            (전체)
      python tools/seo_postprocess.py --guides   (가이드 사진 크기만 — GitHub Actions 용)
"""
import io
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'https://journal.rococops.com'
DIMS_PATH = os.path.join(ROOT, 'data', 'img_dims.json')
FONT_LINK = '<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">'
PRECONNECT = '<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>'
LD_BLOCK = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
LD_URL_LINE = re.compile(r'("@type": "(?:MedicalWebPage|CollectionPage)",.*?\n([ \t]*)"url": "[^"\n]*",)', re.S)
FIGURE_IMG = re.compile(r'(<figure class="guide-figure"><img )(src="([^"]+)")((?:(?!width=)[^>])*>)')


def sitemap_pages():
    """사이트맵 주소 → (주소 경로, 로컬 index.html 경로)"""
    s = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    out = []
    for path in re.findall(r'<loc>' + re.escape(BASE_URL) + r'/(.*?)</loc>', s):
        f = os.path.join(ROOT, path.replace('/', os.sep), 'index.html') if path else os.path.join(ROOT, 'index.html')
        if os.path.isfile(f):
            out.append((path, f))
    return out


def git_date(path):
    try:
        r = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path], cwd=ROOT, capture_output=True, text=True)
        return r.stdout.strip()
    except OSError:
        return ''


def add_preconnect(t):
    if PRECONNECT in t or FONT_LINK not in t:
        return t
    return t.replace(FONT_LINK, PRECONNECT + '\n' + FONT_LINK, 1)


def add_date_modified(t, path):
    date = None

    def block(m):
        nonlocal date
        body = m.group(2)
        if '"dateModified"' in body or not LD_URL_LINE.search(body):
            return m.group(0)
        if date is None:
            date = git_date(path)
        if not date:
            return m.group(0)
        body = LD_URL_LINE.sub(lambda u: u.group(1) + '\n' + u.group(2) + '"dateModified": "%s",' % date, body, count=1)
        return m.group(1) + body + m.group(3)

    return LD_BLOCK.sub(block, t)


def image_size(url, cache):
    if url in cache:
        return cache[url]
    from PIL import ImageFile
    size = None
    try:
        if url.startswith('http'):
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-131071'})
            data = urllib.request.urlopen(req, timeout=20).read(131072)
        else:
            data = open(os.path.join(ROOT, url.lstrip('/').replace('/', os.sep)), 'rb').read(131072)
        p = ImageFile.Parser()
        p.feed(data)
        if p.image:
            size = list(p.image.size)
    except Exception as e:  # 크기를 못 구하면 그 사진은 건너뜀
        print('  크기 확인 실패: %s (%s)' % (url, e))
    if size:
        cache[url] = size
    return size


def add_figure_dims(t, cache):
    def img(m):
        size = image_size(m.group(3), cache)
        if not size:
            return m.group(0)
        return '%s%s width="%d" height="%d"%s' % (m.group(1), m.group(2), size[0], size[1], m.group(4))

    return FIGURE_IMG.sub(img, t)


def main():
    guides_only = '--guides' in sys.argv
    cache = json.load(open(DIMS_PATH, encoding='utf-8')) if os.path.isfile(DIMS_PATH) else {}
    before = json.dumps(cache, sort_keys=True)
    changed = 0
    for path, f in sitemap_pages():
        is_guide = path.startswith('guide/') and path != 'guide/'
        if guides_only and not is_guide:
            continue
        t = open(f, encoding='utf-8', newline='').read()
        t2 = t
        if not guides_only:
            t2 = add_date_modified(add_preconnect(t2), f)
        if is_guide:
            t2 = add_figure_dims(t2, cache)
        if t2 != t:
            open(f, 'w', encoding='utf-8', newline='').write(t2)
            changed += 1
    if json.dumps(cache, sort_keys=True) != before:
        with io.open(DIMS_PATH, 'w', encoding='utf-8', newline='\n') as fp:
            json.dump(cache, fp, ensure_ascii=False, indent=0, sort_keys=True)
            fp.write('\n')
    print('검색 노출 후처리: %d개 페이지 수정' % changed)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
