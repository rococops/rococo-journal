#!/usr/bin/env python3
"""대표페이지를 build_landing.py 로 다시 만든 뒤 반드시 실행하는 후처리 (여러 번 실행해도 같은 결과).

1. 말투 통일 (tools/tone_normalize.py)
2. 회복 타임라인 라벨의 괄호 설명을 <small> 두 번째 줄로 분리
3. rococops.com/files 이미지를 저널 안(images/rococo/)으로 이전 (tools/localize_landing_images.py)

사용: python tools/postprocess_landing.py
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import localize_landing_images as loc  # noqa: E402
from tone_normalize import tone  # noqa: E402

LABEL = re.compile(r'(<span class="lp-tl-label">)(.*?)(</span>)')


def _label(m):
    inner = m.group(2).replace('<br>', ' ')
    mm = re.match(r'^(.*?)\s*\((.+)\)$', inner)
    if '<small>' in inner or not mm or not mm.group(1).strip():
        return m.group(0)
    return m.group(1) + mm.group(1).strip() + '<small>(' + mm.group(2) + ')</small>' + m.group(3)


def main():
    changed = 0
    root = os.path.dirname(HERE)
    for p in loc.find_pages():
        rel = os.path.relpath(p, root).replace(os.sep, '/')
        if rel.split('/')[0] in ('en', 'ja', 'zh'):  # 외국어 페이지는 말투·라벨 규칙 대상이 아님(이미지만 아래에서 처리)
            continue
        t = open(p, encoding='utf-8', newline='').read()
        t2 = LABEL.sub(_label, tone(t))
        if t2 != t:
            open(p, 'w', encoding='utf-8', newline='').write(t2)
            changed += 1
    print('말투·라벨 후처리: %d개 페이지 수정' % changed)
    sys.argv = [sys.argv[0]]
    loc.main()  # 이미지 변환·주소 교체(이미 한 것은 건너뜀)


if __name__ == '__main__':
    main()
