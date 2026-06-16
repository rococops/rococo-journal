import json, re

with open('data/multilang-cases.json', encoding='utf-8') as f:
    data = json.load(f)

def fmt_views(v):
    if v >= 1000:
        return f"{v//1000}K"
    return str(v)

LABELS = {
    'en': {
        'section_title': 'Procedures &amp; Case Reviews',
        'section_sub': 'Real cases from Dr. Kim Sang-ho — sorted by popularity',
        'view_all': 'View all →',
        'categories': {
            'cheekbone': ('광대축소술', 'Cheekbone Reduction', 'cheekbone/'),
            'nose':      ('코성형', 'Rhinoplasty', 'nose/'),
            'nostril':   ('콧구멍성형', 'Nostril Surgery', 'nostril/'),
            'eye':       ('눈성형', 'Eye Surgery', 'eye/'),
            'forehead':  ('이마성형', 'Forehead Surgery', 'forehead/'),
            'antiaging': ('동안성형', 'Anti-Aging', 'anti-aging/'),
        },
    },
    'ja': {
        'section_title': '施術 &amp; 症例レビュー',
        'section_sub': 'キム・サンホ院長の実際の症例 — 閲覧数順',
        'view_all': 'すべて見る →',
        'categories': {
            'cheekbone': ('광대축소술', '頬骨縮小術', 'cheekbone/'),
            'nose':      ('코성형', '鼻整形', 'nose/'),
            'nostril':   ('콧구멍성형', '小鼻整形', 'nostril/'),
            'eye':       ('눈성형', '目の整形', 'eye/'),
            'forehead':  ('이마성형', 'おでこ整形', 'forehead/'),
            'antiaging': ('동안성형', 'アンチエイジング', 'anti-aging/'),
        },
    },
    'zh': {
        'section_title': '手术项目 &amp; 案例回顾',
        'section_sub': '金相镐院长的真实案例 — 按浏览量排序',
        'view_all': '查看全部 →',
        'categories': {
            'cheekbone': ('광대축소술', '颧骨缩小术', 'cheekbone/'),
            'nose':      ('코성형', '鼻整形', 'nose/'),
            'nostril':   ('콧구멍성형', '鼻翼整形', 'nostril/'),
            'eye':       ('눈성형', '眼部整形', 'eye/'),
            'forehead':  ('이마성형', '额头整形', 'forehead/'),
            'antiaging': ('동안성형', '抗衰老整形', 'anti-aging/'),
        },
    },
}

BASE_URL = 'https://journal.rococops.com/'

def gen_cases_html(lang):
    lb = LABELS[lang]
    lines = []
    lines.append(f'<section class="section" id="procedures">')
    lines.append(f'  <p class="section-title">{lb["section_title"]}</p>')
    lines.append(f'  <p class="section-sub">{lb["section_sub"]}</p>')

    for group_key, (kr, local, cat_path) in lb['categories'].items():
        articles = data.get(group_key, [])
        if not articles:
            continue
        cat_url = BASE_URL + cat_path
        lines.append(f'')
        lines.append(f'  <div class="proc-section">')
        lines.append(f'    <div class="proc-section-head">')
        lines.append(f'      <div class="proc-section-labels">')
        lines.append(f'        <span class="kr">{kr}</span>')
        lines.append(f'        <h3>{local}</h3>')
        lines.append(f'      </div>')
        lines.append(f'      <a href="{cat_url}" class="view-all-link" target="_blank">{lb["view_all"]}</a>')
        lines.append(f'    </div>')
        lines.append(f'    <div class="case-scroll">')
        for art in articles:
            img = art.get('img', '')
            title = art.get('title', '')
            views = art.get('views', 0)
            url = art.get('url', '')
            full_url = BASE_URL + url
            views_html = f'<span class="case-views">&#128065; {fmt_views(views)}</span>' if views > 0 else ''
            if img:
                img_html = f'<img src="{img}" alt="" loading="lazy">'
            else:
                img_html = '<div class="case-no-img"></div>'
            lines.append(f'      <a href="{full_url}" class="case-card" target="_blank">')
            lines.append(f'        {img_html}')
            lines.append(f'        <div class="case-card-body">')
            if views_html:
                lines.append(f'          {views_html}')
            lines.append(f'          <p class="case-title">{title}</p>')
            lines.append(f'        </div>')
            lines.append(f'      </a>')
        lines.append(f'    </div>')
        lines.append(f'  </div>')

    lines.append(f'</section>')
    return '\n'.join(lines)

NEW_CSS = """
.proc-section { margin-bottom: 2.8rem; }
.proc-section-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 1rem; }
.proc-section-labels .kr { font-size: 11px; color: #b8956a; font-weight: 700; letter-spacing: 0.05em; display: block; margin-bottom: 2px; }
.proc-section-labels h3 { font-size: 1.15rem; font-weight: 700; color: #111; margin: 0; }
.view-all-link { font-size: 13px; color: #b8956a; font-weight: 700; text-decoration: none; white-space: nowrap; }
.view-all-link:hover { text-decoration: underline; }
.case-scroll { display: flex; gap: 14px; overflow-x: auto; padding-bottom: 8px; -webkit-overflow-scrolling: touch; scrollbar-width: thin; }
.case-scroll::-webkit-scrollbar { height: 4px; }
.case-scroll::-webkit-scrollbar-thumb { background: #ddd; border-radius: 2px; }
.case-card { flex: 0 0 160px; background: #fff; border: 1px solid #ebebeb; border-radius: 8px; overflow: hidden; text-decoration: none; display: flex; flex-direction: column; transition: box-shadow 0.15s; }
.case-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.10); }
.case-card img { width: 100%; height: 120px; object-fit: cover; display: block; }
.case-no-img { width: 100%; height: 120px; background: #f5f5f5; }
.case-card-body { padding: 0.6rem 0.75rem 0.75rem; flex: 1; display: flex; flex-direction: column; gap: 4px; }
.case-views { font-size: 11px; color: #aaa; }
.case-title { font-size: 12px; color: #333; line-height: 1.5; margin: 0; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
"""

for lang in ['en', 'ja', 'zh']:
    fpath = f'{lang}/index.html'
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    new_section = gen_cases_html(lang)

    # 기존 procedures 섹션 교체 (주석 포함 or 미포함)
    replaced = False
    for pattern in [
        r'<!-- 한구먹 -->\s*<section class="section" id="procedures">.*?</section>',
        r'<!-- 시술 -->\s*<section class="section" id="procedures">.*?</section>',
        r'<section class="section" id="procedures">.*?</section>',
    ]:
        if re.search(pattern, html, re.DOTALL):
            html = re.sub(pattern, new_section, html, flags=re.DOTALL)
            replaced = True
            print(f'{lang}: procedures 섹션 교체 완료')
            break

    if not replaced:
        print(f'{lang}: WARNING - procedures 섹션을 찾지 못함!')

    if '.case-scroll' not in html:
        html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
        print(f'{lang}: CSS 추가 완료')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

print('완료')
