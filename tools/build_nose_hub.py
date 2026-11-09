"""코성형 허브(/nose/) 보강 섹션 생성: data/hub/nose.json → nose/index.html 에 삽입.

- 삽입 위치: 하위 메뉴 카드(subcat-section) 와 칼럼 목록(column-section) 사이. 마커 주석 구간을 매번 다시 쓰므로 재실행해도 안전.
- 기존 lp-* 클래스만 사용(css/style.css 는 건드리지 않음). title·h1·description 등 SEO 는 건드리지 않음.
- 새로 넣는 문장에는 말투 통일 규칙(tools/tone_normalize.py)을 적용한다. 대표페이지용 postprocess_landing.py 는 /nose/ 허브 페이지를
  대상으로 하지 않으므로(하위 메뉴 페이지만) 충돌하지 않는다.

사용: python tools/hub_src/nose.py          # 데이터 생성 (줄 범위 → data/hub/nose.json)
      python tools/verify_hub_quotes.py     # 원문 대조 (불일치 0건이어야 함)
      python tools/build_nose_hub.py        # 허브 페이지에 삽입
"""
import os, sys, re, json, html

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tone_normalize import tone
from landing_lib import title as col_title

START, END = '<!-- 코성형 허브 보강 시작 -->', '<!-- 코성형 허브 보강 끝 -->'
ANCHOR = '<section class="section column-section">'
ROOT = '../'  # /nose/ 기준 사이트 루트
e = html.escape


def t(text):
    return e(tone(text))


def href(path):
    return f'{ROOT}{path.strip("/")}/'


def src_link(src):
    return f'<a class="lp-src" href="{href(src)}">— 「{e(col_title(src))}」 중에서 →</a>'


def paras(lst):
    return ''.join(f'<p>{t(p["text"])}</p>' for p in lst)


def render(d):
    L = d['labels']
    toc_ids = ['hub-story', 'hub-series', 'hub-faq', 'hub-risk', 'hub-guides']
    toc = ''.join(f'<a href="#{i}">{e(n)}</a>' for i, n in zip(toc_ids, L['toc']))

    story = ''.join(
        f'''
    <h3 class="lp-h3">{e(col_title(b["src"]))}</h3>
    <blockquote class="lp-quote">{paras(b["paras"])}<cite>— 김상호</cite></blockquote>
    {src_link(b["src"])}''' for b in d['story'])

    series = ''.join(
        f'<a class="lp-log" href="{href(s)}"><span class="lp-log-tag">{e(L["series_tag"])}</span>'
        f'<p>{e(col_title(s))}</p><span class="lp-log-by">김상호 원장 기록 · 보기 →</span></a>' for s in d['series'])

    faq = ''.join(
        f'<details class="lp-faq"><summary>{e(col_title(q["src"]))}</summary><p>{t(q["text"])}</p>{src_link(q["src"])}</details>'
        for q in d['faq'])

    risk = d['risk']
    items = ''.join(f'<li>{t(i["text"])}</li>' for i in risk['items'])
    cards = ''.join(
        f'<a class="lp-log" href="{href(c["lead"]["src"])}"><span class="lp-log-tag">{e(L["risk_tag_" + c["tag"]])}</span>'
        f'<p>{e(col_title(c["lead"]["src"]))}</p><span class="lp-log-by">김상호 원장 기록 · 보기 →</span></a>'
        for c in risk['cards'])

    posts = {p['slug']: p for p in json.load(open(os.path.join(BASE, 'guide', 'posts.json'), encoding='utf-8'))}
    import guide_links
    guides = ''.join(guide_links.card(posts[s], ROOT) for s in d['guides'])

    return f'''{START}
<section class="section lp" id="hub-lead">
  <div class="container lp-narrow">
    <span class="lp-type">NOSE SURGERY</span>
    <h2 class="lp-h2">{e(L["lead_q"])}</h2>
  </div>
  <nav class="lp-toc container" aria-label="코성형 목차">{toc}</nav>
</section>

<section class="section lp lp-dark" id="hub-story">
  <div class="container lp-narrow">
    <span class="lp-type">DOCTOR'S NOTE</span>
    <h2 class="lp-h2">{e(L["story_title"])}</h2>{story}
  </div>
</section>

<section class="section lp lp-gray" id="hub-series">
  <div class="container">
    <span class="lp-type">SERIES</span>
    <h2 class="lp-h2">{e(L["series_title"])}</h2>
    <div class="lp-logs">{series}</div>
  </div>
</section>

<section class="section lp" id="hub-faq">
  <div class="container lp-narrow">
    <span class="lp-type">FAQ</span>
    <h2 class="lp-h2">{e(L["faq_title"])}</h2>
    {faq}
  </div>
</section>

<section class="section lp lp-gray" id="hub-risk">
  <div class="container lp-narrow">
    <span class="lp-type">RISK</span>
    <h2 class="lp-h2">{e(L["risk_title"])}</h2>
    <p class="lp-note">{t(risk["items_intro"]["text"])}</p>
    <ul class="lp-checks">{items}</ul>
    <div class="lp-logs">{cards}</div>
  </div>
</section>

<section class="section lp lp-guides-sec" id="hub-guides">
  <div class="container">
    <span class="lp-type">GUIDE</span>
    <h2 class="lp-h2">{e(L["guide_title"])}</h2>
    <div class="card-grid lp-guide-grid">{guides}</div>
    <p class="lp-guide-more"><a href="{ROOT}guide/">성형 가이드 전체 보기 →</a></p>
  </div>
</section>
{END}
'''


def main():
    d = json.load(open(os.path.join(BASE, 'data', 'hub', 'nose.json'), encoding='utf-8'))
    path = os.path.join(BASE, 'nose', 'index.html')
    raw = open(path, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    s = raw.decode('utf-8-sig')
    crlf = '\r\n' in s
    s = s.replace('\r\n', '\n')
    new = render(d)
    if START in s:
        i, j = s.index(START), s.index(END) + len(END) + 1
        out = s[:i] + new + s[j:]
    else:
        assert s.count(ANCHOR) == 1, '삽입 기준점(column-section)을 찾지 못함'
        out = s.replace(ANCHOR, new + '\n' + ANCHOR, 1)
    if crlf:
        out = out.replace('\n', '\r\n')
    if out != s.replace('\n', '\r\n' if crlf else '\n'):
        open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + out.encode('utf-8'))
        print('nose/index.html 갱신')
    else:
        print('변경 없음')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
