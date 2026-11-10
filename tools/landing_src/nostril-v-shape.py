"""data/landing/nostril-v-shape.json 생성 (V형 콧구멍교정 대표페이지).
옛 글 7편(149·158·174·266·306·410·415) 중 1인칭 칼럼 원문 줄 범위만 그대로 이어붙인다.
사용: python tools/landing_src/nostril-v-shape.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('nostril/v-shape')

ICON_STITCH = ('<path d="M20 60 C40 40 80 40 100 60" fill="none" stroke="#4a4a4a" stroke-width="2.4" stroke-linecap="round"/>'
               '<path d="M36 46 L36 70 M52 42 L52 66 M68 42 L68 66 M84 46 L84 70" stroke="#c46a5a" stroke-width="3" stroke-linecap="round"/>')

data = {
    "_comment": "시술별 대표페이지 데이터(V형 콧구멍교정). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nostril/v-shape",
    "seo": {
        "apply": True,
        "title": "V형 콧구멍교정 | 콧구멍이 많이 보일 때 · 비공내리기가 맞지 않는 경우 | 로코코성형외과 김상호 원장",
        "description": "콧구멍이 많이 보이는데 비공내리기가 맞지 않는 경우, 콧날개올리기를 응용한 V형 콧구멍교정은 어떤 수술인지, 가려지는 정도와 단점, 회복을 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "V형 콧구멍교정",
        "procedure_name": "V형 콧구멍교정"
    },
    "hero": {
        "eyebrow": "V-SHAPE NOSTRIL · V형 콧구멍교정",
        "question": "V형 콧구멍교정은 어떤 수술인가요?",
        "summary": {"text": seg('158', 1), "src": src('158')},
        "stats": [
            {"from": 20, "to": 30, "unit": "분", "label": "수술 시간 (양쪽)", "quote": seg('158', 43), "src": src('158')},
            {"from": 1, "to": 2, "unit": "mm", "label": "콧구멍이 가려지는 정도", "quote": seg('158', (35, 36)), "src": src('158')},
            {"to": 1, "unit": "주", "label": "콧속 실밥 제거", "quote": seg('158', 45), "src": src('158')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('158'), "image": "https://rococops.com/files/editor/20181112878383692.jpg",
                 "alt": "V형 콧구멍교정 수술 전후 사진", "label": "CASE · 정면 3주", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · NOSTRIL",
        "toc": "콧구멍을 가리는 수술",
        "title": seg('306', (5, 7)),
        "items": [seg('306', 8), seg('306', 9), seg('306', 10), seg('306', 11)],
        "note": seg('306', (13, 14)),
        "src": src('306')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "콧구멍 자체의 문제는 두 가지로 나눕니다", "paras": [seg('174', (10, 16))], "src": src('174')},
            {"heading": "V 콧구멍 교정은 이렇게 만든 수술입니다", "paras": [seg('174', (21, 30))], "src": src('174')},
            {"heading": "비공내리기가 맞지 않을 때 합니다", "paras": [seg('158', (7, 11)), seg('158', (12, 14))], "src": src('158')},
            {"heading": "가려지는 정도는 크지 않습니다", "paras": [seg('266', (35, 37)), seg('266', 65)], "src": src('266')},
        ]
    },
    "icons": {"stitch": ICON_STITCH},
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('158', 42), "icon": "sleep"},
            {"text": seg('158', 43), "icon": "clock"},
            {"text": seg('158', 44), "icon": "tape"},
            {"text": seg('158', 45), "icon": "stitch"},
        ],
        "steps_src": src('158'),
        "note": {"text": seg('266', (56, 60)), "src": src('266')},
        "pros_cons": {"paras": [raw('306', 76, 81), raw('306', 82, 84), raw('306', 88, 93)], "src": src('306')}
    },
    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 다음날", "lines": [seg('158', (27, 30))], "src": src('158')},
            {"label": "1주", "lines": [seg('158', 45)], "src": src('158')},
            {"label": "6주", "lines": [seg('174', (50, 51))], "src": src('174')},
            {"label": "흉터가 튀어나온 경우", "lines": [raw('410', 78, 86)], "src": src('410')},
        ],
        "note": {"text": seg('266', (44, 49)), "src": src('266')}
    },
    "before_after": {
        "title": "V형 콧구멍교정 전후",
        "alt": "V형 콧구멍교정 전후 사진",
        "items": [
            {"src": src('158'), "image": "https://rococops.com/files/editor/20181112878383692.jpg",
             "caption": "콧날개올리기 응용한 v-콧구멍 교정술 전후사진입니다.", "label": "정면 3주"},
            {"src": src('158'), "image": "https://rococops.com/files/editor/20181112332904724.jpg",
             "caption": "실내조명에서 찍은 수술전후 사진입니다.", "label": "실내조명"},
            {"src": src('306'), "image": "https://rococops.com/files/editor/20200115123102721511441.jpg",
             "caption": "우사면 콧날개올리기 전후사진 입니다.", "label": "우사면 3주"},
            {"src": src('306'), "image": "https://rococops.com/files/editor/20200115123132357144064.jpg",
             "caption": "좌사면에서 역시 콧볼이 어느 정도 올라간것이 보입니다.", "label": "좌사면 3주"},
            {"src": src('306'), "image": "https://rococops.com/files/editor/20200115123140893191091.jpg",
             "caption": "좌측면 수술전후 3주", "label": "좌측면 3주"},
            {"src": src('174'), "image": "https://rococops.com/files/editor/20151222425314357.jpg",
             "label": "비공내리기 병행 6주"},
            {"src": src('410'), "image": "https://rococops.com/files/editor/20220502112228121330214.jpg",
             "caption": "콧날개올리기 단독 수술로", "label": "뾰족한 V 콧구멍 7주"},
            {"src": src('410'), "image": "https://rococops.com/files/editor/20220502112328667497613.jpg",
             "caption": "수술 전과 수술 후 7주째 사진입니다.", "label": "아래쪽 7주"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('158'), "tag": "종합 설명"},
            {"src": src('174'), "tag": "비공내리기 병행"},
            {"src": src('266'), "tag": "인중축소술 후"},
            {"src": src('306'), "tag": "장점과 단점"},
            {"src": src('410'), "tag": "뾰족한 V 콧구멍"},
            {"src": src('149'), "tag": "콧날개·콧구멍 줄이기 병행"},
        ]
    },
    "faq": [
        {"q": "V형 콧구멍교정으로 콧구멍이 얼마나 가려지나요?", "a": seg('158', (35, 36)), "src": src('158')},
        {"q": "수술 후 일상생활은 언제부터 가능한가요?", "a": seg('158', (27, 30)), "src": src('158')},
        {"q": "수술 후 흉터가 남나요?", "a": seg('266', (50, 53)), "src": src('266')},
        {"q": "인중축소술을 받은 뒤 콧구멍이 많이 보이는데 효과가 있나요?", "a": seg('266', (81, 85)), "src": src('266')},
        {"q": "좌우 콧구멍 모양이 다른데 수술하면 맞춰지나요?", "a": seg('149', (20, 21)), "src": src('149')},
    ],
    "related": [
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nostril/reduction", "name": "콧구멍축소술"},
        {"href": "nostril/alar-base", "name": "콧볼축소술"},
        {"href": "nose/bulbous", "name": "복코"},
        {"href": "nose/columella", "name": "비주성형"},
    ],
    "review_banner_subject": "V형 콧구멍교정",
    "cases_visible": 9
}
write(data, 'nostril-v-shape')
