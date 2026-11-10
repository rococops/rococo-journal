"""data/landing/nose-cat.json 생성 (고양이 수술(입매교정술) 대표페이지).
옛 글 5편(16·74·346·470·584) 중 원문은 16·74·346 에서만 가져온다(470·584 는 대표 사례 링크로만 연결).
사용: python tools/landing_src/nose-cat.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('nose/cat')

D = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(고양이 수술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 수술 시간·회복 기간은 원문에 없어 비움. 문장 단위 대조: tools/verify_landing_quotes.py.",
    "page": "nose/cat",
    "seo": {
        "apply": True,
        "title": "고양이 수술(입매교정술) | 코끝과 윗입술 라인에 볼륨 · 돌출입 교정 | 로코코성형외과 김상호 원장",
        "description": "고양이 수술(입매교정술, 비순각교정술)은 코끝에서 윗입술로 이어지는 라인에 볼륨을 주는 수술입니다. 어떤 코에 필요한지, 비주내리기·비공내리기와 어떻게 함께 하는지를 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "고양이 수술(입매교정술)",
        "procedure_name": "고양이 수술(입매교정술)"
    },
    "hero": {
        "eyebrow": "NASOLABIAL ANGLE · 고양이 수술(입매교정술)",
        "question": "고양이 수술(입매교정술)은 어떤 수술인가요?",
        "summary": {"text": seg('16', 3), "src": src('16')},
        "stats": [
            {"from": 5, "to": 10, "unit": "%", "label": "비개방 로코코 코성형을 권하는 환자", "quote": seg('16', (17, 18)), "src": src('16')},
            {"to": 4, "unit": "가지", "label": "비주 말린 코끝에 필요한 수술", "quote": seg('346', (79, 80)), "src": src('346')},
            {"to": 1, "unit": "년", "label": "코끝 붓기가 가라앉는 기간", "quote": seg('346', (183, 184)), "src": src('346')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('346'), "image": D + "202008291121191639873212.jpg",
                 "alt": "비주내리기·비공내리기 전후 사진", "label": "CASE · 정면 2개월", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · COLUMELLA",
        "toc": "비주 말린 코끝의 세 가지 문제",
        "title": seg('346', (22, 23)),
        "items": [seg('346', 25), seg('346', 26), seg('346', 27)],
        "note": seg('346', (63, 66)),
        "src": src('346')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "고양이 수술이 뭔가요", "paras": [seg('74', (7, 10))], "src": src('74')},
            {"heading": "수술의 목적", "paras": [raw('346', 71, 77)], "src": src('346')},
            {"heading": "보형물만 넣는 수술과 다릅니다", "paras": [seg('16', (4, 8))], "src": src('16')},
            {"heading": "코성형과 함께 하면", "paras": [seg('16', (19, 23))], "src": src('16')},
        ]
    },
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('16', 9), "icon": "tip"},
            {"text": seg('16', (6, 8)), "icon": "fill"},
            {"text": seg('16', (27, 28)), "icon": "graft"},
        ],
        "steps_src": src('16'),
        "note": {"text": seg('346', (97, 98)), "src": src('346')},
        "pros_cons": {"paras": [seg('346', (100, 107))], "src": src('346')}
    },
    "recovery": {
        "title": "경과",
        "items": [
            {"label": "2개월", "lines": [seg('346', (182, 184))], "src": src('346')},
            {"label": "콧털이 자란 뒤", "lines": [seg('346', (166, 167))], "src": src('346')},
        ],
        "note": {"text": seg('346', (162, 165)), "src": src('346')}
    },
    "before_after": {
        "title": "비주내리기·비공내리기 병행 전후",
        "alt": "비주 말린 코끝 교정 전후 사진",
        "items": [
            {"src": src('346'), "image": D + "202008291121191639873212.jpg", "caption": "비주내리기, 비공내리기, 구축코 교정수술", "label": "정면 2개월"},
            {"src": src('346'), "image": D + "202008291121352037577276.jpg", "caption": "콧구멍 위쪽 꺼진 부위가", "label": "아래쪽 2개월"},
            {"src": src('346'), "image": D + "202008291121501881566855.jpg", "caption": "우사면 전후사진입니다.", "label": "우사면"},
            {"src": src('346'), "image": D + "2020082911220125980000.jpg", "caption": "우사면 다른각도", "label": "우사면 다른 각도"},
            {"src": src('346'), "image": D + "20200829112210174957821.jpg", "caption": "우측면 전후사진", "label": "우측면"},
            {"src": src('346'), "image": D + "2020082911221847435620.jpg", "caption": "좌사면 전후사진", "label": "좌사면"},
            {"src": src('346'), "image": D + "20200829112238941860374.jpg", "caption": "좌측면 전후사진", "label": "좌측면"},
            {"src": src('346'), "image": D + "20200829112247856830689.jpg", "caption": "실내조명에서 정면 전후사진입니다.", "label": "실내조명 정면"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('16'), "tag": "종합 설명"},
            {"src": src('74'), "tag": "옆라인의 디자인"},
            {"src": src('346'), "tag": "비주 말린 코끝"},
            {"src": src('470'), "tag": "들창코 재수술"},
            {"src": src('584'), "tag": "첫 코수술과 함께"},
        ]
    },
    "faq": [
        {"q": "고양이 수술은 어떤 수술인가요?", "a": seg('74', (8, 10)), "src": src('74')},
        {"q": "수술은 어디로 하나요?", "a": seg('16', 9), "src": src('16')},
        {"q": "비주 말린 코끝은 고양이 수술만 하면 되나요?", "a": seg('346', (63, 66)), "src": src('346')},
        {"q": "코성형과 함께 하면 어떤 변화가 있나요?", "a": seg('16', (32, 33)), "src": src('16')},
        {"q": "필요한 수술을 다 해야 하나요?", "a": seg('346', (85, 88)), "src": src('346')},
    ],
    "related": [
        {"href": "nose/columella", "name": "비주성형"},
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nose/rib-cartilage", "name": "늑연골 코성형"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/long", "name": "긴코"},
    ],
    "review_banner_subject": "고양이 수술",
    "cases_visible": 9
}
write(data, 'nose-cat')
