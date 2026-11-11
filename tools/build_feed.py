#!/usr/bin/env python3
"""성형 가이드 RSS 피드(feed.xml) 만들기 — guide/posts.json 기준, 최신 30편.

네이버 서치어드바이저·빙에 RSS 로 제출하면 새 글 수집이 빨라진다.
여러 번 실행해도 같은 결과(날짜는 글 발행일만 사용).

사용: python tools/build_feed.py
"""
import datetime
import email.utils
import json
import os
import sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'https://journal.rococops.com'
KST = datetime.timezone(datetime.timedelta(hours=9))


def rfc822(date):
    d = datetime.datetime.strptime(date, '%Y-%m-%d').replace(hour=9, tzinfo=KST)
    return email.utils.format_datetime(d)


def main():
    posts = json.load(open(os.path.join(ROOT, 'guide', 'posts.json'), encoding='utf-8'))
    posts = [p for p in posts if p.get('slug') and p.get('date')]
    posts.sort(key=lambda p: p['date'], reverse=True)
    posts = posts[:30]
    items = []
    for p in posts:
        url = '%s/guide/%s/' % (BASE_URL, p['slug'])
        items.append(
            '  <item>\n'
            '    <title>%s</title>\n'
            '    <link>%s</link>\n'
            '    <guid isPermaLink="true">%s</guid>\n'
            '    <pubDate>%s</pubDate>\n'
            '    <author>김상호 원장</author>\n'
            '    <category>%s</category>\n'
            '    <description>%s</description>\n'
            '  </item>\n' % (escape(p.get('title', '')), url, url, rfc822(p['date']),
                             escape(p.get('tag') or p.get('keyword') or '성형 가이드'), escape(p.get('summary', ''))))
    last = rfc822(posts[0]['date']) if posts else ''
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
           '<channel>\n'
           '  <title>로코코 저널 — 성형 가이드</title>\n'
           '  <link>%s/guide/</link>\n'
           '  <atom:link href="%s/feed.xml" rel="self" type="application/rss+xml"/>\n'
           '  <description>로코코성형외과 김상호 원장이 직접 쓰는 성형 가이드</description>\n'
           '  <language>ko-KR</language>\n'
           '  <lastBuildDate>%s</lastBuildDate>\n'
           '%s'
           '</channel>\n'
           '</rss>\n') % (BASE_URL, BASE_URL, last, ''.join(items))
    path = os.path.join(ROOT, 'feed.xml')
    old = open(path, encoding='utf-8', newline='').read() if os.path.isfile(path) else ''
    if xml != old:
        open(path, 'w', encoding='utf-8', newline='').write(xml)
    print('feed.xml: %d편%s' % (len(posts), '' if xml != old else ' (변경 없음)'))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
