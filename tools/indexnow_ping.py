#!/usr/bin/env python3
"""바뀐 페이지 주소를 IndexNow 로 네이버·빙에 알린다 (색인 요청 자동화).

두 커밋 사이에 바뀐 index.html 중 사이트맵에 있는 주소만 보낸다(케이스 원문처럼 색인 대상이 아닌 글은 제외).
배포가 끝난 뒤 GitHub Actions(.github/workflows/after-deploy.yml)가 실행한다. 실패해도 배포에는 영향이 없다.

사용: python tools/indexnow_ping.py <이전커밋> <새커밋>
      python tools/indexnow_ping.py --urls https://journal.rococops.com/guide/xxx/ ...
      (--dry 를 붙이면 보내지 않고 목록만 출력)
"""
import glob
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'journal.rococops.com'
BASE_URL = 'https://' + HOST
ENDPOINTS = ['https://api.indexnow.org/indexnow', 'https://searchadvisor.naver.com/indexnow']


def key():
    for f in glob.glob(os.path.join(ROOT, '*.txt')):
        name = os.path.basename(f)[:-4]
        if re.fullmatch(r'[0-9a-f]{32}', name) and open(f).read().strip() == name:
            return name
    return None


def changed_urls(a, b):
    out = subprocess.run(['git', '-c', 'core.quotepath=off', 'diff', '--name-only', a, b], cwd=ROOT,
                         capture_output=True, text=True, encoding='utf-8').stdout.splitlines()
    sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    listed = set(re.findall(r'<loc>(.*?)</loc>', sm))
    urls = []
    for f in out:
        if f == 'index.html':
            u = BASE_URL + '/'
        elif f.endswith('/index.html'):
            u = '%s/%s/' % (BASE_URL, f[:-len('/index.html')])
        else:
            continue
        if u in listed and u not in urls:
            urls.append(u)
    return urls


def main():
    args = [a for a in sys.argv[1:] if a != '--dry']
    dry = '--dry' in sys.argv
    urls = args[1:] if args and args[0] == '--urls' else (changed_urls(args[0], args[1]) if len(args) == 2 else [])
    print('알릴 주소 %d개' % len(urls))
    for u in urls[:20]:
        print(' ', u)
    k = key()
    if not urls or dry or not k:
        if not k:
            print('IndexNow 키 파일이 없습니다.')
        return
    body = json.dumps({'host': HOST, 'key': k, 'keyLocation': '%s/%s.txt' % (BASE_URL, k), 'urlList': urls[:10000]}).encode()
    for ep in ENDPOINTS:
        try:
            req = urllib.request.Request(ep, data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
            print(ep, urllib.request.urlopen(req, timeout=30).status)
        except Exception as e:  # 한쪽이 실패해도 계속
            print(ep, '실패:', e)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
