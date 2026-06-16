"""사이트 전체 URL을 모아 sitemap.xml 생성. 글별 udate를 lastmod로 반영."""
import os
import re

BASE_URL = 'https://journal.rococops.com'
DEFAULT_LASTMOD = '2026-06-15'

CATEGORY_DIRS = ['cheekbone', 'nose', 'nostril', 'forehead', 'eye', 'anti-aging']
EXTRA_PATHS = [
    ('about/', '0.5', DEFAULT_LASTMOD),
    ('about/philosophy/', '0.5', DEFAULT_LASTMOD),
    ('about/location/', '0.5', DEFAULT_LASTMOD),
    ('counsel/', '0.5', DEFAULT_LASTMOD),
    ('cases/', '0.7', DEFAULT_LASTMOD),
]

DATE_RE = re.compile(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})')


def read_lastmod(html_path):
    try:
        with open(html_path, encoding='utf-8', errors='ignore') as f:
            content = f.read(4000)
        m = DATE_RE.search(content)
        if m:
            return m.group(1)
    except OSError:
        pass
    return DEFAULT_LASTMOD


def collect_urls():
    urls = [('', '1.0', DEFAULT_LASTMOD)]

    for d in CATEGORY_DIRS:
        for dirpath, _, files in os.walk(d):
            if 'index.html' not in files:
                continue
            path = dirpath.replace('\\', '/') + '/'
            depth = path.count('/')
            # 카테고리 목록(depth=2): 0.7 / 글 상세(depth=3): 0.8
            if depth == 2:
                priority = '0.7'
                lastmod = DEFAULT_LASTMOD
            else:
                priority = '0.8'
                lastmod = read_lastmod(os.path.join(dirpath, 'index.html'))
            urls.append((path, priority, lastmod))

    for p, pri, lm in EXTRA_PATHS:
        urls.append((p, pri, lm))

    return urls


def main():
    urls = collect_urls()
    urls.sort(key=lambda x: x[0])

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for path, priority, lastmod in urls:
        loc = f'{BASE_URL}/{path}'
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'sitemap: {len(urls)}개 URL 생성')


if __name__ == '__main__':
    main()
