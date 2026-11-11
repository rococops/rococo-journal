#!/usr/bin/env python3
"""push 전 구조화데이터(JSON-LD) 검사 — 구글 Search Console 오류 메일을 미리 막는다.

검사: JSON 문법, Review 의 대상 유형(구글이 인정하는 것만), FAQ 답변 누락, 경로 표시(BreadcrumbList) 누락,
      글 유형의 제목·작성자 누락.

사용: python tools/check_jsonld.py              (커밋 안 한 변경 파일만)
      python tools/check_jsonld.py --sitemap    (사이트맵에 있는 페이지 전체)
      python tools/check_jsonld.py 파일...       (지정 파일)
오류가 있으면 종료 코드 1.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
# 구글 리뷰 스니펫이 인정하는 대상 유형 (MedicalProcedure 는 안 됨)
REVIEW_OK = {'Book', 'Course', 'CreativeWorkSeason', 'CreativeWorkSeries', 'Episode', 'Event', 'Game', 'HowTo',
             'LocalBusiness', 'MediaObject', 'Movie', 'MusicPlaylist', 'MusicRecording', 'Organization', 'Product',
             'Recipe', 'SoftwareApplication', 'MedicalBusiness', 'MedicalClinic', 'Physician', 'Hospital'}
ARTICLE = {'Article', 'NewsArticle', 'BlogPosting', 'MedicalWebPage'}


def types(x):
    t = x.get('@type')
    return set(t if isinstance(t, list) else [t])


def walk(x):
    if isinstance(x, dict):
        yield x
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)


def check(path):
    errs = []
    t = open(path, encoding='utf-8', errors='replace').read()
    for raw in LD.findall(t):
        try:
            data = json.loads(raw)
        except ValueError as e:
            errs.append('JSON 문법 오류: %s' % e)
            continue
        for o in walk(data):
            ty = types(o)
            if 'Review' in ty:
                it = o.get('itemReviewed')
                if not isinstance(it, dict) or not (types(it) & REVIEW_OK):
                    errs.append('Review 대상 유형이 구글 기준에 안 맞음: %s' % (it.get('@type') if isinstance(it, dict) else it))
            if 'Question' in ty and not (o.get('acceptedAnswer') or {}).get('text'):
                errs.append('FAQ 답변 없음: %s' % str(o.get('name'))[:40])
            if 'BreadcrumbList' in ty:
                for li in o.get('itemListElement') or []:
                    if not li.get('name') or not (li.get('item') or li.get('position') == len(o['itemListElement'])):
                        errs.append('경로 표시 항목에 name/item 없음 (position %s)' % li.get('position'))
            if ty & ARTICLE:
                if not (o.get('headline') or o.get('name')):
                    errs.append('%s 제목 없음' % '/'.join(sorted(ty)))
                if not o.get('author'):
                    errs.append('%s 작성자 없음' % '/'.join(sorted(ty)))
    return errs


def targets():
    args = sys.argv[1:]
    if args and args[0] == '--sitemap':
        s = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
        return [os.path.join(ROOT, p.replace('/', os.sep), 'index.html')
                for p in re.findall(r'<loc>https://journal\.rococops\.com/(.*?)</loc>', s)]
    if args:
        return args
    out = subprocess.run(['git', '-c', 'core.quotepath=off', 'status', '--porcelain'], cwd=ROOT,
                         capture_output=True, text=True, encoding='utf-8').stdout.splitlines()
    return [os.path.join(ROOT, l[3:].strip().strip('"')) for l in out if l[3:].strip().strip('"').endswith('.html')]


def main():
    files = [f for f in targets() if os.path.isfile(f)]
    bad = {}
    for f in files:
        e = check(f)
        if e:
            bad[os.path.relpath(f, ROOT).replace(os.sep, '/')] = e
    kinds = {}
    for f, es in bad.items():
        for e in es:
            kinds.setdefault(e.split(':')[0], []).append(f)
    print('검사 %d개 파일, 오류 있는 파일 %d개' % (len(files), len(bad)))
    for k, fs in kinds.items():
        print('  [%d건] %s — 예: %s' % (len(fs), k, fs[0]))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
