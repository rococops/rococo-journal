"""가이드 글 ↔ 대표페이지 연결 도우미 (대표페이지 '관련 가이드'와 홈 섹션이 씀).

- 연결표는 tools/guide.mjs 의 LANDING_RULES 하나만 보고 node 로 받아 온다.
- 글 목록은 guide/posts.json (발행된 글). 새 글이 발행되면 대표페이지·홈을 다시 빌드해야 반영된다:
    python tools/build_landing.py && python tools/build_home_links.py
"""
import os, re, json, subprocess, html

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
e = html.escape


def rules():
    out = subprocess.run(['node', os.path.join(BASE, 'tools', 'guide_landing_map.mjs')],
                         capture_output=True, check=True, encoding='utf-8').stdout
    return [(re.compile(r['pattern']), r['path'], r['label']) for r in json.loads(out)]


_RULES = None


def landing_for(keyword):
    """키워드 → (대표페이지 경로, 이름) 또는 None"""
    global _RULES
    if _RULES is None:
        _RULES = rules()
    for rx, path, label in _RULES:
        if rx.search(keyword or ''):
            return path, label
    return None


def posts():
    p = json.load(open(os.path.join(BASE, 'guide', 'posts.json'), encoding='utf-8'))
    return sorted(p, key=lambda x: (x.get('date') or '', x['slug']), reverse=True)


def posts_for(landing_path):
    return [p for p in posts() if (landing_for(p.get('keyword')) or (None,))[0] == landing_path.strip('/')]


def cover(p, root):
    """카드 이미지: 글 대표 이미지, 없으면 표지 그림"""
    if p.get('image'):
        return p['image']
    t = f"{p.get('keyword', '')} {p.get('tag', '')} {p.get('title', '')}"
    for rx, name in [(r'퀵광대', 'quick-cheekbone'), (r'광대', 'cheekbone'), (r'비공|콧구멍|콧날개', 'alar'),
                     (r'늑연골', 'rib-cartilage'), (r'재수술|구축|보형물', 'revision')]:
        if re.search(rx, t):
            return f'{root}images/guide/covers/{name}.png'
    return f'{root}images/guide/covers/nose.png'


def card(p, root, cls='card'):
    """가이드 글 카드 (가이드 목록·홈과 같은 .card 모양)"""
    return (f'<a href="{root}guide/{e(p["slug"])}/" class="{cls}">'
            f'<div class="card-img"><img src="{e(cover(p, root))}" alt="{e(p["title"])}" loading="lazy">'
            f'<span class="card-tag">{e(p.get("tag") or "성형 가이드")}</span></div>'
            f'<div class="card-body"><p class="card-title">{e(p["title"])}</p>'
            f'<p class="card-desc">{e(str(p.get("summary") or "")[:90])}</p></div></a>')
