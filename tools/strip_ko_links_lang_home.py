"""외국어 홈(/en/, /ja/, /zh/)에서 한국어 페이지로 가는 링크를 모두 뺀다 (2026-10-23 결정). 다시 실행해도 안전.

- 케이스 카드(사진)는 링크 없는 <div>로 바꾼다(사진은 그대로 보임)
- 'View all' 링크, 케이스 리뷰 배너, 헤더 'Case Reviews' 메뉴, 언어 선택·푸터의 한국어 항목 삭제
- 온라인 상담 폼 카드(/counsel/ = 한국어 폼)는 메일 링크(mailto)로 교체
사용: python tools/strip_ko_links_lang_home.py
"""
import os, re, sys

NL = chr(13) + chr(10)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.stdout.reconfigure(encoding='utf-8')


def apply(lang):
    path = os.path.join(BASE, lang, 'index.html')
    s = open(path, encoding='utf-8-sig').read()
    n0 = len(s)
    # 케이스 카드 <a ... class="case-card"> ... </a> → <div class="case-card"> ... </div>
    s = re.sub(r'<a href="https://journal\.rococops\.com/[^"]*" class="case-card"[^>]*>(.*?)</a>',
               r'<div class="case-card">\1</div>', s, flags=re.S)
    # 시술별 'View all' 링크
    s = re.sub(r'\n?\s*<a href="https://journal\.rococops\.com/[a-z-]+/" class="view-all-link"[^>]*>.*?</a>', '', s, flags=re.S)
    # 헤더 케이스 리뷰 메뉴
    s = re.sub(r'\n?\s*<li><a href="\.\./cases/">.*?</a></li>', '', s)
    # 케이스 리뷰 배너 섹션
    s = re.sub(r'\n?(<!-- 케이스 리뷰 배너 -->\s*)?<section class="cases-banner">.*?</section>\n?', '\n', s, flags=re.S)
    # 언어 선택·푸터의 한국어
    s = re.sub(r'<a href="/" class="lang-option">[^<]*</a>', '', s)
    s = re.sub(r'\n?\s*<p><a href="\.\./" style="[^"]*">한국어</a></p>', '', s)
    # 맨 위 언어 선택 바의 한국어
    s = re.sub(r'\n?[ \t]*<a href="\.\./">한국어</a>', '', s)
    # 온라인 상담 폼(한국어 폼) 카드 → 메일 링크
    s = s.replace('<a href="https://journal.rococops.com/counsel/" class="consult-card">',
                  '<a href="mailto:rococo2015@naver.com" class="consult-card">')
    # 카드 호버 효과 제거(더 이상 링크가 아니므로)
    s = s.replace('.case-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.10); }\n', '')
    open(path, 'w', encoding='utf-8-sig', newline=NL).write(s)
    print(f'{lang}: {n0} → {len(s)} bytes')


if __name__ == '__main__':
    for l in ('en', 'ja', 'zh'):
        apply(l)
