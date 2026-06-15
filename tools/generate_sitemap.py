"""사이트 전체 URL을 모아 sitemap.xml 생성."""
import os

BASE_URL = 'https://journal.rococops.com'
LASTMOD = '2026-06-15'

CATEGORY_DIRS = ['cheekbone', 'nose', 'nostril', 'forehead', 'eye', 'anti-aging']
EXTRA_PATHS = ['about/', 'about/philosophy/', 'about/location/', 'counsel/']


def collect_urls():
    urls = [('', '1.0')]

    for d in CATEGORY_DIRS:
        for dirpath, _, files in os.walk(d):
            if 'index.html' not in files:
                continue
            path = dirpath.replace('\\', '/') + '/'
            depth = path.count('/')
            priority = '0.7' if depth == 2 else '0.6'
            urls.append((path, priority))

    for p in EXTRA_PATHS:
        urls.append((p, '0.5'))

    return urls


def main():
    urls = collect_urls()
    urls.sort(key=lambda x: x[0])

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for path, priority in urls:
        loc = f'{BASE_URL}/{path}'
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{LASTMOD}</lastmod>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'total urls: {len(urls)}')


if __name__ == '__main__':
    main()
