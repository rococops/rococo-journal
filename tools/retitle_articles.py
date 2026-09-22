# 기존 글 상세 페이지의 <title>/og:title 을 seo_title 규칙으로 일괄 교체.
# 본문/H1/description 은 건드리지 않음. 예전 형식(" — 로코코성형외과 김상호 원장")으로 끝나는
# 제목만 대상이라 여러 번 실행해도 결과가 같음(멱등).
#
#   python tools/retitle_articles.py          # 미리보기(파일 수정 없음)
#   python tools/retitle_articles.py --apply  # 실제 적용
import io, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_title import seo_title

sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CATS = ['cheekbone', 'nose', 'nostril', 'forehead', 'eye', 'anti-aging']
OLD_SUFFIX = ' — 로코코성형외과 김상호 원장'
APPLY = '--apply' in sys.argv

changed = skipped = 0
samples = []
for cat in CATS:
    for dp, _, fn in os.walk(os.path.join(BASE, cat)):
        parts = os.path.relpath(dp, BASE).replace(os.sep, '/').split('/')
        if 'index.html' not in fn or 'reviews' in parts or len(parts) != 3:
            continue
        path = os.path.join(dp, 'index.html')
        raw = io.open(path, encoding='utf-8').read()
        m_h1 = re.search(r'<h1 class="article-title">(.*?)</h1>', raw, re.S)
        m_t = re.search(r'<title>(.*?)</title>', raw, re.S)
        if not m_h1 or not m_t:
            skipped += 1
            continue
        old_title = html.unescape(m_t.group(1))
        if not old_title.endswith(OLD_SUFFIX):
            skipped += 1          # 이미 새 형식이거나 예외 페이지
            continue
        keywords = old_title[:-len(OLD_SUFFIX)].strip()
        h1 = html.unescape(re.sub(r'<[^>]+>', '', m_h1.group(1))).strip()
        new_title = seo_title(h1, keywords)
        esc = html.escape(new_title, quote=True)

        new_raw = raw.replace(m_t.group(0), f'<title>{html.escape(new_title, quote=False)}</title>', 1)
        new_raw = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                         lambda m: m.group(1) + esc + m.group(2), new_raw, count=1)
        new_raw = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")',
                         lambda m: m.group(1) + esc + m.group(2), new_raw, count=1)
        if new_raw != raw:
            changed += 1
            if len(samples) < 400:
                samples.append(f'{"/".join(parts)}\n   전: {old_title}\n   후: {new_title}')
            if APPLY:
                io.open(path, 'w', encoding='utf-8', newline='').write(new_raw)

print(('적용' if APPLY else '미리보기') + f': 변경 대상 {changed}개, 건너뜀 {skipped}개')
out = os.environ.get('RETITLE_REPORT')
if out:
    io.open(out, 'w', encoding='utf-8').write('\n'.join(samples))
