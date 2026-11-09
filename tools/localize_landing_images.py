#!/usr/bin/env python3
"""대표페이지가 rococops.com/files 에서 불러오던 이미지를 저널 안(images/rococo/)으로 옮긴다.

- 받아 둔 옛 서버 파일(SRC_ROOT)을 WebP로 줄여 images/rococo/ 아래에 같은 하위 경로로 저장
- 대표페이지 HTML 안의 주소를 새 주소로 교체
  (img src는 /images/... 상대경로, og:image 같은 meta content는 절대주소)
사용: python tools/localize_landing_images.py [--dry-run] [--html-only]
"""
import glob
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = r'C:\Users\binia\Desktop\rococo홈페이지\public_html'  # 옛 서버에서 받아 둔 파일
OUT_DIR = os.path.join(ROOT, 'images', 'rococo')
SITE = 'https://journal.rococops.com'
CATS = ['cheekbone', 'nose', 'nostril', 'forehead', 'eye', 'anti-aging']
PAT = re.compile(r'https?://(?:www\.)?rococops\.com(/files/[^"\'\s)<>]+?\.(?:jpg|jpeg|png|gif|webp))', re.I)


def find_pages():
    pages = []
    for c in CATS:
        pages += glob.glob(os.path.join(ROOT, c, '*', 'index.html'))
        for lang in ('en', 'ja', 'zh'):
            pages += glob.glob(os.path.join(ROOT, lang, c, '*', 'index.html'))
    return sorted(pages)


def new_path(old):  # '/files/sitecontents/a/b.gif' -> '/images/rococo/sitecontents/a/b.webp'
    rest = old[len('/files/'):]
    return '/images/rococo/' + os.path.splitext(rest)[0] + '.webp'


def convert(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src)
    ext = os.path.splitext(src)[1].lower()
    if ext == '.gif' and getattr(im, 'n_frames', 1) > 1:
        w, h = im.size
        s = min(1.0, 800 / w)
        frames, durs = [], []
        for i in range(im.n_frames):
            im.seek(i)
            f = im.convert('RGBA')
            if s < 1:
                f = f.resize((max(1, int(w * s)), max(1, int(h * s))))
            frames.append(f)
            durs.append(max(20, im.info.get('duration', 100)))
        frames[0].save(dst, 'WEBP', save_all=True, append_images=frames[1:],
                       duration=durs, loop=0, quality=70, method=4)
        return
    im = im.convert('RGBA' if ext in ('.png', '.gif') else 'RGB')
    w, h = im.size
    if w > 1200:
        im = im.resize((1200, int(h * 1200 / w)))
    im.save(dst, 'WEBP', quality=80, method=4)


def main():
    dry = '--dry-run' in sys.argv
    html_only = '--html-only' in sys.argv
    pages = find_pages()
    olds = {}
    for p in pages:
        t = open(p, encoding='utf-8', newline='').read()
        for m in PAT.findall(t):
            olds.setdefault(m, set()).add(p)
    print('대표페이지 %d개, 이미지 %d개' % (len(pages), len(olds)))
    miss = []
    if not html_only:
        for i, old in enumerate(sorted(olds), 1):
            src = os.path.join(SRC_ROOT, old.lstrip('/').replace('/', os.sep))
            dst = os.path.join(ROOT, new_path(old).lstrip('/').replace('/', os.sep))
            if not os.path.exists(src):
                miss.append(old)
                continue
            if os.path.exists(dst):
                continue
            if not dry:
                convert(src, dst)
            if i % 50 == 0:
                print('  변환 %d/%d' % (i, len(olds)), flush=True)
    if miss:
        print('원본 없음(교체 안 함):', len(miss))
        for m in miss[:20]:
            print('  ', m)
    missset = set(miss)
    changed = []
    for p in pages:
        t = open(p, encoding='utf-8', newline='').read()

        def sub(m):
            old = m.group(1)
            if old in missset:
                return m.group(0)
            new = new_path(old)
            pre = t[max(0, m.start() - 12):m.start()]
            return (SITE + new) if 'content="' in pre else new

        t2 = PAT.sub(sub, t)
        if t2 != t:
            changed.append(os.path.relpath(p, ROOT))
            if not dry:
                open(p, 'w', encoding='utf-8', newline='').write(t2)
    print('HTML 수정 %d개%s' % (len(changed), ' (dry-run)' if dry else ''))
    with open(os.path.join(ROOT, 'tools', '_localize_changed.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(changed))


if __name__ == '__main__':
    main()
