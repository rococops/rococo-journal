"""외국어 홈(/en/, /ja/, /zh/)의 시술 카테고리마다 그 언어 대표페이지 링크(칩)를 넣는다.

- 대표페이지 목록: data/landing/i18n/{lang}/*.json (이름은 seo.h1, 끝 괄호 설명은 뗀다)
- 위치: 각 카테고리 블록의 제목줄(.proc-section-head) 바로 아래 (카테고리 순서는 CAT_ORDER)
- <!-- LP-GUIDES --> 표시로 감싸서 넣으므로 다시 실행해도 안전(기존 칩을 지우고 새로 넣음)
- 한국어 링크 제거는 tools/strip_ko_links_lang_home.py (이 스크립트보다 먼저/나중 어느 쪽이든 무방)
사용: python tools/build_lang_home_guides.py
"""
import os, re, json, glob, html, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.stdout.reconfigure(encoding='utf-8')
NL = chr(13) + chr(10)  # 홈 파일은 CRLF

LABEL = {'en': 'Guides', 'ja': '詳しい解説', 'zh': '详细介绍'}
CSS = ('/* LP-GUIDES */\n'
       '.proc-guides { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin: 0.25rem 0 1.4rem; padding: 1rem 1.1rem; background: #faf6f0; border: 1px solid #ecdfcb; border-radius: 12px; }\n'
       '.proc-guides-label { flex: 0 0 100%; font-size: 12px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: #b8956a; }\n'
       '.proc-guides a { font-size: 15px; font-weight: 700; color: #111; text-decoration: none; border: 1.5px solid #b8956a; border-radius: 999px; padding: 10px 18px; background: #fff; line-height: 1.3; transition: background .15s, color .15s; }\n'
       '.proc-guides a::after { content: " \\2192"; color: #b8956a; }\n'
       '.proc-guides a:hover { background: #b8956a; color: #fff; }\n'
       '.proc-guides a:hover::after { color: #fff; }\n'
       '@media (max-width: 640px) { .proc-guides { padding: .85rem; gap: 8px; } .proc-guides a { font-size: 14px; padding: 9px 14px; } }\n'
       '/* /LP-GUIDES */\n')
# 홈 카테고리 블록 순서 (제목줄에 'View all' 링크가 없으므로 순서로 짝을 맞춘다)
CAT_ORDER = ['cheekbone', 'nose', 'nostril', 'eye', 'forehead', 'anti-aging']


def guides(lang):
    """카테고리('nose') → [(주소, 이름)]"""
    out = {}
    for p in sorted(glob.glob(os.path.join(BASE, 'data', 'landing', 'i18n', lang, '*.json'))):
        key = os.path.splitext(os.path.basename(p))[0]
        page = json.load(open(os.path.join(BASE, 'data', 'landing', f'{key}.json'), encoding='utf-8'))['page'].strip('/')
        name = re.sub(r'\s*[（(][^（()）]*[)）]$', '', json.load(open(p, encoding='utf-8'))['seo']['h1'])
        out.setdefault(page.split('/')[0], []).append((f'/{lang}/{page}/', name))
    return out


def apply(lang):
    path = os.path.join(BASE, lang, 'index.html')
    s = open(path, encoding='utf-8-sig').read()
    s = re.sub(r'\n?<!-- LP-GUIDES -->.*?<!-- /LP-GUIDES -->', '', s, flags=re.S)
    s = re.sub(r'/\* LP-GUIDES \*/.*?/\* /LP-GUIDES \*/\n', '', s, flags=re.S)
    g = guides(lang)
    n = 0
    order = iter(CAT_ORDER)

    def add(m):
        nonlocal n
        items = g.get(next(order), [])
        if not items:
            return m.group(0)
        n += len(items)
        links = ''.join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in items)
        return (f'{m.group(0)}\n<!-- LP-GUIDES --><div class="proc-guides"><span class="proc-guides-label">'
                f'{LABEL[lang]}</span>{links}</div><!-- /LP-GUIDES -->')

    # 카테고리 제목줄: <div class="proc-section-head"> ... </div> (안쪽 labels div 포함)
    s = re.sub(r'<div class="proc-section-head">.*?</div>\s*</div>', add, s, flags=re.S)
    s = s.replace('</style>', CSS + '</style>', 1)
    open(path, 'w', encoding='utf-8-sig', newline=NL).write(s)
    print(f'{lang}: 링크 {n}개')


if __name__ == '__main__':
    for l in LABEL:
        apply(l)
