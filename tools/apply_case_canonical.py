"""케이스 상세 페이지의 canonical 을 rococops.com 원글로 바꾼다 (저널 ② 적용 계획).

- 입력: 매칭표 CSV (저널_②매칭표.csv). 구분 A·B(원글 있음)만 바꾸고, C(원글 없음, 칼럼)는 self canonical 그대로 둔다.
- 진료항목(최상위 폴더) 단위로 적용: cheekbone / nose / nostril / eye / forehead / anti-aging
- 기본은 미리보기(dry-run). 실제로 쓰려면 --write. 11/6 이전에는 --write 를 쓰지 않는다.
- 줄바꿈(CRLF/LF)은 파일 원래대로 유지한다.

사용:
  python tools/apply_case_canonical.py 매칭표.csv                      # 전체 미리보기
  python tools/apply_case_canonical.py 매칭표.csv --cat eye --write    # eye 만 적용
"""
import os, re, sys, csv, argparse, collections

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CANON_RE = re.compile(r'(<link rel="canonical" href=")([^"]*)(")')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('--cat', help='적용할 진료항목(최상위 폴더). 생략하면 전체')
    ap.add_argument('--write', action='store_true', help='실제로 파일을 수정')
    a = ap.parse_args()

    stat = collections.Counter()
    with open(a.csv, encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        path, kind, url = r['저널경로'], r['구분'], r['원글URL(canonical 후보)']
        cat = path.split('/')[0]
        if a.cat and cat != a.cat:
            continue
        if not kind.startswith(('A', 'B')) or not url:
            stat[(cat, 'C 유지(self)')] += 1
            continue
        f = os.path.join(BASE, path, 'index.html')
        raw = open(f, 'rb').read()
        s = raw.decode('utf-8')
        m = CANON_RE.search(s)
        if not m:
            stat[(cat, '오류: canonical 없음')] += 1
            continue
        new = url.replace('&', '&amp;')
        if m.group(2) == new:
            stat[(cat, '이미 적용')] += 1
            continue
        stat[(cat, '변경')] += 1
        if a.write:
            s = s[:m.start(2)] + new + s[m.end(2):]
            open(f, 'wb').write(s.encode('utf-8'))
    for (cat, k), n in sorted(stat.items()):
        print(f'{cat:12} {k:16} {n}')
    print('(미리보기)' if not a.write else '(파일 수정됨)')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
