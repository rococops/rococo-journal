"""data/landing/nose-septal.json 생성 (비중격연골 코성형 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
한 줄에 여러 문장이 붙어 있는 칼럼(148)은 cut()으로 '문장 경계'에서만 앞뒤를 덜어낸다(문장 안은 고치지 않음).
사용: python tools/landing_src/nose-septal.py   →  data/landing/nose-septal.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/septal/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


def cut(text, start=None, end=None):
    """문장 경계에서만 자르기: start 로 시작하는 문장부터, end 로 끝나는 문장까지. 경계가 아니면 오류."""
    if start is not None:
        i = text.index(start)
        assert i == 0 or text[i - 2:i] in ('. ', '? '), start
        text = text[i:]
    if end is not None:
        j = text.index(end) + len(end)
        assert end[-1] in '.?', end
        text = text[:j]
    return text


IMG = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(비중격연골 코성형). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨·features.title 은 제작 문구.",
    "page": "nose/septal",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "비중격연골 코성형 | 비중격 채취와 L자 지지대, 휜코 교정, 연골 선택 | 로코코성형외과 김상호 원장",
        "description": "비중격연골 코성형은 콧속 비중격연골을 얻어 코끝을 높이는 수술입니다. 연골을 얼마나 남겨야 코가 내려앉지 않는지(L자 지지대), 귀연골·늑연골과의 선택, 휜코 교정과 회복을 김상호 원장의 글로 정리했습니다.",
        "h1": "비중격연골 코성형",
        "procedure_name": "비중격연골 코성형"
    },

    "hero": {
        "eyebrow": "SEPTAL CARTILAGE · 비중격연골 코성형",
        "question": "비중격연골 코성형은 어떻게 수술하나요?",
        "summary": {"text": seg('7', (38, 40)), "src": src('7')},
        "stats": [
            {"from": 8, "to": 10, "unit": "mm", "label": "남겨두는 L자 지지대(L-strut) 폭",
             "quote": cut(seg('148', 10), start='빨간 화살표가', end='유지된답니다.'), "src": src('148')},
            {"to": 1, "unit": "주", "label": "회복 기간",
             "quote": seg('7', 8), "src": src('7')},
            {"from": 2, "to": 3, "unit": "주", "label": "콧속 실이 녹는 기간",
             "quote": seg('41', 17), "src": src('41')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('98'), "image": IMG + "1325762113.jpg",
                 "alt": "비중격연골 코성형 휜코교정 수술 전후 정면 사진", "label": "CASE · 정면 전후", "layout": "stack"}
    },

    "features": {
        "type": "MATERIAL · SEPTAL CARTILAGE",
        "toc": "연골에 대해 자주 듣는 이야기",
        "title": "상담 때 자주 듣는 연골 이야기",
        "items": [seg('214', 8), seg('214', 10), seg('214', 12), seg('214', 14), seg('214', 16), seg('214', (18, 19))],
        "note": seg('214', (22, 28)),
        "src": src('214')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "비중격연골은 어디에서 얻나요",
             "paras": [cut(seg('148', 3), start='비중격 연골은 양쪽에서'), seg('148', (5, 6))],
             "src": src('148')},
            {"heading": "얼마나 잘라내고, 얼마나 남기나요",
             "paras": [cut(seg('148', (7, 9)), start='질문하신 분이'),
                       cut(seg('148', 10), end='L-strut 이라고 부르는 부위입니다.')],
             "src": src('148')},
            {"heading": "코끝이 주연이고 콧대는 조연입니다",
             "paras": [seg('7', (17, 21)), seg('7', (26, 29))],
             "src": src('7')},
            {"heading": "휜코와 안면비대칭",
             "paras": [seg('157', (5, 7)), seg('157', (21, 24)), seg('157', (32, 35)), seg('157', (53, 54))],
             "src": src('157')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('313', (62, 65)), "icon": "deviation"},
            {"text": seg('313', (88, 89)), "icon": "tip"},
            {"text": seg('313', (90, 92)), "icon": "hump"},
            {"text": seg('313', (93, 101)), "icon": "graft"},
            {"text": seg('313', 116), "icon": "fill"},
        ],
        "steps_src": src('313'),
        "note": {"text": seg('313', (106, 111)), "src": src('313')},
        "pros_cons": {"paras": [seg('157', (85, 86)), seg('157', (97, 101))], "src": src('157')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('41', (18, 21))], "src": src('41')},
            {"label": "5일 · 10일", "lines": [seg('41', (13, 15)), seg('41', 16)], "src": src('41')},
            {"label": "1주", "lines": [seg('7', (8, 9))], "src": src('7')},
            {"label": "2~3주", "lines": [seg('41', 17), seg('41', 24)], "src": src('41')},
            {"label": "2개월", "lines": [seg('628', 96)], "src": src('628')},
        ],
        "note": {"text": seg('64', 12), "src": src('64')}
    },

    "before_after": {
        "title": "비중격연골 코성형 수술 전후",
        "alt": "비중격연골 코성형 수술 전후 사진",
        "items": [
            {"src": src('157'), "image": IMG + "201811101187000392.jpg",
             "caption": "수술전과 수술 후 2개월째 사진입니다.", "label": "휜코 정면 2개월"},
            {"src": src('157'), "image": IMG + "20181110162790042.jpg",
             "caption": "아래쪽에서 본 휜코교정 수술전후 사진입니다.", "label": "휜코 아래쪽"},
            {"src": src('313'), "image": IMG + "202002281452322136557617.jpg",
             "caption": "수술전과 수술 후 2주째 사진입니다.", "label": "휜코 정면 2주"},
            {"src": src('313'), "image": IMG + "20200228145307748988585.jpg",
             "caption": "아래쪽에서 본 사진에서", "label": "휜코 아래쪽"},
            {"src": src('98'), "image": IMG + "1324347904.jpg",
             "caption": "코끝은 비중격 연골을 이용해서 모양을 잡았고,", "label": "측면"},
            {"src": src('7'), "image": IMG + "1342957704.jpg",
             "caption": "두루뭉실한 느낌의 코끝이 오똑하게 자리잡은 것을 볼 수 있습니다.", "label": "코끝 측면"},
            {"src": src('69'), "image": IMG + "1342967352.jpg",
             "caption": "정면 수술 전사진을 보면", "label": "복코 정면"},
            {"src": src('628'), "image": IMG + "202604101037101943388366.jpg",
             "caption": "수술 전과 수술 후 2개월 정면 전후사진입니다.", "label": "재수술 정면 2개월"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('148'), "tag": "채취·L자 지지대"},
            {"src": src('214'), "tag": "연골 선택"},
            {"src": src('313'), "tag": "휜코 수술"},
            {"src": src('157'), "tag": "안면비대칭 휜코"},
            {"src": src('628'), "tag": "비중격 재활용"},
            {"src": src('633'), "tag": "비중격 기둥 재활용"},
        ]
    },

    "faq": [
        {"q": "비중격연골을 떼어내면 코가 내려앉지 않나요?",
         "a": seg('148', (11, 12)) + ' ' + cut(seg('148', 13), end='라고 부릅니다.') + ' '
              + cut(seg('148', (16, 18)), start='그런데,', end='극히 드문 일이랍니다.'),
         "src": src('148')},
        {"q": "귀연골이 아니라 비중격연골을 쓰는 이유는 무엇인가요?", "a": seg('214', (37, 41)), "src": src('214')},
        {"q": "비중격만곡증이 있으면 꼭 펴야 휜코가 교정되나요?", "a": seg('313', (17, 36)), "src": src('313')},
        {"q": "콧대를 높이면 휜코가 더 눈에 띄나요?", "a": seg('157', (87, 91)), "src": src('157')},
        {"q": "예전에 비중격연골로 수술했는데, 재수술에는 늑연골을 꼭 써야 하나요?", "a": seg('633', (24, 30)), "src": src('633')},
    ],

    "related": [
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
        {"href": "nose/osteotomy", "name": "절골술"},
        {"href": "nose/bulbous", "name": "복코"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/rhinitis", "name": "비염수술"},
        {"href": "guide/rhinoplasty-material-guide", "name": "코성형 재료 비교 (가이드)"},
    ],

    "review_banner_subject": "비중격연골 코성형",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-septal.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
