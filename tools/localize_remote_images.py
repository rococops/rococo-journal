#!/usr/bin/env python3
"""저널이 직접 만든 페이지(사이트맵에 있는 페이지)가 rococops.com 에서 불러오던 사진을
저널 안(images/rococo/)으로 가져와 WebP 로 바꾸고, HTML 안 주소를 교체한다. 여러 번 실행해도 같은 결과.

- 케이스 원문(병원 홈페이지로 canonical, 사이트맵 제외)은 건드리지 않는다.
- 원본은 받아 둔 옛 서버 파일(localize_landing_images.SRC_ROOT)이 있으면 그것을, 없으면 내려받아 쓴다.
- 주소 규칙은 localize_landing_images.py 와 같다: /files/a/b.jpg -> /images/rococo/a/b.webp
  (그 밖의 경로는 /images/rococo/site/... , v2 서버는 /images/rococo/v2/...)
- img src 는 /images/... 상대경로, meta·JSON-LD 등 나머지는 절대주소.
- 가져오지 못한 사진은 주소를 그대로 둔다.

사용: python tools/localize_remote_images.py [--dry-run] [--guides]
      (--guides: 성형 가이드 페이지만 — GitHub Actions 용)
"""
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import localize_landing_images as loc  # noqa: E402

ROOT = loc.ROOT
SITE = loc.SITE
PAT = re.compile(r'https?://((?:www\.|v2\.)?)rococops\.com(/[^"\'\s)<>]+?\.(?:jpg|jpeg|png|gif|webp))', re.I)


def new_path(host, path):
    path = urllib.parse.unquote(path)
    stem = os.path.splitext(path)[0]
    if host.lower() == 'v2.':
        return '/images/rococo/v2' + stem + '.webp'
    if path.startswith('/files/'):
        return '/images/rococo/' + stem[len('/files/'):] + '.webp'
    return '/images/rococo/site' + stem + '.webp'


def fetch(host, path, dst):
    """옛 서버 사본이 있으면 그것을, 없으면 내려받아 WebP 로 저장. 성공하면 True."""
    src = os.path.join(loc.SRC_ROOT, urllib.parse.unquote(path).lstrip('/').replace('/', os.sep))
    if host.lower() != 'v2.' and os.path.isfile(src):
        loc.convert(src, dst)
        return True
    url = 'https://%srococops.com%s' % (host, path)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=40).read()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(path)[1])
    try:
        tmp.write(data)
        tmp.close()
        loc.convert(tmp.name, dst)
    finally:
        os.unlink(tmp.name)
    return True


def pages(guides_only):
    s = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    out = []
    for p in re.findall(r'<loc>' + re.escape(SITE) + r'/(.*?)</loc>', s):
        if guides_only and not p.startswith('guide/'):
            continue
        f = os.path.join(ROOT, p.replace('/', os.sep), 'index.html') if p else os.path.join(ROOT, 'index.html')
        if os.path.isfile(f):
            out.append(f)
    return out


def main():
    dry = '--dry-run' in sys.argv
    files = pages('--guides' in sys.argv)
    found = {}
    for f in files:
        for host, path in PAT.findall(open(f, encoding='utf-8', newline='').read()):
            found[(host, path)] = new_path(host, path)
    print('페이지 %d개, 외부 사진 %d개' % (len(files), len(found)))
    failed = set()
    made = 0
    for i, ((host, path), new) in enumerate(sorted(found.items()), 1):
        dst = os.path.join(ROOT, new.lstrip('/').replace('/', os.sep))
        if os.path.exists(dst) or dry:
            continue
        try:
            fetch(host, path, dst)
            made += 1
        except Exception as e:
            failed.add((host, path))
            print('  가져오기 실패(주소 그대로 둠): %s%s — %s' % (host, path, e))
        if i % 100 == 0:
            print('  %d/%d' % (i, len(found)), flush=True)
    changed = 0
    for f in files:
        t = open(f, encoding='utf-8', newline='').read()

        def sub(m):
            key = (m.group(1), m.group(2))
            if key in failed:
                return m.group(0)
            new = found[key]
            return new if t[max(0, m.start() - 5):m.start()] == 'src="' else SITE + new

        t2 = PAT.sub(sub, t)
        if t2 != t:
            changed += 1
            if not dry:
                open(f, 'w', encoding='utf-8', newline='').write(t2)
    print('새로 변환 %d개, 실패 %d개, HTML 수정 %d개%s' % (made, len(failed), changed, ' (dry-run)' if dry else ''))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
