"""허브 데이터(data/hub/*.json)의 모든 원장님 인용이 원문 칼럼과 일치하는지 대조 (verify_landing_quotes.check 와 같은 말투 규칙 사용).
사용: python tools/verify_hub_quotes.py [data/hub/nose.json]   — 불일치가 있으면 종료코드 1
"""
import sys, os, json, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_landing_quotes import check, BASE
from landing_lib import seg
from tone_normalize import tone

sys.stdout.reconfigure(encoding='utf-8')


def quotes(d):
    for b in d['story']:
        for i, p in enumerate(b['paras']):
            yield f'story[{b["src"][-3:]}][{i}]', p
    for p in d['faq']:
        yield f'faq[{p["src"][-3:]}]', p
    for c in d['risk']['cards']:
        yield f'risk.card[{c["tag"]}]', c['lead']
    for i, p in enumerate(d['risk']['items']):
        yield f'risk.items[{i}]', p
    yield 'risk.items_intro', d['risk']['items_intro']
    yield 'hero.summary', d['hero']['summary']


def main():
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(BASE, 'data', 'hub', '*.json')))
    bad = 0
    for path in paths:
        d = json.load(open(path, encoding='utf-8'))
        print('==', os.path.basename(path))
        for label, p in quotes(d):
            r = []
            check(label, p['src'], p['text'], r)
            ok, _, _, missing = r[0]
            # 데이터 text 가 줄 범위 seg() 결과와 같은지도 확인(직접 타이핑·변조 방지)
            same = p['text'] == seg(p['src'], *[tuple(x) for x in p['ranges']])
            if not same:
                missing = missing + ['(text 가 ranges 의 seg() 결과와 다름)']
            good = ok and same
            print(f'  {"OK  " if good else "MISS"} {label:26} {p["src"]}' + ('' if good else f'  {missing}'))
            bad += not good
        # 전후사진: 이미지 URL·캡션이 해당 칼럼 원본 HTML 에 있어야 함
        for it in d['before_after']['items'] + [d['hero']['case']]:
            raw = open(os.path.join(BASE, it['src'], 'index.html'), encoding='utf-8-sig').read()
            miss = [x for x in (it['image'], it.get('caption')) if x and x not in raw]
            print(f'  {"OK  " if not miss else "MISS"} {"before_after":26} {it["src"]}' + ('' if not miss else f'  {miss}'))
            bad += bool(miss)
        # 아이코스 금지(대표 지시): 인용·카드 원문 어디에도 나오면 안 됨
        blob = json.dumps(d, ensure_ascii=False)
        if '아이코스' in blob:
            print('  MISS 아이코스 문구 포함'); bad += 1
    print(f'\n불일치 {bad}건')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
