"""'함께 알아두면 좋은 시술' 데이터 (3순위 흡수, 2026-10-20 사용자 결정).

글이 적은 하위 메뉴 14개를 큰 대표페이지 6곳에 소개 카드로 붙인다.
소개 문장은 각 하위 메뉴 칼럼의 원장님 원문 줄 범위를 그대로 이어붙인 것(재작성 금지).
호스트 페이지 생성 스크립트가 data['companions'] = companions_for(data['page']) 로 가져다 쓴다.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import landing_lib as L


def raw(src, lo, hi):
    """번호('1. ')를 떼지 않고 원문 줄을 그대로 이어붙임 (번호 목록이 문장 안에 있는 경우)."""
    return ' '.join(L.lines(src)[lo:hi + 1])


def part(src, line, start, end):
    """한 줄 안에서 start~end 구간만 (여러 문장이 한 줄로 합쳐진 칼럼)."""
    t = L.lines(src)[line]
    i = t.index(start)
    j = t.index(end, i) + len(end)
    return t[i:j]


def _item(name, href, text, src):
    return {"name": name, "href": href, "lead": {"text": text, "src": src}}


def _build():
    return {
        'nose/columella': [
            _item('긴코', 'nose/long', L.seg('nose/long/11', (3, 9)), 'nose/long/11'),
            _item('비순각 고양이 입매교정', 'nose/cat', L.seg('nose/cat/16', (3, 9)), 'nose/cat/16'),
        ],
        'nostril/alar-raising': [
            _item('콧구멍축소술', 'nostril/reduction', L.seg('nostril/reduction/51', (7, 9)), 'nostril/reduction/51'),
            _item('V형 콧구멍교정', 'nostril/v-shape', L.seg('nostril/v-shape/158', (5, 11)), 'nostril/v-shape/158'),
        ],
        'cheekbone/quick': [
            _item('심부볼·관자 지방이식', 'cheekbone/fat-graft', L.seg('cheekbone/fat-graft/554', (18, 21)), 'cheekbone/fat-graft/554'),
            _item('광대라인 지방흡입', 'cheekbone/liposuction', raw('cheekbone/liposuction/120', 56, 60), 'cheekbone/liposuction/120'),
        ],
        'forehead/endoscopic': [
            _item('이마축소술', 'forehead/reduction', L.seg('forehead/reduction/299', (32, 36)), 'forehead/reduction/299'),
            _item('눈썹하거상술', 'eye/brow-lift', L.seg('eye/brow-lift/507', (5, 11)), 'eye/brow-lift/507'),
        ],
        'eye/correction': [
            _item('꺼진눈 지방이식', 'eye/fat-graft',
                  part('eye/fat-graft/511', 2, '나이가 들면서', '매우 좋은 결과를 만들 수 있습니다.'), 'eye/fat-graft/511'),
            _item('눈밑지방 재배치', 'eye/lower-fat', L.seg('eye/lower-fat/27', (6, 9)), 'eye/lower-fat/27'),
            _item('상·하안검성형', 'anti-aging/blepharoplasty', L.seg('anti-aging/blepharoplasty/28', (3, 9)), 'anti-aging/blepharoplasty/28'),
        ],
        'anti-aging/chin': [
            _item('미세지방이식', 'anti-aging/fat-graft', L.seg('anti-aging/fat-graft/31', (3, 8)), 'anti-aging/fat-graft/31'),
            _item('필러·보톡스', 'anti-aging/filler-botox', L.seg('anti-aging/filler-botox/34', (3, 4), (9, 10)), 'anti-aging/filler-botox/34'),
            _item('엘라스티꿈 실리프팅', 'anti-aging/lifting', L.seg('anti-aging/lifting/332', (6, 11)), 'anti-aging/lifting/332'),
        ],
    }


def companions_for(page):
    items = _build().get(page)
    return {"title": "함께 알아두면 좋은 시술", "items": items} if items else None
