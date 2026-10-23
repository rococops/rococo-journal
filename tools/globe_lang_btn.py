"""외국어 페이지의 'GLOBAL' 언어 버튼을 지구본 아이콘 + 언어 코드로 바꾼다 (한국어 사이트는 js/main.js가 같은 모양으로 바꿈). 다시 실행해도 안전."""
import glob, sys

SVG = ('<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.7 3.9 5.7 3.9 9s-1.3 6.3-3.9 9c-2.6-2.7-3.9-5.7-3.9-9S9.4 5.7 12 3z"/></svg>')
OLD = '<button class="lang-btn" id="langBtn">🌐 GLOBAL &#9662;</button>'


def new(lang):
    return f'<button class="lang-btn lang-btn--globe" id="langBtn" aria-label="Language">{SVG}<span>{lang.upper()}</span></button>'


if __name__ == '__main__':
    n = 0
    for lang in ('en', 'ja', 'zh'):
        for f in glob.glob(f'{lang}/**/index.html', recursive=True):
            s = open(f, encoding='utf-8', newline='').read()
            if OLD in s:
                open(f, 'w', encoding='utf-8', newline='').write(s.replace(OLD, new(lang)))
                n += 1
    print('바꾼 파일', n)
