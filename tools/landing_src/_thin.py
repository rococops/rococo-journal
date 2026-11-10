"""글이 적은 하위 메뉴(얇은 대표페이지) 데이터 생성용 공통 도우미.
원장님 문장은 직접 타이핑하지 않고 칼럼 줄 범위(landing_lib.py dump 의 줄 번호)를 seg()/cut() 으로 가져온다.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')


def make(page):
    P = page + '/'

    def seg(n, *ranges):
        return L.seg(P + n, *ranges)

    def src(n):
        return P + n

    def cut(n, i, start, end):
        """칼럼 n 의 i번째 줄에서 start 표지부터 end 표지(포함)까지를 원문 그대로 잘라 온다."""
        t = L.lines(P + n)[i]
        a = t.index(start)
        return t[a:t.index(end, a) + len(end)]

    def raw(n, lo, hi):
        """번호('1. ')를 떼지 않고 원문 줄을 그대로 이어붙임 (번호 목록이 문장 안에 있는 경우)."""
        return ' '.join(L.lines(P + n)[lo:hi + 1])

    return seg, src, cut, raw


def write(data, name):
    out = os.path.join(ROOT, 'data', 'landing', name + '.json')
    json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('written', os.path.normpath(out))
