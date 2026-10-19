"""data/landing/nose-rib-cartilage.json 생성 (늑연골 명품코성형 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nose-rib-cartilage.py   →  data/landing/nose-rib-cartilage.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/rib-cartilage/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


IMG = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(늑연골 명품코성형). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nose/rib-cartilage",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "자가늑연골 코성형 | 늑연골 채취 방법·흉터, 재료 비교, 코끝 수술 | 로코코성형외과 김상호 원장",
        "description": "자가늑연골 코성형은 본인의 늑연골로 코끝을 만드는 수술입니다. 채취 방법과 흉터, 기증늑연골·실리콘과의 비교, 코가 휘는지 궁금한 점을 김상호 원장의 글로 정리했습니다.",
        "h1": "자가늑연골 코성형",
        "procedure_name": "자가늑연골 코성형"
    },

    "hero": {
        "eyebrow": "RIB CARTILAGE · 늑연골 명품코성형",
        "question": "늑연골 코성형은 어떻게 수술하나요?",
        "summary": {"text": seg('360', (62, 65)), "src": src('360')},
        "stats": [
            {"to": 15, "unit": "분", "label": "늑연골 채취·봉합 시간",
             "quote": seg('121', 31), "src": src('121')},
            {"to": 2, "unit": "cm", "label": "채취 부위 절개 길이",
             "quote": seg('367', (56, 57)), "src": src('367')},
            {"from": 90, "to": 150, "unit": "분", "label": "수술 시간 (들린코 교정 · 복합 수술)",
             "quote": seg('6', 27), "src": src('6'),
             "extra": [{"quote": seg('468', 99), "src": src('468')}]},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('602'), "image": IMG + "202504161359071449698646.jpg",
                 "alt": "늑연골 코성형 수술 전후 정면 사진", "label": "CASE · 정면 전후", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · COSTAL CARTILAGE",
        "toc": "코끝에 쓰는 자가연골",
        "title": seg('320', 28),
        "items": [x.strip() for x in lines('320')[29].split(',')],
        "note": seg('320', (30, 32)),
        "src": src('320')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "자가늑연골만 사용하는 이유",
             "paras": [seg('359', (191, 193)), seg('359', (194, 200)), seg('359', (201, 205))],
             "src": src('359')},
            {"heading": "늑연골로 코끝을 높이면 코가 휘나요?",
             "paras": [seg('320', (40, 47)), seg('320', (62, 67)), seg('320', (68, 71))],
             "src": src('320')},
            {"heading": "콧대에는 실리콘, 늑연골은 코끝에",
             "paras": [seg('375', (8, 9)), seg('375', (18, 22)), seg('375', (23, 33))],
             "src": src('375')},
            {"heading": "늑연골 채취 14년",
             "paras": [seg('367', (17, 19)), seg('367', (24, 29))],
             "src": src('367')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('320', (82, 84)), "icon": "graft"},
            {"text": seg('320', (89, 91)), "icon": "deviation"},
            {"text": seg('320', (93, 96)), "icon": "fill"},
            {"text": seg('320', (98, 101)), "icon": "clock"},
            {"text": seg('320', (114, 115)), "icon": "tip"},
        ],
        "steps_src": src('320'),
        "note": {"text": seg('320', (103, 106)), "src": src('320')},
        "pros_cons": {"paras": [seg('359', (148, 151)), seg('359', (228, 241))], "src": src('359')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "들린코 교정", "lines": [seg('6', (27, 29))], "src": src('6')},
            {"label": "복합 수술", "lines": [seg('468', (99, 100)), seg('468', (101, 102))], "src": src('468')},
            {"label": "채취 부위 1개월", "lines": [seg('360', (46, 49))], "src": src('360')},
            {"label": "붓기", "lines": [seg('217', (38, 39))], "src": src('217')},
        ],
        "note": {"text": seg('360', (50, 51)), "src": src('360')}
    },

    "before_after": {
        "title": "늑연골 코성형 수술 전후",
        "alt": "늑연골 코성형 수술 전후 사진",
        "items": [
            {"src": src('585'), "image": IMG + "202408221341111389463943.jpg",
             "caption": "수술 전과 수술 후 4주 정면 사진입니다.", "label": "정면 4주"},
            {"src": src('482'), "image": IMG + "202308111048112138275172.jpg",
             "caption": "수술 전과 수술 후 6개월 사진입니다.", "label": "정면 6개월"},
            {"src": src('482'), "image": IMG + "202308111049472011909210.jpg",
             "caption": "우측면 전후사진입니다.", "label": "우측면"},
            {"src": src('540'), "image": IMG + "202404021006171159131696.jpg",
             "caption": "수술 전과 수술 후 4주 정면 전후사진입니다.", "label": "정면 4주"},
            {"src": src('540'), "image": IMG + "20240402100725630667782.jpg",
             "caption": "우측면 전후사진", "label": "우측면"},
            {"src": src('437'), "image": IMG + "20221103104844880870932.jpg",
             "caption": "우사면에서 본 전후사진입니다.", "label": "우사면"},
            {"src": src('487'), "image": IMG + "20231117142300286538886.jpg",
             "caption": "우측면 전후사진입니다.", "label": "우측면"},
            {"src": src('589'), "image": IMG + "20240930123508515117922.jpg",
             "caption": "수술 전과 수술 후 3주 사진입니다.", "label": "정면 3주"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('359'), "tag": "자가 vs 기증"},
            {"src": src('320'), "tag": "코 휨"},
            {"src": src('375'), "tag": "콧대 사용"},
            {"src": src('360'), "tag": "채취 흉터"},
            {"src": src('487'), "tag": "구축코 사례"},
            {"src": src('602'), "tag": "뾰족코 사례"},
        ]
    },

    "faq": [
        {"q": "늑연골로 코끝을 높이면 코가 휘나요?", "a": seg('320', (36, 39), (40, 47)), "src": src('320')},
        {"q": "늑연골을 채취한 자리에는 흉터가 얼마나 남나요?", "a": seg('360', (37, 40), (50, 51)), "src": src('360')},
        {"q": "늑연골 채취는 안전한가요?", "a": seg('360', (20, 26)), "src": src('360')},
        {"q": "자가늑연골과 기증늑연골은 무엇이 다른가요?", "a": seg('359', (194, 200), (228, 232)), "src": src('359')},
        {"q": "콧대까지 늑연골로 높일 수 있나요?", "a": seg('375', (8, 9), (18, 22), (92, 97)), "src": src('375')},
    ],

    "related": [
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nose/columella", "name": "비주성형"},
        {"href": "nose/hump", "name": "매부리코"},
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nose/septal", "name": "비중격연골 코성형"},
    ],

    "review_banner_subject": "늑연골 코성형 수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-rib-cartilage.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
