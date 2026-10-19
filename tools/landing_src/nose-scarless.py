"""data/landing/nose-scarless.json 생성 (흉터없는 코성형 = 비개방 코성형 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nose-scarless.py   →  data/landing/nose-scarless.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/scarless/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


data = {
    "_comment": "시술별 대표페이지 데이터(비개방 코성형). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구. 622(2025)·527(2024)를 중심으로, 수치는 옛 글 8·115에서만 나와 그대로 출처 표시.",
    "page": "nose/scarless",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "비개방 코성형(흉터없는 코성형) | 실리콘+귀연골 방식, 가능한 코와 한계 | 로코코성형외과 김상호 원장",
        "description": "콧구멍 안쪽으로만 수술해 바깥쪽으로 흉터를 남기지 않는 비개방 코성형입니다. 실리콘과 귀연골을 쓰는 방식, 개방형과의 차이, 비개방이 가능한 코와 한계, 회복을 김상호 원장의 글로 정리했습니다.",
        "h1": "비개방 코성형(흉터없는 코성형)",
        "procedure_name": "비개방 코성형"
    },

    "hero": {
        "eyebrow": "CLOSED RHINOPLASTY · 비개방 코성형(흉터없는 코성형)",
        "question": "비개방 코성형(흉터없는 코성형)은 어떻게 수술하나요?",
        "summary": {"text": seg('527', (30, 31)), "src": src('527')},
        "stats": [
            {"to": 17, "unit": "년", "label": "이 수술법으로 수술해 온 기간",
             "quote": seg('527', (39, 42)), "src": src('527')},
            {"to": 1, "unit": "시간 전후", "label": "수술 시간",
             "quote": seg('8', 10), "src": src('8')},
            {"to": 5, "unit": "일", "label": "출근이 가능할 정도로 붓기가 빠지는 시점 (코성형만 할 경우)",
             "quote": seg('8', (40, 41)), "src": src('8')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('622'), "image": "https://rococops.com/files/editor/20251022111511900189142.jpg",
                 "alt": "비개방 코성형 수술 전후 정면 사진", "label": "CASE · 정면 4주", "layout": "stack"}
    },

    "features": {
        "type": "ADVANTAGES · CLOSED RHINOPLASTY",
        "toc": "비개방 코성형의 장점",
        "title": seg('622', 17),
        "items": [seg('622', 18), seg('622', 19), seg('622', (20, 21)), seg('622', 22), seg('622', 23), seg('622', 24)],
        "note": seg('622', (31, 34)),
        "src": src('622')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "콧구멍 안쪽으로만 수술하는 코성형",
             "paras": [seg('622', (5, 7)), seg('622', (8, 10))], "src": src('622')},
            {"heading": "비개방으로 할 수 있는 코",
             "paras": [seg('527', (47, 48)), seg('527', 61)], "src": src('527')},
            {"heading": "17년째 해 온 수술법",
             "paras": [seg('527', (39, 42)), seg('527', (43, 45))], "src": src('527')},
            {"heading": "제가 생각하는 수술 목표",
             "paras": [seg('622', (62, 64)), seg('622', 65), seg('622', 66), seg('622', 67)], "src": src('622')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('622', 12), "icon": "ear"},
            {"text": seg('622', 13).rstrip(','), "icon": "fill"},
            {"text": seg('622', (14, 16)), "icon": "tip"},
            {"text": seg('622', (51, 52)), "icon": "graft"},
            {"text": seg('622', 69), "icon": "clock"},
        ],
        "steps_src": src('622'),
        "note": {"text": seg('527', (36, 38)), "src": src('527')},
        "pros_cons": {"paras": [seg('622', 25), seg('622', 26), seg('622', 27), seg('622', 28), seg('622', 29)],
                      "src": src('622')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('8', 9), seg('8', 10)], "src": src('8')},
            {"label": "5일", "lines": [seg('8', 12), seg('8', (40, 41))], "src": src('8')},
            {"label": "1주", "lines": [seg('8', 11)], "src": src('8')},
            {"label": "1–2주 (매부리·절골 함께)", "lines": [seg('115', (43, 44))], "src": src('115')},
            {"label": "1년 6개월", "lines": [seg('622', 69)], "src": src('622')},
        ],
        "note": {"text": seg('527', 35), "src": src('527')}
    },

    "before_after": {
        "title": "비개방 코성형(흉터없는 코성형) 전후",
        "alt": "비개방 코성형 수술 전후 사진",
        "items": [
            {"src": src('622'), "image": "https://rococops.com/files/editor/20251022111511900189142.jpg",
             "caption": "수술 전과 수술 후 4주째 사진입니다.", "label": "정면 4주"},
            {"src": src('622'), "image": "https://rococops.com/files/editor/20251022111558505541797.jpg",
             "caption": "아래쪽에서 본 전후사진입니다.", "label": "아래쪽에서"},
            {"src": src('622'), "image": "https://rococops.com/files/editor/202510221116231066884509.jpg",
             "caption": "양 측면 전후사진입니다.", "label": "측면"},
            {"src": src('527'), "image": "https://rococops.com/files/editor/20240312101207661990353.jpg",
             "caption": "로코코 비개방 귀연골코수술 받으시고, 비순각수술, 미간 지방이식 받으신 분입니다.",
             "label": "사면 · 비순각·미간 지방이식 함께"},
            {"src": src('527'), "image": "https://rococops.com/files/editor/202403121012421602156239.jpg",
             "caption": "남자 첫 코수술을 비개방으로 할 수 있으면", "label": "남자 첫 코수술 · 사면"},
            {"src": src('527'), "image": "https://rococops.com/files/editor/20240312101305906999444.jpg",
             "caption": "타병원 코수술 후 복코가 되어", "label": "복코 재수술 · 사면"},
            {"src": src('115'), "image": "https://rococops.com/files/editor/1386152131.jpg",
             "caption": "매부리 부위를 다듬어주고,", "label": "비개방 매부리코 교정 · 측면"},
            {"src": src('503'), "image": "https://rococops.com/files/editor/20240126135902824634617.jpg",
             "caption": "수술 전과 수술 후 2주 사진입니다.", "label": "찝힌코 교정 · 2주"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('622'), "tag": "장단점·비주말린 코"},
            {"src": src('527'), "tag": "수술법 설명"},
            {"src": src('115'), "tag": "비개방 매부리코"},
            {"src": src('503'), "tag": "비개방 찝힌코 교정"},
            {"src": src('397'), "tag": "코 안 흉터 교정"},
            {"src": src('8'), "tag": "초기 기록"},
        ]
    },

    "faq": [
        {"q": "비개방으로 코끝을 많이 높일 수 있나요?", "a": seg('527', (28, 29)), "src": src('527')},
        {"q": "수술 후 숨쉬기가 불편해지지 않나요?", "a": seg('527', (32, 34)), "src": src('527')},
        {"q": "세월이 지나면 코끝이 낮아지거나 연골이 비치지 않나요?", "a": seg('527', 20) + ' ' + seg('527', (25, 26)),
         "src": src('527')},
        {"q": "찝힌코도 비개방으로 교정할 수 있나요?", "a": seg('503', (7, 11)), "src": src('503')},
        {"q": "코 안 흉터를 교정하려고 연골을 절제하면 코끝이 무너지지 않나요?", "a": seg('397', (19, 25)), "src": src('397')},
    ],

    "related": [
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
        {"href": "nose/septal", "name": "비중격연골 코성형"},
        {"href": "nose/hump", "name": "매부리코"},
        {"href": "nose/male", "name": "남자의 코성형"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "guide/rhinoplasty-material-guide", "name": "코성형 재료 비교 (가이드)"},
    ],

    "review_banner_subject": "비개방 코성형(흉터없는 코성형)",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-scarless.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
