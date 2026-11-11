#!/usr/bin/env python3
"""llms.txt 만들기 — AI 검색(ChatGPT·Perplexity·Claude 등)이 인용할 페이지를 안내하는 목차.

사이트맵에 있는 한국어 대표페이지·안내 페이지와 성형 가이드(guide/posts.json)를
제목 + 한 줄 설명으로 나열한다. 설명은 각 페이지의 meta description 을 그대로 쓴다(새 문장을 만들지 않음).

사용: python tools/build_llms.py
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'https://journal.rococops.com'
CATS = [('cheekbone', '광대성형'), ('nose', '코성형'), ('nostril', '콧구멍성형'), ('eye', '눈성형'),
        ('forehead', '이마성형'), ('anti-aging', '동안성형')]
LANGS = [('en', 'English'), ('ja', '日本語'), ('zh', '中文')]

HEAD = """# 로코코 저널 (ROCOCO Journal)

> 로코코성형외과 김상호 원장(성형외과 전문의)이 직접 집필하는 성형외과 저널. 광대축소술, 코성형, 콧구멍성형, 눈성형, 이마성형, 동안성형의 시술별 대표 페이지와 성형 가이드, 실제 수술 케이스를 수록합니다.

- 사이트: https://journal.rococops.com (한국어, 일부 영어·일본어·중국어)
- 저자: 김상호 (Kim Sang-ho), 로코코성형외과 원장, 성형외과 전문의 — 서울 압구정
- AI 크롤러: 허용. 인용 시 "로코코 저널 (journal.rococops.com)"으로 출처 표기
- 개별 수술 케이스 원문은 병원 홈페이지(rococops.com)가 원본입니다
"""


def meta(path):
    f = os.path.join(ROOT, path.replace('/', os.sep), 'index.html') if path else os.path.join(ROOT, 'index.html')
    if not os.path.isfile(f):
        return None
    t = open(f, encoding='utf-8').read(20000)
    title = re.search(r'<title>(.*?)</title>', t, re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', t)
    name = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else (title.group(1).split('|')[0].strip() if title else path)
    return html.unescape(re.sub(r'\s+', ' ', name)), html.unescape(desc.group(1).strip()) if desc else ''


def line(path, name=None, desc=None):
    m = meta(path)
    if not m:
        return None
    name, desc = name or m[0], m[1] if desc is None else desc
    return '- [%s](%s/%s)%s' % (name, BASE_URL, path, ': ' + desc if desc else '')


def main():
    s = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    paths = re.findall(r'<loc>' + re.escape(BASE_URL) + r'/(.*?)</loc>', s)
    out = [HEAD]
    for cat, label in CATS:
        rows = [line(p) for p in paths
                if p.startswith(cat + '/') and not p.endswith('reviews/') and p.count('/') <= 2]
        rows = [r for r in rows if r]
        if rows:
            out.append('## %s\n\n%s\n' % (label, '\n'.join(rows)))
    posts = json.load(open(os.path.join(ROOT, 'guide', 'posts.json'), encoding='utf-8'))
    posts.sort(key=lambda p: p.get('date', ''), reverse=True)
    rows = ['- [%s](%s/guide/%s/): %s' % (p['title'], BASE_URL, p['slug'], p.get('summary', '')) for p in posts if p.get('slug')]
    out.append('## 성형 가이드 (김상호 원장 집필)\n\n%s\n' % '\n'.join(rows))
    rows = [r for r in (line(p) for p in paths if p.split('/')[0] in ('about', 'reviews', 'cases', 'counsel')) if r]
    out.append('## 병원·원장 안내\n\n%s\n' % '\n'.join(rows))
    rows = [r for r in (line(code + '/', name=label) for code, label in LANGS) if r]
    rows.append('- [RSS 피드](%s/feed.xml): 성형 가이드 새 글' % BASE_URL)
    rows.append('- [사이트맵](%s/sitemap.xml)' % BASE_URL)
    out.append('## Optional\n\n%s\n' % '\n'.join(rows))
    text = '\n'.join(out)
    path = os.path.join(ROOT, 'llms.txt')
    old = open(path, encoding='utf-8', newline='').read()
    if text != old:
        open(path, 'w', encoding='utf-8', newline='').write(text)
    print('llms.txt: %d줄, %.1fKB%s' % (text.count('\n'), len(text.encode('utf-8')) / 1024, '' if text != old else ' (변경 없음)'))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
