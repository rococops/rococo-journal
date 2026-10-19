"""data/landing/nostril-alar-base.json 생성 (콧볼축소술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nostril-alar-base.py   →  data/landing/nostril-alar-base.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nostril/alar-base/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


NAME = '콧볼축소술(콧날개축소술)'

data = {
    "_comment": "시술별 대표페이지 데이터(콧볼축소술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구. c105/c106/c139 는 236/75/12 의 복제본이라 숫자 번호 글을 사용.",
    "page": "nostril/alar-base",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "콧볼축소술(콧날개축소술) | 넓은 콧볼·복코, 콧볼 형태별 수술법과 흉터 | 로코코성형외과 김상호 원장",
        "description": "콧볼축소술(콧날개축소술)은 넓게 벌어진 콧볼을 줄이는 수술입니다. 복코교정과의 관계, 콧볼 형태·콧구멍 크기에 따른 수술법, 수술하면 안 되는 콧볼, 절개선과 봉합, 흉터가 흐려지는 과정을 김상호 원장의 글로 정리했습니다.",
        "h1": NAME,
        "procedure_name": NAME
    },

    "hero": {
        "eyebrow": "ALAR BASE REDUCTION · 콧볼축소술",
        "question": f"{NAME}은 어떻게 수술하나요?",
        "summary": {"text": seg('12', (4, 6)), "src": src('12')},
        "stats": [
            {"from": 15, "to": 20, "unit": "분", "label": "수술 시간",
             "quote": seg('12', 26), "src": src('12')},
            {"to": 5, "unit": "일", "label": "회복 기간 · 세안 및 화장",
             "quote": seg('12', 27), "src": src('12'),
             "extra": [{"quote": seg('12', 28), "src": src('12')}]},
            {"from": 6, "to": 12, "unit": "개월", "label": "흉터가 흐려지는 시기",
             "quote": seg('268', (33, 34)), "src": src('268'),
             "extra": [{"quote": seg('295', (144, 146)), "src": src('295')}]},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('268'), "image": "https://rococops.com/files/editor/201907021036561772643227.jpg",
                 "alt": "콧볼축소술 수술 전후 사진", "label": "CASE · 전후", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · ALAR BASE",
        "toc": "콧볼축소술이 잘 맞는 콧볼",
        "title": seg('268', (7, 8)),
        "items": [seg('268', 9), seg('268', 11), seg('268', (46, 48))],
        "note": seg('268', (19, 22)),
        "src": src('268')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "복코교정과 함께 하는 경우가 많습니다",
             "paras": [seg('295', (7, 13))], "src": src('295')},
            {"heading": "콧볼축소술을 비추천하는 콧볼",
             "paras": [seg('518', (5, 8)), seg('518', (16, 17)), seg('518', 35)], "src": src('518')},
            {"heading": "절개선 위치와 봉합",
             "paras": [seg('579', (31, 38)), seg('579', (56, 58)), seg('579', (72, 73))], "src": src('579')},
            {"heading": "흉터를 줄이는 수술은 디자인에서 시작합니다",
             "paras": [seg('75', 19), seg('75', (22, 27)), seg('75', (32, 34))], "src": src('75')},
        ]
    },

    "icons": {
        "ellipse": '<path d="M34 78 Q60 34 86 78" fill="#efe4d3" stroke="#b8956a" stroke-width="2.4"/><ellipse cx="60" cy="74" rx="18" ry="7" fill="none" stroke="#c46a5a" stroke-width="2.2" stroke-dasharray="4 3"/>',
        "thin": '<path d="M30 80 Q60 30 90 80" fill="none" stroke="#b8956a" stroke-width="10" stroke-linecap="round" opacity=".35"/><path d="M30 80 Q60 30 90 80" fill="none" stroke="#b8956a" stroke-width="3" stroke-linecap="round"/><path d="M60 44 L60 60 M54 54 L60 60 L66 54" fill="none" stroke="#c46a5a" stroke-width="2.4" stroke-linecap="round"/>',
        "nostril": '<ellipse cx="44" cy="66" rx="14" ry="20" fill="#efe4d3" stroke="#b8956a" stroke-width="2.4"/><ellipse cx="80" cy="66" rx="9" ry="14" fill="#efe4d3" stroke="#b8956a" stroke-width="2.4"/><path d="M60 66 L66 66" stroke="#c46a5a" stroke-width="2.4" stroke-linecap="round"/>',
        "keep": '<ellipse cx="44" cy="66" rx="12" ry="18" fill="#efe4d3" stroke="#b8956a" stroke-width="2.4"/><ellipse cx="76" cy="66" rx="12" ry="18" fill="#efe4d3" stroke="#b8956a" stroke-width="2.4"/><path d="M52 98 L68 98" stroke="#c46a5a" stroke-width="2.4" stroke-linecap="round"/><path d="M52 104 L68 104" stroke="#c46a5a" stroke-width="2.4" stroke-linecap="round"/>',
        "thread": '<path d="M28 74 Q44 54 60 74 T92 74" fill="none" stroke="#c46a5a" stroke-width="2.4" stroke-linecap="round"/><circle cx="28" cy="74" r="4" fill="#b8956a"/><circle cx="92" cy="74" r="4" fill="#b8956a"/>'
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('295', (30, 32)), "icon": "ellipse"},
            {"text": seg('295', 33), "icon": "keep"},
            {"text": seg('295', (34, 37)), "icon": "thin"},
            {"text": seg('295', (38, 40)), "icon": "nostril"},
            {"text": seg('295', (86, 88)), "icon": "thread"},
        ],
        "steps_src": src('295'),
        "note": {"text": seg('295', (41, 45)), "src": src('295')},
        "pros_cons": {"paras": [seg('579', (44, 47)), seg('579', (76, 82))], "src": src('579')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "5일", "lines": [seg('12', 27), seg('12', 28)], "src": src('12')},
            {"label": "실밥 제거 후", "lines": [seg('268', (32, 34))], "src": src('268')},
            {"label": "6~12개월", "lines": [seg('295', (144, 148))], "src": src('295')},
            {"label": "피부가 검은 편이라면", "lines": [seg('75', (49, 50)), seg('75', 54)], "src": src('75')},
        ],
        "note": {"text": seg('12', (23, 24)), "src": src('12')}
    },

    "before_after": {
        "title": f"{NAME} 전후",
        "alt": "콧볼축소술 수술 전후 사진",
        "items": [
            {"src": src('268'), "image": "https://rococops.com/files/editor/201907021036561772643227.jpg",
             "caption": "콧볼축소술 전후사진 입니다.", "label": "정면 · 열흘째"},
            {"src": src('268'), "image": "https://rococops.com/files/editor/201907021038002024296498.jpg",
             "caption": "아래쪽에서 본 전후사진입니다.", "label": "아래쪽에서"},
            {"src": src('295'), "image": "https://rococops.com/files/editor/20191105135238343585107.jpg",
             "caption": "좌측이 수술전이고", "label": "type C · 수술 직후"},
            {"src": src('295'), "image": "https://rococops.com/files/editor/201911051353151625827480.jpg",
             "caption": "수술 전과 수술 후 2주째 사진입니다.", "label": "type D · 2주 (융비술 동시)"},
            {"src": src('624'), "image": "https://rococops.com/files/editor/20251022111511900189142.jpg",
             "caption": "수술 전과 수술 후 4주째 사진입니다.", "label": "콧구멍-콧볼 축소 · 4주"},
            {"src": src('624'), "image": "https://rococops.com/files/editor/20251022111558505541797.jpg",
             "caption": "아래쪽에서 본 전후사진입니다.", "label": "아래쪽에서"},
            {"src": src('236'), "image": "https://rococops.com/files/album/attach1/1_20110508184752036.jpg",
             "caption": "일반적인 복코교정 사례였습니다.", "label": "복코교정 + 콧날개 줄이기"},
            {"src": src('75'), "image": "https://rococops.com/files/editor/1303382555.jpg",
             "caption": "자~ 이 사진을 보시면 콧날개 줄이기라는 수술에 대해 좀 더 이해하시기 쉬울 듯 합니다.", "label": "콧날개 줄이기"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('295'), "tag": "콧볼 형태별 수술법"},
            {"src": src('518'), "tag": "수술하면 안 되는 콧볼"},
            {"src": src('579'), "tag": "절개선 · 봉합"},
            {"src": src('268'), "tag": "콧구멍 동시 축소"},
            {"src": src('624'), "tag": "코성형 + 콧구멍·콧볼 축소"},
            {"src": src('75'), "tag": "흉터"},
        ]
    },

    "faq": [
        {"q": "복코교정만 하면 콧볼이 더 커 보이나요?", "a": seg('236', (10, 11)), "src": src('236')},
        {"q": "콧볼축소술을 하면 안 되는 코도 있나요?", "a": seg('518', (5, 8)), "src": src('518')},
        {"q": "콧볼축소술 흉터는 남나요?", "a": seg('579', (44, 47)), "src": src('579')},
        {"q": "콧구멍을 같이 줄이면 숨쉬기가 불편해지지 않나요?", "a": seg('295', (115, 119)), "src": src('295')},
        {"q": "수술 후 주의할 점이 있나요?", "a": seg('579', (19, 21)), "src": src('579')},
    ],

    "related": [
        {"href": "nostril/reduction", "name": "콧구멍축소술"},
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nostril/v-shape", "name": "V형 콧구멍교정"},
        {"href": "nose/bulbous", "name": "복코성형"},
        {"href": "nose/revision", "name": "코재수술"},
    ],

    "review_banner_subject": NAME,
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nostril-alar-base.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
