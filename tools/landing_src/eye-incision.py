"""data/landing/eye-incision.json 생성 (트임성형 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/eye-incision.py   →  data/landing/eye-incision.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'eye/incision/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


# 눈 일러스트 공통 요소 (120x120)
_EYE = ('<path d="M14 62 C32 40 80 40 94 62 C80 80 32 80 14 62 Z" fill="#fff" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/>'
        '<circle cx="54" cy="61" r="13" fill="#6b4a3a"/><circle cx="54" cy="61" r="5" fill="#2b2b2b"/>')
_RIM = '<path d="M106 26 C118 48 118 76 106 98" fill="none" stroke="#b8956a" stroke-width="3" stroke-linecap="round"/>'

ICONS = {
    # 상담 시 눈꼬리를 만져 뼈(안와골)와의 공간 확인: 눈 + 바깥 뼈 테두리 + 손끝
    'eyetouch': _EYE + _RIM +
                '<ellipse cx="100" cy="74" rx="7" ry="10" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2" transform="rotate(-25 100 74)"/>',
    # 눈꼬리~뼈 사이 공간 4mm: 측정 화살표
    'gap': _EYE + _RIM +
           '<path d="M95 62 L105 62 M98 58 L94 62 L98 66 M102 58 L106 62 L102 66" fill="none" stroke="#c46a5a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
           '<text x="66" y="34" font-size="13" font-weight="700" fill="#b8956a" font-family="sans-serif">4mm</text>',
    # 눈꼬리를 뒤쪽으로 열기: 원래 눈꼬리(점선) → 새 눈꼬리(금색)
    'open': '<path d="M14 62 C32 40 80 40 94 62 C80 80 32 80 14 62 Z" fill="#fff" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round" stroke-dasharray="4 4"/>'
            '<path d="M14 62 C32 40 80 40 94 62 L106 64 C84 82 32 80 14 62 Z" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linejoin="round"/>'
            '<circle cx="54" cy="61" r="13" fill="#6b4a3a"/><circle cx="54" cy="61" r="5" fill="#2b2b2b"/>'
            '<path d="M86 90 L104 90 M98 84 L104 90 L98 96" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    # 수술 시간 (공용 clock 과 같은 모양을 쓰지 않고 공용 이름을 그대로 사용하므로 여기선 정의하지 않음)
    # 눈꼬리 여유살이 부드러워짐: 눈꼬리의 작은 볼록 + 고주파 물결
    'smooth': _EYE +
              '<path d="M92 56 C98 52 102 58 98 64" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="3 3"/>'
              '<path d="M84 26 C88 22 92 30 96 26 C100 22 104 30 108 26" fill="none" stroke="#b8956a" stroke-width="2.2" stroke-linecap="round"/>'
              '<path d="M84 36 C88 32 92 40 96 36 C100 32 104 40 108 36" fill="none" stroke="#b8956a" stroke-width="2.2" stroke-linecap="round"/>',
}

CASE_IMG = 'https://rococops.com/files/editor/20260624162240603620012.jpg'

data = {
    "_comment": "시술별 대표페이지 데이터(트임성형). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "eye/incision",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "트임성형 | 앞트임·뒤트임(뒷트임)·밑트임 차이, 뒤트임 가능한 눈과 회복 | 로코코성형외과 김상호 원장",
        "description": "트임성형은 눈을 키우는 방향에 따라 앞트임·뒤트임(뒷트임)·밑트임으로 나뉩니다. 뒤트임이 가능한 눈의 기준(눈꼬리 뒤 공간 4mm), 다시 붙지 않게 하는 수술 방법, 흉터와 회복 과정을 김상호 원장의 글로 정리했습니다.",
        "h1": "트임성형",
        "procedure_name": "트임성형"
    },

    "icons": ICONS,

    "hero": {
        "eyebrow": "CANTHOPLASTY · 트임성형",
        "question": "앞트임·뒤트임·밑트임은 어떻게 다른가요?",
        "summary": {"text": seg('263', (6, 8)), "src": src('263')},
        "stats": [
            {"to": 4, "unit": "mm", "label": "뒤트임을 권하는 눈꼬리 뒤 공간 (이상)",
             "quote": seg('350', (30, 31)), "src": src('350')},
            {"from": 10, "to": 30, "unit": "분", "label": "수술 시간 (밑트임 · 뒤트임)",
             "quote": seg('510', (11, 13)), "src": src('510'),
             "extra": [{"quote": seg('263', 47), "src": src('263')}]},
            {"to": 16, "unit": "년", "label": "다듬어 온 뒤트임 수술법 (2024년 글 기준)",
             "quote": seg('506', (9, 10)), "src": src('506')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('629'), "image": CASE_IMG,
                 "alt": "뒤트임 수술 전과 수술 후 2년 정면 눈 사진", "label": "CASE · 뒤트임 2년", "layout": "stack"}
    },

    "features": {
        "type": "POINT · 뒤트임",
        "toc": "뒤트임의 기준",
        "title": seg('21', 206),
        "items": [seg('21', i) for i in range(207, 212)],
        "note": seg('21', (46, 47)),
        "src": src('21')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "눈을 키우는 방향에 따라 다른 트임",
             "paras": [seg('263', (6, 11))], "src": src('263')},
            {"heading": "뒤트임으로 커질 수 있는 크기는 이미 정해져 있습니다",
             "paras": [seg('350', (18, 21)), seg('350', (22, 24)), seg('350', (25, 29))], "src": src('350')},
            {"heading": "앞트임은 과하지 않게",
             "paras": [seg('508', (17, 23)), seg('508', (63, 64))], "src": src('508')},
            {"heading": "왜 뒤트임은 다시 붙는다고 알려져 있을까",
             "paras": [seg('629', (22, 23)), seg('629', (24, 27))], "src": src('629')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('263', (21, 24)), "icon": "eyetouch"},
            {"text": seg('263', 25), "icon": "gap"},
            {"text": seg('263', (51, 53)), "icon": "open"},
            {"text": seg('263', 47).rstrip(','), "icon": "clock"},
            {"text": seg('263', (63, 65)), "icon": "smooth"},
        ],
        "steps_src": src('263'),
        "note": {"text": seg('263', (41, 42)), "src": src('263')},
        "pros_cons": {"paras": [seg('629', (28, 32)), seg('629', (66, 68))], "src": src('629')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "1주 · 3주", "lines": [seg('263', (47, 50))], "src": src('263')},
            {"label": "결막충혈 · 부종", "lines": [seg('629', (60, 65))], "src": src('629')},
            {"label": "1개월", "lines": [seg('629', (71, 73))], "src": src('629')},
            {"label": "1년 6개월", "lines": [seg('629', 76)], "src": src('629')},
            {"label": "2년", "lines": [seg('629', (89, 90))], "src": src('629')},
        ],
        "note": {"text": seg('263', (54, 57)), "src": src('263')}
    },

    "before_after": {
        "title": "트임성형 전후",
        "alt": "트임성형 수술 전후 눈 사진",
        "items": [
            {"src": src('629'), "image": CASE_IMG,
             "caption": "뒤트임 수술전 : 2년차 전후사진", "label": "뒤트임 정면 2년"},
            {"src": src('629'), "image": "https://rococops.com/files/editor/20260624162312118728172.jpg",
             "caption": "뒤트임 수술전 : 2년차 전후사진", "label": "뒤트임 눈꼬리 2년"},
            {"src": src('629'), "image": "https://rococops.com/files/editor/20260624162408282085631.jpg",
             "caption": "뒤트임 수술전 : 1주차 : 1년6개월 : 2년차 전후사진", "label": "뒤트임 연속 경과"},
            {"src": src('263'), "image": "https://www.rococops.com/files/editor/20150923493437080.jpg",
             "caption": "정면 뒷트임, 밑트임 수술 전과 수술 후 3년째 사진입니다.", "label": "뒤트임+밑트임 3년"},
            {"src": src('263'), "image": "https://www.rococops.com/files/editor/201509231111591732.jpg",
             "caption": "우측 눈 뒷트임, 밑트임 수술 전과 수술 후 3년째 사진입니다.", "label": "우측 눈 3년"},
            {"src": src('508'), "image": "https://rococops.com/files/editor/202402231304211878351825.jpg",
             "caption": "제가 <앞트임 밴드 없애기> 라고 부르는 수술만 한 앞트임 전후사진입니다.", "label": "앞트임 밴드 없애기"},
            {"src": src('508'), "image": "https://rococops.com/files/editor/20240223130728518134257.jpg",
             "caption": seg('508', (69, 70)), "label": "리드래핑 앞트임"},
            {"src": src('508'), "image": "https://rococops.com/files/editor/20240223130629743380151.jpg",
             "caption": seg('508', (66, 67)), "label": "쌍커풀 + 앞트임"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('629'), "tag": "뒤트임 2년 경과"},
            {"src": src('350'), "tag": "뒤트임 가능한 눈"},
            {"src": src('263'), "tag": "뒤트임+밑트임 3년"},
            {"src": src('508'), "tag": "앞트임·윗트임"},
            {"src": src('510'), "tag": "비절개 밑트임"},
            {"src": src('506'), "tag": "뒤트임 전후사진"},
        ]
    },

    "faq": [
        {"q": "뒤트임은 시간이 지나면 다시 붙지 않나요?", "a": seg('629', (33, 36)), "src": src('629')},
        {"q": "눈꼬리 뒤 공간이 4mm보다 좁으면 어떻게 하나요?", "a": seg('350', (30, 37)), "src": src('350')},
        {"q": "밑트임은 어떻게 수술하나요?", "a": seg('510', (11, 15)), "src": src('510')},
        {"q": "앞트임 흉터는 남나요?", "a": seg('508', 68), "src": src('508')},
        {"q": "뒤트임으로 새로 생긴 눈꼬리에는 속눈썹이 없나요?", "a": seg('629', (77, 82)), "src": src('629')},
    ],

    "related": [
        {"href": "eye/double", "name": "쌍커풀 자연유착법"},
        {"href": "eye/correction", "name": "눈매교정술"},
        {"href": "eye/lower-fat", "name": "눈밑지방 재배치"},
        {"href": "eye/fat-graft", "name": "꺼진눈 지방이식"},
        {"href": "eye/brow-lift", "name": "눈썹하거상술"},
        {"href": "nose/revision", "name": "코재수술"},
    ],

    "review_banner_subject": "트임성형",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'eye-incision.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
