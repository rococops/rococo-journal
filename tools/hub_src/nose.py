"""코성형 허브(/nose/) 데이터 생성: data/hub/nose.json
원장님 문장은 landing_lib.seg() 줄 범위로만 가져온다(직접 타이핑 금지). ranges 는 감사용으로 JSON 에 함께 남긴다.
실행: python tools/hub_src/nose.py  →  python tools/verify_hub_quotes.py  →  python tools/build_nose_hub.py
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from landing_lib import seg

C = lambda n: f'nose/column/{n}'


def para(n, *ranges):
    return {'src': C(n), 'ranges': [list(r) if not isinstance(r, int) else [r, r] for r in ranges], 'text': seg(C(n), *ranges)}


def landing(name):
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'landing', name + '.json'), encoding='utf-8'))


# 전후사진: 이미 검증된 시술별 대표페이지(data/landing/nose-*.json)의 첫 사진을 하나씩 가져온다(이미지 URL·캡션 원본 그대로)
_ba = []
for _n in ('hump', 'rib-cartilage', 'revision', 'septal', 'bulbous', 'male', 'columella', 'osteotomy'):
    _d = landing('nose-' + _n)
    _it = _d['before_after']['items'][0]
    _ba.append({'src': _it['src'], 'image': _it['image'], 'caption': _it.get('caption'), 'label': _it.get('label') or _it.get('caption'),
                'alt': _d['before_after']['alt']})
_case = landing('nose-rib-cartilage')['hero']['case']

data = {
    'page': 'nose',
    'hero': {
        'eyebrow': 'NOSE SURGERY · 코성형',
        'bg_image': 'images/landing/nose-hump-hero.jpg',
        'summary': para(144, (69, 70)),   # 약점 먼저: 코끝을 높이는 수술의 방향성
        'case': {k: _case[k] for k in ('src', 'image', 'alt', 'label', 'layout') if k in _case},
        # 숫자는 이 허브 페이지 자체의 집계(칼럼·대표페이지 수). 임상 수치 아님. (옛 문구의 '케이스 247개'는 근거를 확인할 수 없어 쓰지 않음)
        'stats': [{'to': 51, 'unit': '편', 'label': '원장 칼럼'}, {'to': 12, 'unit': '개', 'label': '시술별 대표페이지'}],
    },
    'before_after': {'title': '코성형 수술 전후', 'items': _ba},
    # ── 제작 문구(원문 아님): 질문형 부제·소제목·라벨만 ──
    'labels': {
        'lead_q': '코성형, 무엇부터 알아야 하나요?',
        'ba_title': '코성형 수술 전후',
        'toc': ['시술별 안내', '원장 이야기', '전후사진', '바꿀 수 없는 것', '재료·연골 Q&A', '염증·부작용', '관련 가이드'],
        'story_title': '김상호 원장 이야기',
        'series_title': '코(재)수술로 바꿀 수 없는 것',
        'series_tag': '시리즈',
        'faq_title': '재료·연골, 자주 묻는 질문',
        'risk_title': '염증과 부작용',
        'risk_tag_inflam': '염증',
        'risk_tag_side': '부작용',
        'guide_title': '이 시술, 더 깊이 알아보기',
    },
    # ── 원장 이야기 (최대 4블록) ──
    'story': [
        {'src': C(144), 'paras': [para(144, (5, 8)), para(144, (69, 71)), para(144, (78, 84)), para(144, (90, 98))]},
        {'src': C(529), 'paras': [para(529, (25, 30)), para(529, (31, 33)), para(529, (36, 39))]},
        {'src': C(551), 'paras': [para(551, (12, 13)), para(551, (26, 32)), para(551, (35, 39))]},
        {'src': C(517), 'paras': [para(517, (29, 33))]},
    ],
    # ── 바꿀 수 없는 것 시리즈 (원문 제목만 카드로) ──
    'series': [C(n) for n in (383, 384, 385, 386, 387, 388, 393, 394, 395)],
    # ── FAQ: 질문 = 칼럼 제목, 답변 = 줄 범위 ──
    'faq': [
        para(381, (33, 41), (44, 49)),
        para(547, (14, 21), (26, 28)),
        para(440, (17, 23), (55, 64)),
        para(403, (32, 34), (61, 64)),
    ],
    # ── 염증·부작용 ──
    'risk': {
        'cards': [
            {'tag': 'inflam', 'lead': para(471, (11, 13))},   # 아이코스 문장 제외
            {'tag': 'side', 'lead': para(556, (7, 7))},
        ],
        'items': [para(556, i) for i in range(8, 21)],      # 수술동의서 부작용 13항목 (줄머리 번호는 seg 가 뗌)
        'items_intro': para(556, (7, 7)),
    },
    # ── 관련 가이드(링크만, 인용 없음). 담배·아이코스 제목 글은 제외 ──
    'guides': ['rib-cartilage-rhinoplasty-guide', 'revision-rhinoplasty-side-effects', 'revision-rhinoplasty-inflammation',
               'revision-rhinoplasty-limits', 'rib-cartilage-pointy-tip', 'revision-rhinoplasty-timing'],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'hub', 'nose.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('생성:', os.path.normpath(out))
