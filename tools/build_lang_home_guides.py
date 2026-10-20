"""외국어 홈(/en/, /ja/, /zh/)의 시술 카테고리마다 그 언어 대표페이지 링크(칩)를 넣는다.

- 대표페이지 목록: data/landing/i18n/{lang}/*.json (이름은 seo.h1, 끝 괄호 설명은 뗀다)
- 위치: 각 카테고리 블록의 제목줄(.proc-section-head) 바로 아래
- <!-- LP-GUIDES --> 표시로 감싸서 넣으므로 다시 실행해도 안전(기존 칩을 지우고 새로 넣음)
사용: python tools/build_lang_home_guides.py
"""
import os, re, json, glob, html, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.stdout.reconfigure(encoding='utf-8')

LABEL = {'en': 'Guides', 'ja': '詳しい解説', 'zh': '详细介绍'}
CSS = ('/* LP-GUIDES */\n'
       '.proc-guides { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px; margin: -0.25rem 0 1rem; }\n'
       '.proc-guides-label { font-size: 12px; font-weight: 700; color: #888; margin-right: 2px; }\n'
       '.proc-guides a { font-size: 13px; color: #111; text-decoration: none; border: 1px solid #ddd; border-radius: 999px; padding: 5px 12px; background: #fff; }\n'
       '.proc-guides a:hover { border-color: #b8956a; color: #b8956a; }\n'
       '/* /LP-GUIDES */\n')


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

    def add(m):
        nonlocal n
        items = g.get(m.group(2), [])
        if not items:
            return m.group(0)
        n += len(items)
        links = ''.join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in items)
        return (f'{m.group(0)}\n<!-- LP-GUIDES --><div class="proc-guides"><span class="proc-guides-label">'
                f'{LABEL[lang]}</span>{links}</div><!-- /LP-GUIDES -->')

    # 카테고리 제목줄: ...<a href="https://journal.rococops.com/{cat}/" class="view-all-link" ...>...</a>\n    </div>
    s = re.sub(r'(<a href="https://journal\.rococops\.com/([a-z-]+)/" class="view-all-link"[^>]*>.*?</a>\s*</div>)', add, s)
    s = s.replace('</style>', CSS + '</style>', 1)
    open(path, 'w', encoding='utf-8-sig', newline='').write(s)
    print(f'{lang}: 링크 {n}개')


if __name__ == '__main__':
    for l in LABEL:
        apply(l)
