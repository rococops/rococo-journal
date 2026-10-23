"""외국어 대표페이지 생성: 번역 데이터 + 한국어 대표페이지 데이터 → /{lang}/{cat}/{sub}/index.html

- 번역 파일: data/landing/i18n/{lang}/{cat}-{sub}.json  (문장만. 숫자·사진·출처 링크는 한국어 데이터에서 가져옴)
- 원장님 인용(원장 이야기)은 번역문 아래에 '한국어 원문'을 접어서 그대로 보여 준다(번역이 원문과 어긋날 위험 보완).
- 케이스 글은 번역하지 않는다. 한국어 페이지로 가는 링크는 하나도 두지 않는다(2026-10-23 결정):
  사진은 링크 없이 보여 주고, 출처 링크·케이스 노트·전체 케이스 버튼·한국어 언어 선택은 뺀다.
- 번역 파일의 문장 개수가 한국어 데이터와 다르면 멈춘다(구조 대조).

사용: python tools/build_landing_i18n.py                (번역 파일 전체)
      python tools/build_landing_i18n.py en nose-hump   (특정 언어·페이지)
"""
import sys, os, re, json, glob, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_landing import ICONS, COUNTUP_JS, _svg  # 수술 단계 아이콘·숫자 카운트업은 한국어 페이지와 공용

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SITE = 'https://journal.rococops.com'
LANGS = ['en', 'ja', 'zh']
e = html.escape

# 화면 고정 문구 (언어별)
UI = {
    'en': {
        'home': 'Home', 'story': "Dr. Kim's notes", 'ba': 'Before & after', 'logs': 'Case notes', 'comps': 'Related procedures',
        'faq': 'Frequently asked questions', 'cases': 'All cases', 'consult': 'Book a consultation', 'see_ba': 'See before & after',
        'by': 'Dr. Kim Sang-ho · Rococo Plastic Surgery', 'src': "From Dr. Kim's column (Korean) →",
        'orig': 'Read the original (Korean)', 'cite': '— Dr. Kim Sang-ho',
        'disclaimer': 'Results vary from person to person.',
        'log_by': "Dr. Kim's case note (Korean) · Read →", 'related': 'Related procedures', 'case': 'CASE',
        'case_more': 'See the case (Korean) →', 'cases_title': 'Every case, in Dr. Kim\'s own words',
        'cases_desc': 'The full case archive is written in Korean. Your browser can translate it automatically.',
        'cases_btn': 'See all {n} cases (Korean) →', 'more_cases': 'cases (Korean) →',
        'notice': "This page is an English translation of Dr. Kim Sang-ho's Korean columns. The original Korean text is shown under each quote.",
        'contact': 'Contact', 'kr': '(Korean)',
    },
    'ja': {
        'home': 'ホーム', 'story': 'キム院長の話', 'ba': '術前術後', 'logs': '症例記録', 'comps': '関連する施術',
        'faq': 'よくある質問', 'cases': 'すべての症例', 'consult': 'カウンセリング予約', 'see_ba': '術前術後を見る',
        'by': 'キム・サンホ院長 · ロココ整形外科', 'src': 'キム院長のコラムより（韓国語）→',
        'orig': '原文（韓国語）を見る', 'cite': '— キム・サンホ',
        'disclaimer': '結果には個人差があります。',
        'log_by': 'キム院長の症例記録（韓国語）· 見る →', 'related': '関連する施術', 'case': 'CASE',
        'case_more': '症例を見る（韓国語）→', 'cases_title': 'すべての症例を院長自身の言葉で',
        'cases_desc': '症例アーカイブは韓国語です。ブラウザの自動翻訳でお読みいただけます。',
        'cases_btn': '{n}件の症例を見る（韓国語）→', 'more_cases': '件の症例（韓国語）→',
        'notice': 'このページはキム・サンホ院長の韓国語コラムを日本語に翻訳したものです。各引用の下に韓国語の原文を掲載しています。',
        'contact': 'お問い合わせ', 'kr': '（韓国語）',
    },
    'zh': {
        'home': '首页', 'story': '金院长的话', 'ba': '术前术后', 'logs': '病例记录', 'comps': '相关项目',
        'faq': '常见问题', 'cases': '全部病例', 'consult': '预约咨询', 'see_ba': '查看术前术后',
        'by': '金相浩院长 · 洛可可整形外科', 'src': '摘自金院长专栏（韩语）→',
        'orig': '查看原文（韩语）', 'cite': '— 金相浩',
        'disclaimer': '效果因人而异。',
        'log_by': '金院长病例记录（韩语）· 查看 →', 'related': '相关项目', 'case': 'CASE',
        'case_more': '查看病例（韩语）→', 'cases_title': '每一个病例，都是院长亲笔记录',
        'cases_desc': '病例档案为韩语，可使用浏览器自动翻译阅读。',
        'cases_btn': '查看全部 {n} 个病例（韩语）→', 'more_cases': '个病例（韩语）→',
        'notice': '本页面由金相浩院长的韩语专栏翻译而成，每段引用下方附有韩语原文。',
        'contact': '联系我们', 'kr': '（韩语）',
    },
}
LANG_NAMES = [('ko', '🇰🇷 한국어'), ('en', '🇺🇸 English'), ('ja', '🇯🇵 日本語'), ('zh', '🇨🇳 中文')]


def i18n_path(lang, key):
    return os.path.join(BASE, 'data', 'landing', 'i18n', lang, f'{key}.json')


def available_langs(key):
    return [l for l in LANGS if os.path.exists(i18n_path(l, key))]


def check_shape(ko, t, key, lang):
    """번역 파일의 문장 개수가 한국어 데이터와 같은지 확인."""
    pairs = [
        ('hero.stats', len(ko['hero']['stats']), len(t['hero']['stats'])),
        ('hero.units', len(ko['hero']['stats']), len(t['hero']['units'])),
        ('features.items', len(ko['features']['items']), len(t['features']['items'])),
        ('story.blocks', len(ko['story']['blocks']), len(t['story']['blocks'])),
        ('method.steps', len(ko['method']['steps']), len(t['method']['steps'])),
        ('method.pros_cons', len(ko['method']['pros_cons']['paras']), len(t['method']['pros_cons'])),
        ('recovery.items', len(ko['recovery']['items']), len(t['recovery']['items'])),
        ('before_after', len(ko['before_after']['items']), len(t['before_after']['labels'])),
        ('logs', len(ko['logs']['items']), len(t['logs']['tags'])),
        ('faq', len(ko['faq']), len(t['faq'])),
        ('related', len(ko.get('related', [])), len(t.get('related', []))),
        ('companions', len((ko.get('companions') or {}).get('items', [])), len(t.get('companions', []))),
    ]
    for i, b in enumerate(ko['story']['blocks']):
        pairs.append((f'story[{i}].paras', len(b['paras']), len(t['story']['blocks'][i]['paras'])))
    for i, it in enumerate(ko['recovery']['items']):
        pairs.append((f'recovery[{i}].lines', len(it['lines']), len(t['recovery']['items'][i]['lines'])))
    bad = [f'{k}: 한국어 {a} / 번역 {b}' for k, a, b in pairs if a != b]
    if bad:
        raise SystemExit(f'[{lang}/{key}] 번역 파일 구조가 한국어 데이터와 다름:\n  ' + '\n  '.join(bad))


def kr(path):
    return f'/{path.strip("/")}/'


def render(lang, key):
    U = UI[lang]
    ko = json.load(open(os.path.join(BASE, 'data', 'landing', f'{key}.json'), encoding='utf-8'))
    t = json.load(open(i18n_path(lang, key), encoding='utf-8'))
    check_shape(ko, t, key, lang)
    page = ko['page'].strip('/')
    url = f'{SITE}/{lang}/{page}/'
    src_link = lambda s: ''  # 한국어 칼럼 출처 링크는 두지 않는다
    paras = lambda lst: ''.join(f'<p>{e(p)}</p>' for p in lst)
    h, th = ko['hero'], t['hero']

    # ── 히어로 ──
    stats = ''
    for s, label, unit in zip(h['stats'], th['stats'], th['units']):
        num = lambda n: f'<span class="lp-num" data-to="{n}">{n}</span>'
        val = (f'{num(s["from"])}–' if 'from' in s else '') + num(s['to'])
        stats += f'<li><strong>{val}<small>{e(unit)}</small></strong><span>{e(label)}</span></li>'
    case = h['case']
    stack = ' lp-hero-case--stack' if case.get('layout') == 'stack' else ''
    hero = f'''<section class="lp-hero" style="--lp-hero-bg:url(/{h["bg_image"]})">
  <div class="container lp-hero-inner">
    <div class="lp-hero-text">
      <div class="lp-hero-crumb"><a href="/{lang}/">{e(U["home"])}</a><span>›</span><span>{e(t["seo"]["h1"])}</span></div>
      <span class="lp-hero-eyebrow">{e(th["eyebrow"])}</span>
      <h1 class="article-title lp-hero-title">{e(t["seo"]["h1"])}</h1>
      <p class="lp-hero-q">{e(th["question"])}</p>
      <p class="lp-hero-summary">{e(th["summary"])}</p>
      <ul class="lp-hero-stats">{stats}</ul>
      <div class="lp-hero-cta">
        <a href="/{lang}/#consult" class="lp-btn lp-btn-gold">{e(U["consult"])}</a>
        <a href="#lp-ba" class="lp-btn lp-btn-line">{e(U["see_ba"])}</a>
      </div>
      <p class="lp-hero-by">{e(U["by"])}</p>
    </div>
    <div class="lp-hero-case{stack}">
      <img src="{e(case["image"])}" alt="{e(th.get("case_alt", t["before_after"]["alt"]))}" loading="eager">
      <div class="lp-hero-case-cap"><span>{e(U["case"])}</span><p>{e(th.get("case_caption", t["before_after"]["title"]))}</p></div>
    </div>
  </div>
</section>'''

    # ── 본문 ──
    f, tf = ko['features'], t['features']
    st = ''.join(
        f'''<h3 class="lp-h3">{e(tb["heading"])}</h3>
    <blockquote class="lp-quote">{paras(tb["paras"])}<cite>{e(U["cite"])}</cite></blockquote>
    <details class="lp-orig"><summary>{e(U["orig"])}</summary><div lang="ko">{paras(kb["paras"])}</div></details>
    {src_link(kb["src"])}'''
        for kb, tb in zip(ko['story']['blocks'], t['story']['blocks']))
    m, tm = ko['method'], t['method']
    icons = {**ICONS, **{k: _svg(v) for k, v in ko.get('icons', {}).items()}}
    steps = ''.join(f'<li><div class="lp-step-ico">{icons[s["icon"]]}</div><span>STEP {i + 1:02d}</span><p>{e(ts)}</p></li>'
                    for i, (s, ts) in enumerate(zip(m['steps'], tm['steps'])))
    rec, tr = ko['recovery'], t['recovery']
    timeline = ''.join(f'<li><span class="lp-tl-label">{e(ti["label"])}</span><div>{paras(ti["lines"])}</div></li>' for ti in tr['items'])
    rec_srcs = list(dict.fromkeys(it['src'] for it in rec['items']))
    ba, tba = ko['before_after'], t['before_after']
    ba_items = ''.join(f'<div class="lp-ba-item"><img src="{e(it["image"])}" alt="{e(tba["alt"])}" loading="lazy">'
                       f'<p>{e(lb)}</p></div>' for it, lb in zip(ba['items'], tba['labels']))
    faq = ''.join(f'<details class="lp-faq"><summary>{e(tq["q"])}</summary><p>{e(tq["a"])}</p>{src_link(kq["src"])}</details>'
                  for kq, tq in zip(ko['faq'], t['faq']))
    langs_avail = set(available_langs_all())

    def rel_href(path):
        k = path.strip('/').replace('/', '-')
        return f'/{lang}/{path.strip("/")}/' if (lang, k) in langs_avail else None
    # 번역된 대표페이지만 잇는다(한국어 페이지로 가는 항목은 뺀다)
    related = ''.join(f'<a href="{rel_href(r["href"])}">{e(n)}</a>' for r, n in zip(ko.get('related', []), t.get('related', []))
                      if rel_href(r["href"]))
    comps = ''
    if (ko.get('companions') or {}).get('items'):
        cards = ''.join(
            f'<article class="lp-comp"><div class="lp-comp-body"><h3 class="lp-comp-name">{e(tc["name"])}</h3>'
            f'<p class="lp-comp-lead">{e(tc["lead"])}</p></div></article>'
            for c, tc in zip(ko['companions']['items'], t['companions']))
        comps = f'''<section class="section lp" id="lp-comps"><div class="container">
    <span class="lp-type">RELATED PROCEDURES</span><h2 class="lp-h2">{e(U["comps"])}</h2><div class="lp-comps">{cards}</div></div></section>'''
    n_cases = len([x for x in glob.glob(os.path.join(BASE, page, '*', 'index.html'))
                   if os.path.basename(os.path.dirname(x)) != 'reviews'])

    body = f'''<p class="lp-i18n-notice container">{e(U["notice"])}</p>
<nav class="lp-toc container" aria-label="contents">
  <a href="#lp-features">{e(tf["toc"])}</a><a href="#lp-story">{e(U["story"])}</a><a href="#lp-method">{e(tm["title"])}</a>
  <a href="#lp-recovery">{e(tr["title"])}</a><a href="#lp-ba">{e(U["ba"])}</a>{f'<a href="#lp-comps">{e(U["comps"])}</a>' if comps else ''}<a href="#lp-faq">{e(U["faq"])}</a>
</nav>
<section class="section lp" id="lp-features"><div class="container lp-narrow">
    <span class="lp-type">{e(tf["type"])}</span><h2 class="lp-h2">{e(tf["title"])}</h2>
    <ul class="lp-checks">{"".join(f"<li>{e(x)}</li>" for x in tf["items"])}</ul>
    <p class="lp-note">{e(tf["note"])}</p>{src_link(f["src"])}</div></section>
<section class="section lp lp-dark" id="lp-story"><div class="container lp-narrow">
    <span class="lp-type">DOCTOR'S NOTE</span><h2 class="lp-h2">{e(t["story"].get("title", U["story"]))}</h2>{st}</div></section>
<section class="section lp" id="lp-method">
  <div class="container lp-narrow"><span class="lp-type">METHOD</span><h2 class="lp-h2">{e(tm["title"])}</h2></div>
  <div class="container"><ol class="lp-steps">{steps}</ol></div>
  <div class="container lp-narrow">{src_link(m["steps_src"])}
    <p class="lp-note">{e(tm["note"])}</p>{src_link(m["note"]["src"]) if m["note"]["src"] != m["steps_src"] else ""}
    <div class="lp-pc">{paras(tm["pros_cons"])}</div>{src_link(m["pros_cons"]["src"])}</div>
</section>
<section class="section lp lp-flush" id="lp-recovery"><div class="container lp-narrow">
    <span class="lp-type">RECOVERY</span><h2 class="lp-h2">{e(tr["title"])}</h2>
    <ol class="lp-timeline">{timeline}</ol>{"".join(src_link(s) for s in rec_srcs)}
    <p class="lp-note lp-note-gap">{e(tr["note"])}</p>{src_link(rec["note"]["src"])}</div></section>
<section class="section lp lp-flush" id="lp-ba"><div class="container">
    <span class="lp-type">BEFORE &amp; AFTER</span><h2 class="lp-h2">{e(tba["title"])}</h2>
    <div class="lp-ba">{ba_items}</div><p class="lp-disclaimer">{e(U["disclaimer"])}</p></div></section>
{comps}
<section class="section lp" id="lp-faq"><div class="container lp-narrow">
    <span class="lp-type">FAQ</span><h2 class="lp-h2">{e(U["faq"])}</h2>{faq}
    {f'<h3 class="lp-h3 lp-related-head">{e(U["related"])}</h3><div class="lp-related">{related}</div>' if related else ''}</div></section>'''

    # ── 머리말·구조화데이터 ──
    alts = [('ko', f'{SITE}/{page}/')] + [(l, f'{SITE}/{l}/{page}/') for l in available_langs(key)]
    hreflang = ''.join(f'<link rel="alternate" hreflang="{l}" href="{u}">\n' for l, u in alts)
    hreflang += f'<link rel="alternate" hreflang="x-default" href="{SITE}/{page}/">\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "name": t['seo']['title'], "description": t['seo']['description'], "url": url, "inLanguage": lang,
         "about": {"@type": "MedicalProcedure", "name": t['seo']['h1']},
         "author": {"@type": "Physician", "name": "Kim Sang-ho", "worksFor": {"@type": "MedicalBusiness", "name": "Rococo Plastic Surgery"}}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in t['faq']]}]}
    ko_raw = open(os.path.join(BASE, page, 'index.html'), encoding='utf-8-sig').read()
    analytics = ko_raw[ko_raw.index('<head>') + len('<head>'):ko_raw.index('<meta charset')]
    switch_links = ''.join(
        f'<a href="{(f"/{page}/" if l == "ko" else (f"/{l}/{page}/" if l in available_langs(key) else f"/{l}/"))}" '
        f'class="lang-option{" active" if l == lang else ""}">{n}</a>' for l, n in LANG_NAMES if l != 'ko')
    home = open(os.path.join(BASE, lang, 'index.html'), encoding='utf-8-sig').read()
    footer = re.search(r'<footer class="site-footer">.*?</footer>', home, re.S).group(0).replace('href="../', 'href="/')
    og_img = h['case']['image']
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>{analytics}<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(t["seo"]["title"])}</title>
<meta name="description" content="{e(t["seo"]["description"])}">
<meta property="og:title" content="{e(t["seo"]["h1"])} | Rococo Plastic Surgery">
<meta property="og:description" content="{e(t["seo"]["description"])}">
<meta property="og:image" content="{e(og_img)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<link rel="canonical" href="{url}">
{hreflang}<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
<header class="site-header lp-i18n-header" id="header">
  <div class="header-inner">
    <a href="/{lang}/" class="logo"><span class="logo-main">ROCOCO</span><span class="logo-sub">Plastic Surgery</span></a>
    <div class="lp-i18n-actions">
      <div class="lang-switcher"><button class="lang-btn" id="langBtn">🌐 GLOBAL &#9662;</button><div class="lang-dropdown" id="langDropdown">{switch_links}</div></div>
      <a href="/{lang}/#consult" class="lp-i18n-contact">{e(U["contact"])}</a>
    </div>
  </div>
</header>
{hero}
{body}
{footer}
<script>
(function(){{var btn=document.getElementById('langBtn');var dd=document.getElementById('langDropdown');if(!btn||!dd)return;
btn.addEventListener('click',function(e){{e.stopPropagation();dd.classList.toggle('open');}});document.addEventListener('click',function(){{dd.classList.remove('open');}});}})();
</script>
{COUNTUP_JS}
</body>
</html>
'''


def available_langs_all():
    out = []
    for l in LANGS:
        for p in glob.glob(os.path.join(BASE, 'data', 'landing', 'i18n', l, '*.json')):
            out.append((l, os.path.splitext(os.path.basename(p))[0]))
    return out


def main():
    args = sys.argv[1:]
    targets = available_langs_all()
    if args:
        targets = [(l, k) for l, k in targets if l == args[0] and (len(args) < 2 or k == args[1])]
    for lang, key in targets:
        ko = json.load(open(os.path.join(BASE, 'data', 'landing', f'{key}.json'), encoding='utf-8'))
        out_dir = os.path.join(BASE, lang, ko['page'].strip('/'))
        os.makedirs(out_dir, exist_ok=True)
        open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(render(lang, key))
        print(f'생성: /{lang}/{ko["page"].strip("/")}/')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
