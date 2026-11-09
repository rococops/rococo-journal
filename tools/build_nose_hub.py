"""코성형 허브(/nose/) 보강 섹션 생성: data/hub/nose.json → nose/index.html 에 삽입.

- 삽입 위치: 하위 메뉴 카드(subcat-section) 와 칼럼 목록(column-section) 사이. 마커 주석 구간을 매번 다시 쓰므로 재실행해도 안전.
- 기존 lp-* 클래스만 사용(css/style.css 는 건드리지 않음). 히어로는 다른 대표페이지와 같은 lp-hero 로 교체(h1 은 "코성형" 그대로).
- title·description·og:description 은 SEO 상수(아래)로 갱신(대표 승인, 2026-11-09). 나머지 SEO(canonical·구조화데이터)는 그대로.
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
import localize_landing_images as loc  # 이미지 주소를 저널 안(images/rococo/)으로
from build_landing import COUNTUP_JS

START, END = '<!-- 코성형 허브 보강 시작 -->', '<!-- 코성형 허브 보강 끝 -->'
HSTART, HEND = '<!-- 코성형 허브 히어로 시작 -->', '<!-- 코성형 허브 히어로 끝 -->'
JSTART, JEND = '<!-- 코성형 허브 스크립트 시작 -->', '<!-- 코성형 허브 스크립트 끝 -->'
# 문장이 끊겨 있던 description 을 완결 문장으로, title 은 '핵심키워드 | 설명 | 병원' 형태로 (2026-11-09 대표 승인)
SEO = {
    'title': '코성형 | 코재수술·늑연골·매부리코·복코 | 로코코성형외과 김상호 원장',
    'description': '로코코성형외과 김상호 원장의 코성형 안내. 코재수술, 늑연골·비중격연골 코성형, 매부리코, 복코, 비주성형, 비염수술까지 시술별 설명과 원장 칼럼, 수술 전후 사진을 확인하세요.',
}
ANCHOR = '<section class="section column-section">'
ROOT = '../'  # /nose/ 기준 사이트 루트
e = html.escape


def t(text):
    return e(tone(text))


def href(path):
    return f'{ROOT}{path.strip("/")}/'


def src_link(src):
    return f'<a class="lp-src" href="{href(src)}">— 「{e(col_title(src))}」 중에서 →</a>'


def img_url(u):
    """rococops.com/files 이미지는 이전된 사본(/images/rococo/...)이 있으면 그 주소로."""
    if u.startswith('https://rococops.com/files/'):
        new = loc.new_path(u[len('https://rococops.com'):])
        if os.path.exists(os.path.join(BASE, new.lstrip('/'))):
            return new
    return u


def render_hero(d):
    h, L = d['hero'], d['labels']
    stats = ''.join(f'<li><strong><span class="lp-num" data-to="{x["to"]}">{x["to"]}</span><small>{e(x["unit"])}</small></strong>'
                    f'<span>{e(x["label"])}</span></li>' for x in h['stats'])
    c = h['case']
    bg = f' style="--lp-hero-bg:url({ROOT}{h["bg_image"]})"'
    toc_ids = ['hub-subs', 'hub-story', 'hub-ba', 'hub-series', 'hub-faq', 'hub-risk', 'hub-guides']
    toc = ''.join(f'<a href="#{i}">{e(n)}</a>' for i, n in zip(toc_ids, L['toc']))
    stack = ' lp-hero-case--stack' if c.get('layout') == 'stack' else ''
    return f'''{HSTART}
<section class="lp-hero"{bg}>
  <div class="container lp-hero-inner">
    <div class="lp-hero-text">
      <div class="lp-hero-crumb"><a href="{ROOT}">홈</a><span>›</span><span>코성형</span></div>
      <span class="lp-hero-eyebrow">{e(h["eyebrow"])}</span>
      <h1 class="article-title lp-hero-title">코성형</h1>
      <p class="lp-hero-q">{e(L["lead_q"])}</p>
      <p class="lp-hero-summary">{t(h["summary"]["text"])}</p>
      <ul class="lp-hero-stats">{stats}</ul>
      <div class="lp-hero-cta">
        <a href="{ROOT}counsel/" class="lp-btn lp-btn-gold">상담 신청</a>
        <a href="#hub-ba" class="lp-btn lp-btn-line">전후사진 보기</a>
      </div>
      <p class="lp-hero-by">김상호 원장 · 로코코성형외과</p>
    </div>
    <a class="lp-hero-case{stack}" href="{href(c["src"])}">
      <img src="{e(img_url(c["image"]))}" alt="{e(c["alt"])}" loading="eager">
      <div class="lp-hero-case-cap"><span>{e(c["label"])}</span><p>{e(col_title(c["src"]))}</p><em>케이스 보기 →</em></div>
    </a>
  </div>
</section>
<nav class="lp-toc container" aria-label="코성형 목차">{toc}</nav>
{HEND}'''


def paras(lst):
    return ''.join(f'<p>{t(p["text"])}</p>' for p in lst)


def render(d):
    L = d['labels']
    ba = ''.join(
        f'<a class="lp-ba-item" href="{href(it["src"])}"><img src="{e(img_url(it["image"]))}" alt="{e(it["alt"])}" loading="lazy">'
        f'<p>{e(col_title(it["src"]))}</p><span>{e(it["label"])}</span></a>' for it in d['before_after']['items'])

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
<section class="section lp lp-dark" id="hub-story">
  <div class="container lp-narrow">
    <span class="lp-type">DOCTOR'S NOTE</span>
    <h2 class="lp-h2">{e(L["story_title"])}</h2>{story}
  </div>
</section>

<section class="section lp lp-flush" id="hub-ba">
  <div class="container">
    <span class="lp-type">BEFORE &amp; AFTER</span>
    <h2 class="lp-h2">{e(d["before_after"]["title"])}</h2>
    <div class="lp-ba">{ba}</div>
    <p class="lp-disclaimer">수술 결과는 개인에 따라 차이가 있을 수 있습니다. 사진을 누르면 해당 케이스 글로 이동합니다.</p>
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
    orig = s.replace('\r\n', '\n')
    out = orig

    # 히어로: 처음에는 기존 cat-hero 구간을 교체, 이후에는 마커 구간을 다시 씀
    if HSTART not in out:
        i = out.index('<section class="cat-hero">')
        j = out.index('</section>', i) + len('</section>')
        out = out[:i] + HSTART + HEND + out[j:]
    i, j = out.index(HSTART), out.index(HEND) + len(HEND)
    out = out[:i] + render_hero(d) + out[j:]

    # 하위 메뉴 카드 영역에 앵커 id
    if 'id="hub-subs"' not in out:
        out = out.replace('<section class="subcat-section">', '<section class="subcat-section" id="hub-subs">', 1)

    # 본문 보강 구간 (하위 메뉴 카드와 칼럼 목록 사이)
    new = render(d)
    if START in out:
        i, j = out.index(START), out.index(END) + len(END) + 1
        out = out[:i] + new + out[j:]
    else:
        assert out.count(ANCHOR) == 1, '삽입 기준점(column-section)을 찾지 못함'
        out = out.replace(ANCHOR, new + '\n' + ANCHOR, 1)

    # 카운트업 스크립트(</body> 앞)
    js = f'{JSTART}\n{COUNTUP_JS}\n{JEND}\n'
    if JSTART in out:
        i, j = out.index(JSTART), out.index(JEND) + len(JEND) + 1
        out = out[:i] + js + out[j:]
    else:
        out = out.replace('</body>', js + '</body>', 1)

    # SEO: title·description·공유 문구
    out = re.sub(r'<title>.*?</title>', lambda m: f'<title>{e(SEO["title"])}</title>', out, count=1, flags=re.S)
    out = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(SEO['description']), out, count=1)
    if '<meta property="og:description"' in out:
        out = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(SEO['description']), out, count=1)
    else:
        out = out.replace('<meta property="og:title"', f'<meta property="og:description" content="{e(SEO["description"])}">\n<meta property="og:title"', 1)

    if out != orig:
        if crlf:
            out = out.replace('\n', '\r\n')
        open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + out.encode('utf-8'))
        print('nose/index.html 갱신')
    else:
        print('변경 없음')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
