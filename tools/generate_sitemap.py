"""사이트 전체 URL을 모아 sitemap.xml 생성. 글별 udate를 lastmod로 반영."""
import os
import re

BASE_URL = 'https://journal.rococops.com'
DEFAULT_LASTMOD = '2026-06-15'

CATEGORY_DIRS = ['cheekbone', 'nose', 'nostril', 'forehead', 'eye', 'anti-aging']
# 성형 가이드(/guide/)는 api/publish.js 가 발행할 때 사이트맵에 직접 추가한다. 재생성해도 빠지지 않게 여기서도 포함
GUIDE_DIR = 'guide'

# 사이트맵에서 뺄 페이지: 케이스 상세(숫자 슬러그: 593, c209 …)와 후기 상세(…/reviews/숫자/).
# rococops.com 원글과 내용이 겹쳐 구글이 수집을 미루고 있어, 사이트맵은 저널만의 페이지(메뉴·가이드)에 집중한다.
# 페이지 자체는 그대로 있고, 목록 페이지의 링크로 수집될 수는 있다. 다시 넣고 싶으면 False.
EXCLUDE_DETAIL_PAGES = True
# 외국어 홈(/en/ …)과 외국어 대표페이지(/en/nose/hump/ …)
LANG_DIRS = ['en', 'ja', 'zh']
EXTRA_PATHS = [
    ('about/', '0.5', DEFAULT_LASTMOD),
    ('about/philosophy/', '0.5', DEFAULT_LASTMOD),
    ('about/location/', '0.5', DEFAULT_LASTMOD),
    ('about/faq/', '0.5', DEFAULT_LASTMOD),
    ('counsel/', '0.6', DEFAULT_LASTMOD),
    ('counsel/online/', '0.5', DEFAULT_LASTMOD),
    ('reserve/', '0.5', DEFAULT_LASTMOD),
    ('reviews/', '0.7', DEFAULT_LASTMOD),
    ('cases/', '0.7', DEFAULT_LASTMOD),
]

DATE_RE = re.compile(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})')


def read_lastmod(html_path):
    try:
        with open(html_path, encoding='utf-8', errors='ignore') as f:
            content = f.read(4000)
        m = DATE_RE.search(content)
        if m:
            date = m.group(1)
            # 0001-01-01 같은 유효하지 않은 날짜 제외
            if date >= '1900-01-01':
                return date
    except OSError:
        pass
    return DEFAULT_LASTMOD


def file_date(path):
    """파일 수정일 (YYYY-MM-DD)."""
    import datetime
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


def is_detail_page(path):
    """케이스 상세 / 후기 상세 여부. path 예: 'nose/hump/593/', 'anti-aging/chin/reviews/34/'"""
    parts = [p for p in path.split('/') if p]
    if len(parts) == 3:
        return bool(re.fullmatch(r'c?\d+', parts[2]))
    if len(parts) == 4 and parts[2] == 'reviews':
        return bool(re.fullmatch(r'\d+', parts[3]))
    return False


def collect_urls():
    urls = [('', '1.0', DEFAULT_LASTMOD)]

    # 성형 가이드: 목록(guide/) + 글(guide/슬러그/)
    for dirpath, _, files in os.walk(GUIDE_DIR):
        if 'index.html' not in files:
            continue
        path = dirpath.replace('\\', '/') + '/'
        urls.append((path, '0.8', read_lastmod(os.path.join(dirpath, 'index.html'))))

    for d in CATEGORY_DIRS:
        for dirpath, _, files in os.walk(d):
            if 'index.html' not in files:
                continue
            path = dirpath.replace('\\', '/') + '/'
            depth = path.count('/')
            if EXCLUDE_DETAIL_PAGES and is_detail_page(path):
                continue
            # 카테고리 목록(depth=2): 0.7 / 글 상세(depth=3): 0.8
            if depth == 2:
                priority = '0.7'
                lastmod = DEFAULT_LASTMOD
            else:
                priority = '0.8'
                lastmod = read_lastmod(os.path.join(dirpath, 'index.html'))
            urls.append((path, priority, lastmod))

    for lang in LANG_DIRS:
        for dirpath, _, files in os.walk(lang):
            if 'index.html' not in files:
                continue
            path = dirpath.replace('\\', '/') + '/'
            lastmod = DEFAULT_LASTMOD if path.count('/') == 1 else file_date(os.path.join(dirpath, 'index.html'))
            urls.append((path, '0.7', lastmod))

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
