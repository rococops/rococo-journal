"""로코코 저널 관리자 — 새 글 작성/발행 도구.
사용법: python tools/admin.py  →  브라우저에서 http://localhost:8282 접속
"""
import os, sys, re, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import date as date_cls

sys.path.insert(0, os.path.dirname(__file__))

from clean_content import build_article_blocks, clean_text, html_escape, extract_origin_url
from templates import (CTA_SECTION_HTML, DETAIL_PAGE, ORIGIN_LINK_CARD)
from build_pages import (SUBCATS, CAT_NAMES, ACTIVE_MAP, THUMB_BASE_URL,
                          thumb_pool, header, footer, truncate, og_url_for)

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PORT = 8282

# 서브카테고리 목록 (표시용)
SUBCAT_OPTIONS = [
    (cfg[1], cfg[2], cfg[3])  # (cat_path, sub_dir, sub_name)
    for cfg in SUBCATS if cfg[5] is not None
]


def next_slug():
    """전체 카테고리 폴더를 스캔해서 숫자 slug 최대값 + 1 반환."""
    max_num = 700
    for cfg in SUBCATS:
        d = os.path.join(BASE, cfg[1], cfg[2])
        if not os.path.exists(d):
            continue
        for name in os.listdir(d):
            if re.match(r'^\d+$', name):
                try:
                    max_num = max(max_num, int(name))
                except ValueError:
                    pass
    return str(max_num + 1)


def build_article(form):
    """폼 데이터로 상세페이지 HTML 생성 후 저장. 성공 시 (slug, url) 반환."""
    cat_path = form.get('cat_path', [''])[0].strip()
    sub_dir  = form.get('sub_dir',  [''])[0].strip()
    title    = form.get('title',    [''])[0].strip()
    summary  = form.get('summary',  [''])[0].strip()
    content_raw = form.get('content', [''])[0]
    date_str = form.get('date', [str(date_cls.today())])[0].strip()

    # 필수 항목 검증
    if not all([cat_path, sub_dir, title, content_raw.strip()]):
        return None, '필수 항목(카테고리, 제목, 본문)을 모두 입력해주세요.'

    # 서브카테고리 메타 찾기
    cfg = next((c for c in SUBCATS if c[1] == cat_path and c[2] == sub_dir), None)
    if not cfg:
        return None, '올바르지 않은 카테고리입니다.'
    _, _, _, sub_name, sub_name_en, keywords = cfg

    if not summary:
        summary = clean_text(content_raw[:300]) or title

    slug = next_slug()
    img_alt = f'{keywords or sub_name} 로코코성형외과'
    meta_title = f'{keywords or sub_name} — 로코코성형외과 김상호 원장'
    cat_name = CAT_NAMES[cat_path]
    active_key = ACTIVE_MAP[cat_path]

    root = '../../../'
    list_root = '../'
    og_url = og_url_for(cat_path, sub_dir, slug)

    # 본문 파싱
    content_html, images = build_article_blocks(content_raw, img_alt)

    # 이미지/썸네일
    pool = thumb_pool(cat_path, sub_dir)
    fallback_img = THUMB_BASE_URL + pool[0]
    hero_image = images[0] if images else (root + 'images/thumbnails/' + pool[0])
    og_image = images[0] if images else fallback_img

    # 원문 링크
    origin_url = extract_origin_url(content_raw)
    origin_link_card = ORIGIN_LINK_CARD.format(origin_url=origin_url) if origin_url else ''

    page = DETAIL_PAGE.format(
        title=html_escape(title),
        title_short=html_escape(truncate(title, 24)),
        title_json=title.replace('"', '\\"'),
        meta_title=html_escape(meta_title),
        description=html_escape(summary),
        description_json=summary.replace('"', '\\"'),
        og_image=og_image,
        og_url=og_url,
        canonical_url=og_url,
        img_alt=html_escape(img_alt),
        root=root,
        header=header(root, active_key),
        footer=footer(root),
        cat_path=cat_path,
        cat_name=cat_name,
        cat_name_json=cat_name.replace('"', '\\"'),
        sub_name=sub_name,
        sub_name_json=sub_name.replace('"', '\\"'),
        sub_name_en=sub_name_en,
        sub_dir=sub_dir,
        list_root=list_root,
        hero_image=hero_image,
        content=content_html,
        origin_link_card=origin_link_card,
        date=date_str,
        cta_section=CTA_SECTION_HTML.format(root=root, cat_name=sub_name),
    )

    out_dir = os.path.join(BASE, cat_path, sub_dir, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page)

    # 사이트맵 재생성
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        import generate_sitemap
        os.chdir(BASE)
        generate_sitemap.main()
    except Exception as e:
        print(f'sitemap 재생성 오류: {e}')

    return slug, og_url


# ── 관리자 HTML ──────────────────────────────────────────────────

def subcat_options_html(selected_cat='', selected_sub=''):
    opts = []
    for cat_path, sub_dir, sub_name in SUBCAT_OPTIONS:
        sel = 'selected' if (cat_path == selected_cat and sub_dir == selected_sub) else ''
        opts.append(f'<option value="{cat_path}|{sub_dir}" {sel}>{CAT_NAMES[cat_path]} &gt; {sub_name}</option>')
    return '\n'.join(opts)


ADMIN_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>로코코 저널 관리자</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Apple SD Gothic Neo',sans-serif;background:#f4f4f4;color:#222}}
  .top-bar{{background:#111;color:#fff;padding:1rem 2rem;display:flex;align-items:center;gap:1rem}}
  .top-bar h1{{font-size:1rem;font-weight:700;letter-spacing:.05em}}
  .top-bar .badge{{font-size:.75rem;background:#333;padding:.2rem .6rem;border-radius:4px}}
  .wrap{{max-width:860px;margin:2rem auto;padding:0 1.5rem 4rem}}
  .card{{background:#fff;border-radius:10px;padding:2rem;margin-bottom:1.5rem;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
  .card h2{{font-size:1rem;font-weight:700;margin-bottom:1.25rem;padding-bottom:.75rem;border-bottom:1px solid #eee}}
  .field{{margin-bottom:1.25rem}}
  label{{display:block;font-size:.82rem;font-weight:700;color:#555;margin-bottom:.35rem}}
  input[type=text],input[type=date],select,textarea{{
    width:100%;padding:.6rem .8rem;border:1px solid #ddd;border-radius:6px;
    font-size:.92rem;font-family:inherit;background:#fff;
  }}
  input:focus,select:focus,textarea:focus{{outline:none;border-color:#111}}
  textarea{{height:380px;font-family:monospace;font-size:.82rem;line-height:1.5;resize:vertical}}
  .row{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
  .hint{{font-size:.78rem;color:#888;margin-top:.3rem}}
  .btn{{display:inline-block;padding:.7rem 1.8rem;border:none;border-radius:6px;
    font-size:.95rem;font-weight:700;cursor:pointer;text-decoration:none}}
  .btn-black{{background:#111;color:#fff}}
  .btn-black:hover{{background:#333}}
  .btn-green{{background:#1a7f37;color:#fff}}
  .btn-green:hover{{background:#145c28}}
  .btn-gray{{background:#e0e0e0;color:#333}}
  .actions{{display:flex;gap:.75rem;align-items:center;margin-top:1rem}}
  .msg{{padding:1rem 1.25rem;border-radius:6px;margin-bottom:1.5rem;font-size:.92rem}}
  .msg.ok{{background:#d4edda;color:#155724;border:1px solid #c3e6cb}}
  .msg.err{{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb}}
  .url-box{{font-family:monospace;font-size:.85rem;background:#f0f0f0;padding:.5rem .8rem;
    border-radius:4px;word-break:break-all;margin-top:.5rem}}
</style>
</head>
<body>
<div class="top-bar">
  <h1>ROCOCO Journal — 관리자</h1>
  <span class="badge">로컬 전용</span>
</div>
<div class="wrap">

{msg_html}

<form method="POST" action="/publish">
<div class="card">
  <h2>새 글 작성</h2>

  <div class="field">
    <label>카테고리</label>
    <select name="subcat" required>
      <option value="">— 선택 —</option>
      {subcat_options}
    </select>
  </div>

  <div class="field">
    <label>제목</label>
    <input type="text" name="title" value="{title_val}" required placeholder="글 제목 입력">
  </div>

  <div class="row">
    <div class="field">
      <label>작성일</label>
      <input type="date" name="date" value="{date_val}" required>
    </div>
    <div class="field">
      <label>요약 (비워두면 본문 첫 문장 자동 추출)</label>
      <input type="text" name="summary" value="{summary_val}" placeholder="선택사항">
    </div>
  </div>

  <div class="field">
    <label>본문 HTML</label>
    <textarea name="content" required placeholder="기존 홈페이지 에디터에서 HTML 탭 클릭 → 전체 복사 → 여기에 붙여넣기">{content_val}</textarea>
    <p class="hint">기존 홈페이지 에디터 하단 <strong>HTML</strong> 탭 클릭 → 전체 선택(Ctrl+A) → 복사(Ctrl+C) → 여기에 붙여넣기</p>
  </div>

  <div class="actions">
    <button type="submit" class="btn btn-black">글 생성 →</button>
    <span style="font-size:.82rem;color:#888">생성 후 아래에서 GitHub에 발행할 수 있습니다</span>
  </div>
</div>
</form>

{push_section}

</div>
</body>
</html>"""

PUSH_SECTION_HTML = """
<div class="card">
  <h2>GitHub 발행</h2>
  <p style="font-size:.9rem;color:#555;margin-bottom:1rem">
    생성된 파일을 GitHub에 push하면 <strong>journal.rococops.com</strong>에 즉시 반영됩니다.<br>
    마지막 생성: <a href="{og_url}" target="_blank" style="color:#1a7f37">{og_url}</a>
  </p>
  <form method="POST" action="/push">
    <input type="hidden" name="slug" value="{slug}">
    <input type="hidden" name="title" value="{title}">
    <div class="actions">
      <button type="submit" class="btn btn-green">GitHub에 발행 (git push) →</button>
    </div>
  </form>
</div>
"""


class AdminHandler(BaseHTTPRequestHandler):
    last_slug = ''
    last_url = ''
    last_title = ''

    def log_message(self, fmt, *args):
        pass  # 터미널 로그 최소화

    def send_html(self, body, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def render(self, msg_html='', form_vals=None):
        fv = form_vals or {}
        push = ''
        if AdminHandler.last_slug:
            push = PUSH_SECTION_HTML.format(
                og_url=AdminHandler.last_url,
                slug=AdminHandler.last_slug,
                title=AdminHandler.last_title,
            )
        html_body = ADMIN_HTML.format(
            msg_html=msg_html,
            subcat_options=subcat_options_html(fv.get('cat_path',''), fv.get('sub_dir','')),
            title_val=fv.get('title',''),
            date_val=fv.get('date', str(date_cls.today())),
            summary_val=fv.get('summary',''),
            content_val=fv.get('content','').replace('<','&lt;').replace('>','&gt;'),
            push_section=push,
        )
        self.send_html(html_body)

    def do_GET(self):
        self.render()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        form = parse_qs(body, keep_blank_values=True)

        if self.path == '/push':
            slug = form.get('slug', [''])[0]
            title = form.get('title', ['새 글'])[0]
            try:
                os.chdir(BASE)
                subprocess.run(['git', 'add', '-A', '--', ':!*.sql'], check=True)
                subprocess.run(['git', 'commit', '-m', f'새 글 추가: {title}'], check=True)
                subprocess.run(['git', 'push', 'origin', 'main'], check=True)
                msg = '<div class="msg ok">✅ GitHub push 완료! journal.rococops.com에 1~2분 내 반영됩니다.</div>'
            except subprocess.CalledProcessError as e:
                msg = f'<div class="msg err">❌ push 실패: {e}</div>'
            self.render(msg)
            return

        # /publish
        subcat_raw = form.get('subcat', [''])[0]
        if '|' in subcat_raw:
            cat_path, sub_dir = subcat_raw.split('|', 1)
        else:
            cat_path = sub_dir = ''

        form['cat_path'] = [cat_path]
        form['sub_dir'] = [sub_dir]

        slug, result = build_article(form)
        if slug is None:
            msg = f'<div class="msg err">❌ {result}</div>'
            fv = {
                'cat_path': cat_path, 'sub_dir': sub_dir,
                'title': form.get('title', [''])[0],
                'date': form.get('date', [str(date_cls.today())])[0],
                'summary': form.get('summary', [''])[0],
                'content': form.get('content', [''])[0],
            }
            self.render(msg, fv)
        else:
            AdminHandler.last_slug = slug
            AdminHandler.last_url = result
            AdminHandler.last_title = form.get('title', ['새 글'])[0]
            msg = f'''<div class="msg ok">
              ✅ 글이 생성되었습니다! slug: <strong>{slug}</strong><br>
              <div class="url-box">{result}</div>
              <p style="margin-top:.5rem;font-size:.85rem">아래에서 GitHub에 발행하세요.</p>
            </div>'''
            self.render(msg)


if __name__ == '__main__':
    os.chdir(BASE)
    server = HTTPServer(('localhost', PORT), AdminHandler)
    print(f'\n로코코 저널 관리자 실행 중')
    print(f'브라우저에서 열기 → http://localhost:{PORT}\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n종료')
