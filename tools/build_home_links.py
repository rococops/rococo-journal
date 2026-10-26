"""홈(index.html)에 '시술별 상세 안내(대표페이지 21개)'와 '최신 성형 가이드' 섹션을 넣는다. 다시 실행해도 안전.

- 위치: 히어로 바로 아래, '최근 케이스' 앞 (<!-- HOME-LINKS --> 표시로 감쌈)
- 대표페이지: data/landing/*.json 21개 / 가이드: guide/posts.json 최신 6편
- 새 가이드가 발행되면 다시 실행:  python tools/build_landing.py && python tools/build_home_links.py
사용: python tools/build_home_links.py
"""
import os, re, json, glob, html, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guide_links

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
e = html.escape
START, END = '<!-- HOME-LINKS -->', '<!-- /HOME-LINKS -->'
CATS = [('cheekbone', '광대성형'), ('nose', '코성형'), ('nostril', '콧구멍성형'),
        ('forehead', '이마성형'), ('eye', '눈성형'), ('anti-aging', '동안성형')]


def landing_chips():
    by_cat = {}
    for p in sorted(glob.glob(os.path.join(BASE, 'data', 'landing', '*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        page = d['page'].strip('/')
        name = re.sub(r'\s*[（(][^（()）]*[)）]$', '', d['seo']['h1'])
        by_cat.setdefault(page.split('/')[0], []).append((page, name))
    rows = ''
    for cat, label in CATS:
        items = by_cat.get(cat, [])
        if not items:
            continue
        chips = ''.join(f'<a href="{pg}/">{e(nm)}</a>' for pg, nm in items)
        rows += f'<div class="home-lp-row"><span class="home-lp-cat">{label}</span><div class="home-lp-chips">{chips}</div></div>'
    return rows


def build():
    cards = ''.join(guide_links.card(p, '') for p in guide_links.posts()[:6])
    return f'''{START}
<section class="section home-lp-section">
  <div class="container">
    <div class="section-head">
      <h2 class="section-label">내 고민에 맞는 시술 알아보기</h2>
    </div>
    <p class="home-lp-sub">수술 방법·회복 과정·전후사진·자주 묻는 질문을 시술별로 한 페이지에 정리했습니다.</p>
    <div class="home-lp">{landing_chips()}</div>
  </div>
</section>

<section class="section home-guide-section">
  <div class="container">
    <div class="section-head">
      <h2 class="section-label">최신 성형 가이드</h2>
      <a href="guide/" class="section-more">전체 보기 →</a>
    </div>
    <div class="card-grid">{cards}</div>
  </div>
</section>
{END}
'''


def main():
    path = os.path.join(BASE, 'index.html')
    raw = open(path, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    s = raw.decode('utf-8-sig')
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')
    block = build()
    if START in s:
        i = s.index(START)
        j = s.index(END, i) + len(END)
        s = s[:i] + block.rstrip('\n') + s[j:]
    else:
        anchor = '<!-- 최근 케이스 -->'
        assert anchor in s, '삽입 기준점 없음'
        s = s.replace(anchor, block + '\n' + anchor, 1)
    out = s.replace('\n', nl).encode('utf-8')
    open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + out)
    print('홈 링크 섹션 적용')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
