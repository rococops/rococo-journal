"""sitemap.xml 에 빠진 주소만 추가 (기존 항목·lastmod 는 그대로 둠).

generate_sitemap.py 의 규칙(collect_urls)으로 나와야 할 주소 중 sitemap.xml 에 없는 것을 끝에 덧붙인다.
새 외국어 대표페이지를 올릴 때 사용. 지정한 경로들의 lastmod 를 오늘로 바꾸려면 --touch 경로...

사용: python tools/sitemap_sync.py
      python tools/sitemap_sync.py --touch en/nose/hump/ nose/hump/
"""
import os, re, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_sitemap as gs

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def main():
    os.chdir(BASE)
    today = datetime.date.today().isoformat()
    touch = sys.argv[sys.argv.index('--touch') + 1:] if '--touch' in sys.argv else []
    s = open('sitemap.xml', encoding='utf-8', newline='').read()
    have = set(re.findall(r'<loc>https://journal\.rococops\.com/(.*?)</loc>', s))
    added = []
    for path, pri, lm in gs.collect_urls():
        if path not in have:
            block = f'  <url>\n    <loc>{gs.BASE_URL}/{path}</loc>\n    <lastmod>{lm}</lastmod>\n    <priority>{pri}</priority>\n  </url>\n'
            s = s.replace('</urlset>', block + '</urlset>')
            added.append(path)
    touched = 0
    for p in touch:
        s, k = re.subn(r'(<loc>' + re.escape(f'{gs.BASE_URL}/{p}') + r'</loc>\s*<lastmod>)[^<]*', rf'\g<1>{today}', s, count=1)
        touched += k
    open('sitemap.xml', 'w', encoding='utf-8', newline='').write(s)
    print(f'추가 {len(added)}개: {added}')
    print(f'lastmod 갱신 {touched}개')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
