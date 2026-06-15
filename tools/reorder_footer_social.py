"""footer-social 블록을 footer-title('바로가기') 바로 아래로 이동 (기존 4개 링크보다 먼저 노출)."""
import os
import re

ROOT_DIRS = ['cheekbone', 'nose', 'nostril', 'forehead', 'eye', 'anti-aging']
EXTRA_FILES = [
    'about/index.html',
    'about/philosophy/index.html',
    'about/location/index.html',
    'counsel/index.html',
]

SOCIAL_PATTERN = re.compile(
    r'(        <a href="(?:\.\./)*about/">About 로코코</a>\n)'
    r'(        <div class="footer-social">.*?</div>\n)',
    re.DOTALL,
)

TITLE_PATTERN = re.compile(r'(<p class="footer-title">바로가기</p>\n)')


def process_file(path):
    content = open(path, encoding='utf-8').read()

    m = SOCIAL_PATTERN.search(content)
    if not m:
        return False

    social_block = m.group(2)
    content = content[:m.start()] + m.group(1) + content[m.end():]

    content = TITLE_PATTERN.sub(lambda tm: tm.group(1) + social_block, content, count=1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    changed = 0
    total = 0
    for d in ROOT_DIRS:
        for dirpath, _, files in os.walk(d):
            for fn in files:
                if fn == 'index.html':
                    total += 1
                    if process_file(os.path.join(dirpath, fn)):
                        changed += 1

    for f in EXTRA_FILES:
        total += 1
        if process_file(f):
            changed += 1

    print(f'total={total} changed={changed}')


if __name__ == '__main__':
    main()
