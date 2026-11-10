"""data/landing/nose-long.json 생성 (긴 코 성형 대표페이지).
옛 글 3편(11·c140·274) 중 11 과 274 의 1인칭 칼럼 줄 범위만 그대로 이어붙인다(c140 은 11 의 복제본).
사용: python tools/landing_src/nose-long.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('nose/long')
D = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(긴 코 성형). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 칼럼이 2편뿐이라 회복·수술 단계는 원문에 있는 만큼만. 문장 단위 대조: tools/verify_landing_quotes.py.",
    "page": "nose/long",
    "seo": {
        "apply": True,
        "title": "긴 코 성형 | 코끝이 처졌거나 코가 길어 보일 때 · 장단점 · 전후사진 | 로코코성형외과 김상호 원장",
        "description": "코끝이 처졌거나 중안면이 길어 코가 길어 보일 때 긴 코 성형은 어떻게 디자인하는지, 콧대를 높이면 생기는 단점과 콧구멍 노출 문제를 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "긴 코 성형",
        "procedure_name": "긴 코 성형"
    },
    "hero": {
        "eyebrow": "LONG NOSE · 긴 코 성형",
        "question": "긴 코 성형은 어떤 수술인가요?",
        "summary": {"text": seg('11', (6, 9)), "src": src('11')},
        "stats": [
            {"to": 1, "unit": "시간", "label": "수술 시간 (전후)", "quote": seg('11', 11), "src": src('11')},
            {"to": 1, "unit": "주", "label": "회복 기간", "quote": seg('11', 12), "src": src('11')},
            {"to": 2, "unit": "mm", "label": "이 사례에서 실리콘 보형물로 높인 높이", "quote": seg('274', (44, 47)), "src": src('274')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('274'), "image": D + "201908281550021653361787.jpg",
                 "alt": "긴 코 성형(매부리코수술) 전후 사진", "label": "CASE · 정면 3주", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · LONG NOSE",
        "toc": "긴 코의 두 가지 경우",
        "title": seg('11', (3, 5)),
        "items": [seg('11', 6), seg('11', (7, 9))],
        "note": seg('11', (10, 13)),
        "src": src('11')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "작은 문제의 코가 더 어렵습니다", "paras": [seg('274', (40, 43))], "src": src('274')},
            {"heading": "이 코의 조건과 단점", "paras": [seg('274', (17, 22)), raw('274', 30, 36)], "src": src('274')},
            {"heading": "수술 계획", "paras": [seg('274', (44, 47)), seg('274', (50, 52))], "src": src('274')},
            {"heading": "수술 후 콧구멍이 더 보일 수 있습니다", "paras": [seg('274', (83, 87))], "src": src('274')},
        ]
    },
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('274', (44, 45)), "icon": "graft"},
            {"text": seg('274', 46), "icon": "hump"},
            {"text": seg('274', 47), "icon": "fill"},
            {"text": seg('274', (61, 62)), "icon": "tip"},
        ],
        "steps_src": src('274'),
        "note": {"text": seg('274', (58, 60)), "src": src('274')},
        "pros_cons": {"paras": [raw('274', 67, 76), seg('274', (63, 65))], "src": src('274')}
    },
    "recovery": {
        "title": "회복",
        "items": [
            {"label": "1주", "lines": [seg('11', (12, 13))], "src": src('11')},
            {"label": "수술 후 3주 (사례)", "lines": [seg('274', (83, 85))], "src": src('274')},
        ],
        "note": {"text": seg('274', (86, 87)), "src": src('274')}
    },
    "before_after": {
        "title": "긴 코 성형 전후",
        "alt": "긴 코 성형(매부리코수술) 전후 사진",
        "items": [
            {"src": src('274'), "image": D + "201908281550021653361787.jpg", "caption": seg('274', 54), "label": "정면 3주"},
            {"src": src('274'), "image": D + "20190828155029997268541.jpg", "caption": seg('274', 66), "label": "우사면"},
            {"src": src('274'), "image": D + "20190828155053779310806.jpg", "caption": seg('274', 77), "label": "우측면"},
            {"src": src('274'), "image": D + "20190828155114328316512.jpg", "caption": seg('274', 82), "label": "좌사면"},
            {"src": src('274'), "image": D + "201908281551321976824319.jpg", "caption": seg('274', 88), "label": "좌측면"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('11'), "tag": "종합 설명"},
            {"src": src('274'), "tag": "낮고 긴 코 · 매부리코수술"},
        ]
    },
    "faq": [
        {"q": "긴 코는 어떻게 교정하나요?", "a": seg('11', (6, 9)), "src": src('11')},
        {"q": "콧대를 높이면 코가 더 길어 보이나요?", "a": raw('274', 33, 36), "src": src('274')},
        {"q": "수술 후 콧구멍이 더 많이 보일 수 있나요?", "a": seg('274', (58, 62)), "src": src('274')},
        {"q": "콧구멍이 많이 보이면 어떻게 하나요?", "a": seg('274', (63, 65)), "src": src('274')},
        {"q": "수술 시간과 회복 기간은 얼마나 걸리나요?", "a": seg('11', (11, 13)), "src": src('11')},
    ],
    "related": [
        {"href": "nose/columella", "name": "비주성형"},
        {"href": "nose/hump", "name": "매부리코"},
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nose/septal", "name": "비중격연골 코성형"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/cat", "name": "고양이 수술(입매교정술)"},
    ],
    "review_banner_subject": "긴 코 성형",
    "cases_visible": 9
}
write(data, 'nose-long')
