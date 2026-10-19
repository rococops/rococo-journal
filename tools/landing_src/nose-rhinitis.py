"""data/landing/nose-rhinitis.json 생성 (비염수술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nose-rhinitis.py   →  data/landing/nose-rhinitis.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/rhinitis/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


# 이 페이지 전용 아이콘 (하비갑개 부분축소술 3단계). 공용 build_landing.py 는 고치지 않는다.
_TUNNEL = ('<path d="M60 14 C38 14 22 40 22 70 C22 94 38 106 60 106 C82 106 98 94 98 70 C98 40 82 14 60 14 Z" '
           'fill="#efe4d3" stroke="#b8956a" stroke-width="2.2"/>'
           '<path d="M60 16 L60 104" fill="none" stroke="#b8956a" stroke-width="3"/>')
ICONS = {
    # 하비갑개 뼈 일부 제거: 코안 단면, 한쪽 하비갑개에 절제선(점선)
    "concha": _TUNNEL + '<ellipse cx="36" cy="78" rx="12" ry="16" fill="#f1cfb8" stroke="#b8956a" stroke-width="2"/>'
              '<ellipse cx="84" cy="78" rx="12" ry="16" fill="#f1cfb8" stroke="#b8956a" stroke-width="2"/>'
              '<path d="M28 66 L48 90" fill="none" stroke="#c46a5a" stroke-width="2.4" stroke-dasharray="4 3"/>',
    # 남은 뼈 미세골절 후 바깥쪽으로: 하비갑개 + 바깥 방향 화살표
    "outfracture": _TUNNEL + '<ellipse cx="32" cy="78" rx="9" ry="14" fill="#f1cfb8" stroke="#b8956a" stroke-width="2"/>'
                   '<ellipse cx="88" cy="78" rx="9" ry="14" fill="#f1cfb8" stroke="#b8956a" stroke-width="2"/>'
                   '<path d="M52 50 L38 50 M43 45 L38 50 L43 55 M68 50 L82 50 M77 45 L82 50 L77 55" fill="none" '
                   'stroke="#c46a5a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    # 점막 고주파: 번개 모양
    "rf": '<ellipse cx="60" cy="74" rx="26" ry="30" fill="#f1cfb8" stroke="#b8956a" stroke-width="2.2"/>'
          '<path d="M66 20 L50 56 L62 56 L52 90 L76 46 L63 46 L72 20 Z" fill="#b8956a"/>',
}

data = {
    "_comment": "시술별 대표페이지 데이터(비염수술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nose/rhinitis",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "비염수술 | 코막힘 원인(비중격만곡증·하비갑개 비대)과 코성형 동시 수술 | 로코코성형외과 김상호 원장",
        "description": "비염수술은 비중격이나 하비갑개 때문에 좁아진 공기 통로를 넓히는 수술입니다. 하비갑개 부분축소술 방법, 코성형과 함께 하는 경우, 수술 후 호흡과 회복을 김상호 원장의 글과 내시경 전후사진으로 정리했습니다.",
        "h1": "비염수술",
        "procedure_name": "비염수술"
    },

    "icons": ICONS,

    "hero": {
        "eyebrow": "RHINITIS SURGERY · 비염수술",
        "question": "비염수술은 어떻게 수술하나요?",
        "summary": {"text": seg('369', (15, 17)), "src": src('369')},
        "stats": [
            {"to": 15, "unit": "분", "label": "수술 시간",
             "quote": seg('18', 19), "src": src('18')},
            {"to": 3, "unit": "일", "label": "회복 기간",
             "quote": seg('18', 20), "src": src('18')},
            {"to": 13, "unit": "년", "label": "비염수술 집도 (2019년 글 기준)",
             "quote": seg('288', (100, 101)), "src": src('288')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('311'), "image": "https://rococops.com/files/editor/202002031100221164281735.jpg",
                 "alt": "비염수술 전후 내시경 사진", "label": "CASE · 내시경 전후", "layout": "stack"}
    },

    "features": {
        "type": "CAUSE · NASAL OBSTRUCTION",
        "toc": "코막힘의 원인",
        "title": seg('369', (9, 11)),
        "items": [seg('369', (12, 14)), seg('369', (15, 17)), seg('369', (18, 20))],
        "note": seg('369', (7, 8)),
        "src": src('369')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "비염수술은 정해진 한 가지 수술이 아닙니다",
             "paras": [seg('571', 24), seg('571', (25, 28)), seg('571', (29, 31)), seg('571', (32, 34))],
             "src": src('571')},
            {"heading": "비중격만곡증과 하비갑개 비대",
             "paras": [seg('288', (23, 26)), seg('288', (28, 31)), seg('288', (32, 37)), seg('288', (41, 42))],
             "src": src('288')},
            {"heading": "코성형과 비염수술을 함께 하는 경우",
             "paras": [seg('571', (35, 37)), seg('571', (38, 39)), seg('571', (40, 42))],
             "src": src('571')},
            {"heading": "코막힘은 개인적인 느낌입니다",
             "paras": [seg('571', (53, 55)), seg('571', (56, 60)), seg('571', (61, 64))],
             "src": src('571')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('318', (49, 50)).rstrip(','), "icon": "deviation"},
            {"text": seg('318', 51), "icon": "concha"},
            {"text": seg('318', 52), "icon": "outfracture"},
            {"text": seg('318', 53), "icon": "rf"},
        ],
        "steps_src": src('318'),
        "note": {"text": seg('318', (54, 56)), "src": src('318')},
        "pros_cons": {"paras": [seg('288', (15, 19)), seg('288', (100, 107))], "src": src('288')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "회복 기간", "lines": [seg('18', 20)], "src": src('18')},
            {"label": "1개월", "lines": [seg('311', (58, 59))], "src": src('311')},
            {"label": "6주", "lines": [seg('288', (95, 99))], "src": src('288')},
            {"label": "2개월", "lines": [seg('318', (58, 60))], "src": src('318')},
            {"label": "3개월", "lines": [seg('536', (46, 48)), seg('536', (50, 51))], "src": src('536')},
        ],
        "note": {"text": seg('288', (91, 93)), "src": src('288')}
    },

    "before_after": {
        "title": "비염수술 전후 내시경 사진",
        "alt": "비염수술 전후 내시경 사진",
        "items": [
            {"src": src('311'), "image": "https://rococops.com/files/editor/202002031100221164281735.jpg",
             "caption": "이렇게 됩니다.", "label": "양쪽 · 1개월"},
            {"src": src('288'), "image": "https://rococops.com/files/editor/201910071400571002057460.jpg",
             "caption": "수술 전과 수술 후 6주째 모습입니다.", "label": "우측 · 6주"},
            {"src": src('288'), "image": "https://rococops.com/files/editor/20191007140124188821073.jpg",
             "caption": "역시 우측 하비갑개 전후사진입니다.", "label": "우측 · 6주"},
            {"src": src('288'), "image": "https://rococops.com/files/editor/20191007140134416974769.jpg",
             "caption": "좌측 하비갑개 수술 후 6주 사진입니다.", "label": "좌측 · 6주"},
            {"src": src('318'), "image": "https://rococops.com/files/editor/20200309151813676889676.jpg",
             "caption": "수술 전과 수술 후 2개월째 내시경 소견입니다.", "label": "양쪽 · 2개월"},
            {"src": src('78'), "image": "https://rococops.com/files/album/attach1/1_201109051744443204.jpg",
             "caption": "위쪽이 수술전이고, 아래쪽이 수술후입니다.", "label": "위 수술 전 · 아래 수술 후"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('571'), "tag": "종합 설명"},
            {"src": src('288'), "tag": "비중격·하비갑개"},
            {"src": src('369'), "tag": "수술 방법"},
            {"src": src('536'), "tag": "코성형과 비염"},
            {"src": src('318'), "tag": "코성형 동시 수술"},
            {"src": src('378'), "tag": "부작용 질문"},
        ]
    },

    "faq": [
        {"q": "비염이 없는데 코성형하면서 비염수술을 같이 하자고 해요.", "a": seg('571', (87, 93)), "src": src('571')},
        {"q": "비염수술만 따로 받을 수도 있나요?", "a": seg('18', (16, 17)), "src": src('18')},
        {"q": "코성형 후에 비염이 생길 수 있나요?", "a": seg('536', (35, 40)), "src": src('536')},
        {"q": "비중격만곡증·비염수술 후 코끝이 내려앉을 수 있나요?", "a": seg('378', (19, 21), (25, 30)), "src": src('378')},
        {"q": "겨울이 되면 수술한 코가 막히고 코피가 나요.", "a": seg('311', (10, 20)), "src": src('311')},
    ],

    "related": [
        {"href": "nose/septal", "name": "비중격연골 코성형"},
        {"href": "nose/hump", "name": "매부리코"},
        {"href": "nose/osteotomy", "name": "절골술"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
        {"href": "nose/male", "name": "남자 코성형"},
    ],

    "review_banner_subject": "비염수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-rhinitis.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
