"""기존 생성된 HTML 파일들의 상담·예약 메뉴/CTA/footer 링크를 새 템플릿 패턴으로 일괄 업데이트.

- nav: '상담·예약' has-sub + 하위메뉴 -> 단순 링크
- CTA: '온라인 상담' 카드 href를 외부 rococops.com -> 내부 {root}counsel/?from={cat_name}
- footer: '온라인 상담' 링크를 외부 rococops.com -> 내부 {root}counsel/
"""
import os
import re

ROOT_DIRS = ['cheekbone', 'nose', 'nostril', 'forehead', 'eye', 'anti-aging']
EXTRA_FILES = [
    'about/index.html',
    'about/philosophy/index.html',
    'about/location/index.html',
    'counsel/index.html',
]

NAV_PATTERN = re.compile(
    r'<li class="has-sub(?: active)?"><a href="((?:\.\./)*counsel/)">상담·예약</a>\s*'
    r'<ul class="sub-menu">.*?</ul>\s*</li>',
    re.DOTALL,
)

CTA_PATTERN = re.compile(
    r'<a href="https://rococops\.com/htm/counsel_normal\.php" class="cta-card" target="_blank">'
)

FOOTER_PATTERN = re.compile(
    r'<a href="https://rococops\.com/htm/counsel_normal\.php" target="_blank">온라인 상담</a>'
)

CTA_LABEL_PATTERN = re.compile(r'<span class="cta-label">(.*?) 전후사진</span>')


def process_file(path):
    content = open(path, encoding='utf-8').read()
    original = content

    depth = path.replace('\\', '/').count('/')
    root = '../' * depth

    content = NAV_PATTERN.sub(
        lambda m: f'<li><a href="{m.group(1)}">상담·예약</a></li>',
        content,
    )

    if CTA_PATTERN.search(content):
        label_match = CTA_LABEL_PATTERN.search(content)
        cat_name = label_match.group(1) if label_match else ''
        content = CTA_PATTERN.sub(
            f'<a href="{root}counsel/?from={cat_name}" class="cta-card">',
            content,
        )

    content = FOOTER_PATTERN.sub(
        f'<a href="{root}counsel/">온라인 상담</a>',
        content,
    )

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


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
