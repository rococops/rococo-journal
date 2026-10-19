"""시술별 대표페이지 생성: data/landing/{cat}-{sub}.json 이 있는 하위 메뉴 목록 페이지에
대표페이지 섹션(히어로·원장 이야기·수술 방법·회복·전후사진·대표 사례·FAQ)을 넣는다.

- 데이터 파일이 없는 페이지는 건드리지 않음 (지금처럼 목록 페이지 그대로).
- 기존 목록(카드 그리드)·후기 배너·하단 CTA 는 그대로 두고, 아래 구간만 교체/삽입:
    · 아티클 히어로 → 대표페이지 히어로 (H1 은 class="article-title" 유지: build_reviews 등이 읽음)
    · 후기 배너 앞에 대표페이지 본문
    · 케이스 목록은 cases_visible 개만 보이고 '더보기' 버튼
- 마커 사이 구간을 매번 다시 쓰므로 재실행해도 안전(idempotent).
- <title>·description·구조화데이터·H1 문구는 seo.apply 가 true 일 때만 바꿈.

사용: python tools/build_landing.py            (data/landing/*.json 전체)
      python tools/build_landing.py nose-hump  (특정 파일만)
"""
import sys, os, re, json, glob, html

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LANDING_DIR = os.path.join(BASE, 'data', 'landing')

HERO_START, HERO_END = '<!-- 대표페이지 히어로 시작 -->', '<!-- 대표페이지 히어로 끝 -->'
BODY_START, BODY_END = '<!-- 대표페이지 본문 시작 -->', '<!-- 대표페이지 본문 끝 -->'
MORE_START, MORE_END = '<!-- 대표페이지 더보기 시작 -->', '<!-- 대표페이지 더보기 끝 -->'
JS_START, JS_END = '<!-- 대표페이지 스크립트 시작 -->', '<!-- 대표페이지 스크립트 끝 -->'
LD_START, LD_END = '<!-- 대표페이지 구조화데이터 시작 -->', '<!-- 대표페이지 구조화데이터 끝 -->'

e = html.escape

# ── 수술 단계 일러스트 (단순 선화 SVG, 120x120) ──
_LINE = 'fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
_NASION = 'M30 6 C36 16 38 26 40 34'
_STRAIGHT = 'L66 74'
_GOODTIP = 'C70 80 71 86 66 89 C62 91 58 90 55 90 C56 96 58 101 61 105 C58 108 58 111 61 114'
_HUMP = 'C48 40 59 44 60 52 C61 60 62 65 63.1 69.6'
_SKIN = 'fill="#f1cfb8" stroke="none"'
_FACE = f'<path d="{_NASION} {_STRAIGHT} {_GOODTIP} L0 114 L0 6 Z" {_SKIN}/>'
_PROFILE = f'<path d="{_NASION} {_STRAIGHT} {_GOODTIP}" {_LINE}/>'


def _svg(inner):
    return f'<svg viewBox="0 0 120 120" aria-hidden="true">{inner}</svg>'


ICONS = {
    # 수면마취: 달 + z
    'sleep': _svg('<path d="M70 28 A30 30 0 1 0 92 78 A24 24 0 1 1 70 28 Z" fill="#efe4d3" stroke="#b8956a" stroke-width="2.2"/>'
                  '<text x="78" y="44" font-size="15" font-weight="700" fill="#b8956a" font-family="sans-serif">z</text>'
                  '<text x="90" y="30" font-size="11" font-weight="700" fill="#b8956a" font-family="sans-serif">z</text>'),
    # 휜코교정: 정면, 휜 중심축(점선) → 곧은 축
    'deviation': _svg('<path d="M50 14 C49 40 46 62 40 78 C33 82 33 92 42 93 C46 93 49 91 52 92 L68 92 C71 91 74 93 78 93 C87 92 87 82 80 78 C74 62 71 40 70 14 Z" fill="#f1cfb8"/>'
                      f'<path d="M50 14 C49 40 46 62 40 78 C33 82 33 92 42 93 C46 93 49 91 52 92 M70 14 C71 40 74 62 80 78 C87 82 87 92 78 93 C74 93 71 91 68 92" {_LINE}/>'
                      '<path d="M60 12 C64 40 66 60 64 92" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="4 4"/>'
                      '<path d="M60 12 L60 92" fill="none" stroke="#b8956a" stroke-width="2.6"/>'
                      '<path d="M70 56 L62 56 M65 52 L61 56 L65 60" fill="none" stroke="#c46a5a" stroke-width="2" stroke-linecap="round"/>'),
    # 코끝 높이기: 처진 코끝(점선) → 올라간 코끝 + 화살표
    'tip': _svg(_FACE + '<path d="M66 74 C68 82 68 90 62 92 C58 93 56 92 55 91" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="4 4"/>'
                + _PROFILE +
                '<path d="M80 92 L80 78 M75 83 L80 78 L85 83" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'),
    # 매부리 다듬기: 볼록한 매부리(붉은 면) 제거 후 곧은 콧대
    'hump': _svg(_FACE + f'<path d="M40 34 {_HUMP} L40 34 Z" fill="#e58f7c" fill-opacity=".55" stroke="#c46a5a" stroke-width="1.8" stroke-dasharray="3 3"/>'
                 + _PROFILE),
    # 꺼진 부위 채우기: 콧대-코끝 사이 연골 이식(금색 면)
    'fill': _svg(_FACE + '<path d="M50 50 C57 53 64 62 66 73 C58 70 52 62 50 50 Z" fill="#c9a26f" stroke="#a9834f" stroke-width="1.4"/>'
                 + _PROFILE +
                 '<path d="M82 52 L82 62 M77 57 L87 57" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round"/>'),
    # 귀연골+피부 채취: 귀 옆모습, 채취 부위(금색)
    'ear': _svg('<path d="M60 18 C38 18 30 40 36 62 C40 76 46 84 52 96 C56 104 68 104 74 94 C78 88 76 82 82 76 C94 62 90 18 60 18 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/>'
                '<path d="M58 36 C47 37 45 50 51 60 C55 67 58 72 56 82" fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round"/>'
                '<ellipse cx="66" cy="62" rx="8" ry="12" fill="#c9a26f" stroke="#a9834f" stroke-width="1.6"/>'),
    # 콧구멍 가리기(3세대 방식): 아래에서 본 코, 콧구멍 윗부분을 이식 조직(금색)이 덮음
    'graft': _svg('<path d="M25 72 C25 52 40 40 60 40 C80 40 95 52 95 72 C95 87 80 94 60 94 C40 94 25 87 25 72 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
                  '<path d="M37 78 C39 64 52 62 56 74 C52 80 42 82 37 78 Z" fill="#6b4a3a" fill-opacity=".75"/>'
                  '<path d="M83 78 C81 64 68 62 64 74 C68 80 78 82 83 78 Z" fill="#6b4a3a" fill-opacity=".75"/>'
                  '<path d="M37 78 C39 64 52 62 56 74 C51 68 43 69 37 78 Z" fill="#c9a26f" stroke="#a9834f" stroke-width="1.2"/>'
                  '<path d="M83 78 C81 64 68 62 64 74 C69 68 77 69 83 78 Z" fill="#c9a26f" stroke="#a9834f" stroke-width="1.2"/>'
                  '<path d="M60 14 L60 32 M53 25 L60 32 L67 25" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'),
    # 수술 시간
    'clock': _svg('<circle cx="60" cy="62" r="32" fill="#fff" stroke="#b8956a" stroke-width="2.4"/>'
                  '<path d="M60 36 L60 40 M60 84 L60 88 M34 62 L38 62 M82 62 L86 62" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round"/>'
                  '<path d="M60 62 L60 46 M60 62 L72 70" fill="none" stroke="#4a4a4a" stroke-width="2.6" stroke-linecap="round"/>'
                  '<circle cx="60" cy="62" r="3" fill="#4a4a4a"/>'),
    # 코끝 반창고
    'tape': _svg('<g transform="rotate(-20 60 62)"><rect x="18" y="48" width="84" height="28" rx="14" fill="#f3d9bf" stroke="#b8956a" stroke-width="2.2"/>'
                 '<rect x="46" y="50" width="28" height="24" fill="#fff6ea" stroke="#b8956a" stroke-width="1.4"/>'
                 '<path d="M28 58 L28 66 M36 58 L36 66 M84 58 L84 66 M92 58 L92 66" stroke="#b8956a" stroke-width="1.6" stroke-linecap="round"/></g>'),
}

# 히어로 숫자 카운트업: 보일 때 한 번, 동작 줄이기 설정이면 생략
COUNTUP_JS = '''<script>
(function(){var els=document.querySelectorAll('.lp-num');if(!els.length||!('IntersectionObserver' in window))return;
if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function run(el){var to=+el.dataset.to,dur=to<10?700:1400,t0=null;
 function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/dur,1),v=1-Math.pow(1-p,3);el.textContent=Math.round(to*v);if(p<1)requestAnimationFrame(step);}
 el.textContent='0';requestAnimationFrame(step);setTimeout(function(){el.textContent=to;},dur+400);}
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){run(en.target);io.unobserve(en.target);}});},{threshold:.6});
els.forEach(function(el){io.observe(el);});})();
</script>'''


def page_title(src):
    """칼럼 제목: 해당 글의 H1(원장님 원래 글 제목). <title> 은 페이지마다 접미어가 달라 쓰지 않음."""
    raw = open(os.path.join(BASE, src, 'index.html'), encoding='utf-8-sig').read()
    t = re.search(r'<h1 class="article-title">(.*?)</h1>', raw, re.S).group(1)
    return html.unescape(t).strip()


class Renderer:
    def __init__(self, data, root):
        self.d = data
        self.root = root  # 목록 페이지 기준 사이트 루트 상대경로 (예: '../../')

    def href(self, path):
        """사이트 루트 기준 경로 → 페이지 상대경로 (기존 페이지들과 같은 방식)."""
        return f'{self.root}{path.strip("/")}/'

    def src_link(self, src):
        return f'<a class="lp-src" href="{self.href(src)}">— 「{e(page_title(src))}」 중에서 →</a>'

    @staticmethod
    def paras(lst):
        return ''.join(f'<p>{e(p)}</p>' for p in lst)

    @staticmethod
    def num(n):
        return f'<span class="lp-num" data-to="{n}">{n}</span>'

    def hero(self, h1, crumbs):
        h = self.d['hero']
        stats = []
        for s in h['stats']:
            value = (f'{self.num(s["from"])}–' if 'from' in s else '') + self.num(s['to'])
            stats.append(f'<li><strong>{value}<small>{e(s["unit"])}</small></strong><span>{e(s["label"])}</span></li>')
        case = h['case']
        bg = f' style="--lp-hero-bg:url({self.root}{h["bg_image"]})"' if h.get('bg_image') else ''
        return f'''{HERO_START}
<section class="lp-hero"{bg}>
  <div class="container lp-hero-inner">
    <div class="lp-hero-text">
      <div class="lp-hero-crumb">{crumbs}</div>
      <span class="lp-hero-eyebrow">{e(h["eyebrow"])}</span>
      <h1 class="article-title lp-hero-title">{e(h1)}</h1>
      <p class="lp-hero-q">{e(h["question"])}</p>
      <p class="lp-hero-summary">{e(h["summary"]["text"])}</p>
      <ul class="lp-hero-stats">{"".join(stats)}</ul>
      <div class="lp-hero-cta">
        <a href="{self.root}counsel/" class="lp-btn lp-btn-gold">상담 신청</a>
        <a href="#lp-ba" class="lp-btn lp-btn-line">전후사진 보기</a>
      </div>
      <p class="lp-hero-by">김상호 원장 · 로코코성형외과</p>
    </div>
    <a class="lp-hero-case{' lp-hero-case--stack' if case.get('layout') == 'stack' else ''}" href="{self.href(case["src"])}">
      <img src="{e(case["image"])}" alt="{e(case["alt"])}" loading="eager">
      <div class="lp-hero-case-cap"><span>{e(case["label"])}</span><p>{e(page_title(case["src"]))}</p><em>케이스 보기 →</em></div>
    </a>
  </div>
</section>
{HERO_END}'''

    def body(self):
        d = self.d
        f, st, m, rec, ba, logs = (d['features'], d['story'], d['method'], d['recovery'],
                                   d['before_after'], d['logs'])
        story = ''.join(
            f'''
    <h3 class="lp-h3">{e(b["heading"])}</h3>
    <blockquote class="lp-quote">{self.paras(b["paras"])}<cite>— 김상호</cite></blockquote>
    {self.src_link(b["src"])}''' for b in st['blocks'])
        # 아이콘: 공용 ICONS 이름, 또는 이 페이지 데이터의 "icons": {"이름": "<svg 내부 요소>"} (페이지마다 고유 아이콘이 필요할 때)
        icons = {**ICONS, **{k: _svg(v) for k, v in d.get('icons', {}).items()}}
        steps = ''.join(
            f'<li><div class="lp-step-ico">{icons[s["icon"]]}</div><span>STEP {i + 1:02d}</span><p>{e(s["text"])}</p></li>'
            for i, s in enumerate(m['steps']))
        # 회복 출처: 같은 칼럼이 이어지면 한 번만 표시
        rec_srcs = list(dict.fromkeys(it['src'] for it in rec['items']))
        timeline = ''.join(f'<li><span class="lp-tl-label">{e(it["label"])}</span><div>{self.paras(it["lines"])}</div></li>'
                           for it in rec['items'])
        ba_items = ''.join(
            f'<a class="lp-ba-item" href="{self.href(it["src"])}"><img src="{e(it["image"])}" alt="{e(ba["alt"])}" loading="lazy">'
            f'<p>{e(page_title(it["src"]))}</p><span>{e(it.get("label") or it["caption"])}</span></a>'
            for it in ba['items'])
        log_items = ''.join(
            f'<a class="lp-log" href="{self.href(it["src"])}"><span class="lp-log-tag">{e(it["tag"])}</span>'
            f'<p>{e(page_title(it["src"]))}</p><span class="lp-log-by">김상호 원장 기록 · 보기 →</span></a>'
            for it in logs['items'])
        faq = ''.join(f'<details class="lp-faq"><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p>{self.src_link(q["src"])}</details>'
                      for q in d['faq'])
        related = ''.join(f'<a href="{self.href(r["href"])}">{e(r["name"])}</a>' for r in d.get('related', []))
        comps = self.companions()
        return f'''{BODY_START}
<nav class="lp-toc container" aria-label="목차">
  <a href="#lp-features">{e(f["toc"])}</a><a href="#lp-story">원장 이야기</a><a href="#lp-method">{e(m["title"])}</a>
  <a href="#lp-recovery">{e(rec["title"])}</a><a href="#lp-ba">전후사진</a><a href="#lp-logs">대표 사례</a>{'<a href="#lp-comps">함께 보는 시술</a>' if comps else ''}<a href="#lp-faq">자주 묻는 질문</a><a href="#lp-cases">전체 케이스</a>
</nav>

<section class="section lp" id="lp-features">
  <div class="container lp-narrow">
    <span class="lp-type">{e(f["type"])}</span>
    <h2 class="lp-h2">{e(f["title"])}</h2>
    <ul class="lp-checks">{"".join(f"<li>{e(t)}</li>" for t in f["items"])}</ul>
    <p class="lp-note">{e(f["note"])}</p>
    {self.src_link(f["src"])}
  </div>
</section>

<section class="section lp lp-dark" id="lp-story">
  <div class="container lp-narrow">
    <span class="lp-type">DOCTOR'S NOTE</span>
    <h2 class="lp-h2">{e(st["title"])}</h2>{story}
  </div>
</section>

<section class="section lp" id="lp-method">
  <div class="container lp-narrow">
    <span class="lp-type">METHOD</span>
    <h2 class="lp-h2">{e(m["title"])}</h2>
  </div>
  <div class="container">
    <ol class="lp-steps">{steps}</ol>
  </div>
  <div class="container lp-narrow">
    {self.src_link(m["steps_src"])}
    <p class="lp-note">{e(m["note"]["text"])}</p>
    {self.src_link(m["note"]["src"]) if m["note"]["src"] != m["steps_src"] else ''}
    <div class="lp-pc">{self.paras(m["pros_cons"]["paras"])}</div>
    {self.src_link(m["pros_cons"]["src"])}
  </div>
</section>

<section class="section lp lp-flush" id="lp-recovery">
  <div class="container lp-narrow">
    <span class="lp-type">RECOVERY</span>
    <h2 class="lp-h2">{e(rec["title"])}</h2>
    <ol class="lp-timeline">{timeline}</ol>
    {"".join(self.src_link(s) for s in rec_srcs)}
    <p class="lp-note lp-note-gap">{e(rec["note"]["text"])}</p>
    {self.src_link(rec["note"]["src"])}
  </div>
</section>

<section class="section lp lp-flush" id="lp-ba">
  <div class="container">
    <span class="lp-type">BEFORE &amp; AFTER</span>
    <h2 class="lp-h2">{e(ba["title"])}</h2>
    <div class="lp-ba">{ba_items}</div>
    <p class="lp-disclaimer">수술 결과는 개인에 따라 차이가 있을 수 있습니다. 사진을 누르면 해당 케이스 글로 이동합니다.</p>
  </div>
</section>

<section class="section lp lp-gray" id="lp-logs">
  <div class="container">
    <span class="lp-type">SURGERY NOTES</span>
    <h2 class="lp-h2">{e(logs["title"])}</h2>
    <div class="lp-logs">{log_items}</div>
  </div>
</section>
{comps}
<section class="section lp" id="lp-faq">
  <div class="container lp-narrow">
    <span class="lp-type">FAQ</span>
    <h2 class="lp-h2">자주 묻는 질문</h2>
    {faq}
    {f'<h3 class="lp-h3 lp-related-head">관련 수술</h3><div class="lp-related">{related}</div>' if related else ''}
  </div>
</section>
<div id="lp-cases"></div>
{BODY_END}'''

    def companions(self):
        """'함께 알아두면 좋은 시술' 섹션 (선택). 작은 하위 메뉴를 큰 대표페이지에 소개 카드로 흡수할 때 사용.
        데이터: "companions": {"title": ..., "items": [{"name", "href"(하위 메뉴 경로),
                 "lead": {"text", "src"}(원장님 원문), "image": {"src", "url", "caption"}(선택)}]}"""
        c = self.d.get('companions')
        if not c or not c.get('items'):
            return ''
        cards = []
        for it in c['items']:
            n = len([x for x in glob.glob(os.path.join(BASE, it['href'], '*', 'index.html'))
                     if os.path.basename(os.path.dirname(x)) != 'reviews'])
            img = it.get('image')
            img_html = (f'<a class="lp-comp-img" href="{self.href(img["src"])}"><img src="{e(img["url"])}" '
                        f'alt="{e(it["name"])} 수술 전후 사진" loading="lazy"></a>') if img else ''
            cards.append(
                f'<article class="lp-comp">{img_html}<div class="lp-comp-body">'
                f'<h3 class="lp-comp-name"><a href="{self.href(it["href"])}">{e(it["name"])}</a></h3>'
                f'<p class="lp-comp-lead">{e(it["lead"]["text"])}</p>{self.src_link(it["lead"]["src"])}'
                f'<a class="lp-comp-more" href="{self.href(it["href"])}">{e(it["name"])} 케이스 {n}개 보기 →</a>'
                f'</div></article>')
        return f'''
<section class="section lp" id="lp-comps">
  <div class="container">
    <span class="lp-type">RELATED PROCEDURES</span>
    <h2 class="lp-h2">{e(c.get("title", "함께 알아두면 좋은 시술"))}</h2>
    <div class="lp-comps">{"".join(cards)}</div>
  </div>
</section>
'''

    def more_button(self, hidden):
        return (f'{MORE_START}\n    <button type="button" class="lp-more" id="lpMore">케이스 더보기 ({hidden}개) ↓</button>'
                '\n    <script>document.getElementById("lpMore").onclick=function(){'
                'document.getElementById("case-grid").classList.remove("lp-collapsed");this.remove();};</script>\n    '
                + MORE_END)

    def json_ld(self, url_path):
        """seo.apply=true 일 때 추가하는 MedicalWebPage + FAQPage 구조화데이터."""
        s = self.d['seo']
        url = f'https://journal.rococops.com/{url_path}/'
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "MedicalWebPage", "name": s['title'], "description": s['description'], "url": url,
             "inLanguage": "ko", "about": {"@type": "MedicalProcedure", "name": s['procedure_name']},
             "author": {"@type": "Physician", "name": "김상호", "worksFor": {"@type": "MedicalBusiness", "name": "로코코성형외과"}}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}}
                for q in self.d['faq']]}]}
        return (f'{LD_START}\n<script type="application/ld+json">\n'
                + json.dumps(ld, ensure_ascii=False, indent=2) + f'\n</script>\n{LD_END}')


def _replace_between(text, start, end, new):
    """start~end 마커 구간을 new 로 교체. 구간이 없으면 None."""
    i = text.find(start)
    if i < 0:
        return None
    j = text.index(end, i) + len(end)
    return text[:i] + new + text[j:]


def _upsert(text, start, end, new, anchor, before=True):
    """마커 구간이 있으면 교체, 없으면 anchor 앞(또는 뒤)에 삽입."""
    out = _replace_between(text, start, end, new)
    if out is not None:
        return out
    assert anchor in text, f'삽입 기준점 없음: {anchor}'
    return text.replace(anchor, (new + '\n' + anchor) if before else (anchor + '\n' + new), 1)


def apply_landing(page_dir, data):
    """page_dir/index.html (하위 메뉴 목록 페이지)에 대표페이지 섹션을 적용."""
    path = os.path.join(page_dir, 'index.html')
    raw = open(path, encoding='utf-8-sig').read()
    bom = open(path, 'rb').read(3) == b'\xef\xbb\xbf'
    out = raw
    root = '../' * data['page'].strip('/').count('/') + '../'
    r = Renderer(data, root)
    seo = data.get('seo', {})

    # ── 히어로: 기존 아티클 히어로(또는 이전에 넣은 대표페이지 히어로) 교체 ──
    if HERO_START in out:
        old = out[out.index(HERO_START):out.index(HERO_END)]
    else:
        s_i = out.index('<!-- 아티클 히어로 -->')
        old = out[s_i:out.index('</section>', s_i)]
    cur_h1 = html.unescape(re.search(r'<h1 class="article-title[^"]*">(.*?)</h1>', old, re.S).group(1).strip())
    crumb_m = re.search(r'<div class="(?:article-breadcrumb|lp-hero-crumb)">(.*?)</div>', old, re.S)
    crumbs = re.sub(r'\s*\n\s*', '', crumb_m.group(1).strip())
    h1 = seo['h1'] if seo.get('apply') else cur_h1
    new_hero = r.hero(h1, crumbs)
    if HERO_START in out:
        out = _replace_between(out, HERO_START, HERO_END, new_hero)
    else:
        s_i = out.index('<!-- 아티클 히어로 -->') + len('<!-- 아티클 히어로 -->')
        s_j = out.index('</section>', s_i) + len('</section>')
        out = out[:s_i] + '\n' + new_hero + out[s_j:]

    # ── 본문: 후기 배너 앞 (배너가 없으면 글 목록 앞) ──
    anchor = '<!-- 수술후기 진입 배너 -->' if '<!-- 수술후기 진입 배너 -->' in out else '<!-- 글 목록 -->'
    out = _upsert(out, BODY_START, BODY_END, r.body(), anchor)

    # 후기 배너 문구: '{하위메뉴}을 받은' → '{review_banner_subject}을 받은'
    subj = data.get('review_banner_subject')
    if subj:
        out = re.sub(r'(<h3 class="cta-title">)[^<]*?을 받은', rf'\g<1>{subj}을 받은', out, count=1)

    # ── 케이스 목록: cases_visible 개만 보이고 더보기 ──
    visible = data.get('cases_visible')
    if visible:
        if 'lp-collapsed' not in out:
            out = out.replace('<div class="card-grid" id="case-grid">',
                              '<div class="card-grid lp-collapsed" id="case-grid">', 1)
        n_cards = len(re.findall(r'class="card"', out))
        more = r.more_button(n_cards - visible)
        if MORE_START in out:
            out = _replace_between(out, MORE_START, MORE_END, more)
        else:
            grid_close = out.index('</a>\n    </div>', out.rindex('class="card"')) + len('</a>\n    </div>')
            out = out[:grid_close] + '\n    ' + more + out[grid_close:]

    # ── 카운트업 스크립트 ──
    out = _upsert(out, JS_START, JS_END, f'{JS_START}\n{COUNTUP_JS}\n{JS_END}', '</body>')

    # ── SEO (승인 후에만) ──
    if seo.get('apply'):
        out = re.sub(r'<title>.*?</title>', f'<title>{e(seo["title"])}</title>', out, count=1, flags=re.S)
        out = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(seo['description']), out, count=1)
        out = _upsert(out, LD_START, LD_END, r.json_ld(data['page'].strip('/')), '</head>')
        # 공유(카카오톡 등) 미리보기 문구도 새 제목·설명에 맞춤
        short_title = seo['title'].split(' | ')[0]
        out = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(short_title + ' | 로코코 저널'), out, count=1)
        out = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(seo['description']), out, count=1)

    if out != raw:
        with open(path, 'w', encoding='utf-8-sig' if bom else 'utf-8') as fp:
            fp.write(out)
    return out != raw


def landing_data_for(cat_path, sub_dir):
    """data/landing/{cat}-{sub}.json 이 있으면 로드, 없으면 None."""
    p = os.path.join(LANDING_DIR, f'{cat_path}-{sub_dir}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def main():
    names = sys.argv[1:]
    paths = ([os.path.join(LANDING_DIR, f'{n}.json') for n in names] if names
             else sorted(glob.glob(os.path.join(LANDING_DIR, '*.json'))))
    for p in paths:
        data = json.load(open(p, encoding='utf-8'))
        changed = apply_landing(os.path.join(BASE, data['page']), data)
        print(f'{"적용" if changed else "변화 없음"}: {data["page"]}/index.html  ({os.path.basename(p)})')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
