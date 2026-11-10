"""data/landing/nostril-reduction.json 생성 (콧구멍축소술 대표페이지).
옛 글 6편(51·c124·170·267·406·623) 중 51·170·267·406·623 의 1인칭 칼럼 줄 범위만 그대로 이어붙인다.
(267 의 사진은 v2.rococops.com 이라 쓰지 않음)
사용: python tools/landing_src/nostril-reduction.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('nostril/reduction')
D = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(콧구멍축소술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nostril/reduction",
    "seo": {
        "apply": True,
        "title": "콧구멍축소술 | 콧구멍이 크고 많이 보일 때 · 흉터와 호흡 · 전후사진 | 로코코성형외과 김상호 원장",
        "description": "콧구멍이 크거나 많이 보여 고민일 때 콧구멍축소술은 어떤 수술인지, 되돌릴 수 없다는 점과 흉터·호흡 문제, 콧날개올리기와 함께 하는 경우를 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "콧구멍축소술",
        "procedure_name": "콧구멍축소술"
    },
    "hero": {
        "eyebrow": "NOSTRIL REDUCTION · 콧구멍축소술",
        "question": "콧구멍축소술은 어떤 수술인가요?",
        "summary": {"text": seg('51', (7, 9)), "src": src('51')},
        "stats": [
            {"from": 30, "to": 40, "unit": "분", "label": "수술 시간 (콧날개+콧구멍 줄이기, V콧구멍교정 병행)", "quote": seg('170', 27), "src": src('170')},
            {"from": 6, "to": 12, "unit": "개월", "label": "흉터가 연한 선으로 가라앉는 기간 (콧볼축소 병행)", "quote": seg('267', (33, 34)), "src": src('267')},
            {"to": 1, "unit": "년", "label": "콧구멍 아래 흉터가 계속 흐려지는 기간", "quote": seg('406', 104), "src": src('406')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('406'), "image": D + "202203081238181944144824.jpg",
                 "alt": "콧구멍축소술·콧날개올리기 전후 사진", "label": "CASE · 정면 10일", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · NOSTRIL",
        "toc": "콧구멍이 보이는 네 가지 원인",
        "title": seg('406', 10),
        "items": [seg('406', 11), seg('406', 12), seg('406', 13), seg('406', 14)],
        "note": seg('406', (16, 20)),
        "src": src('406')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "콧구멍이 보일 때 해결 방법", "paras": [raw('406', 21, 27)], "src": src('406')},
            {"heading": "콧구멍은 약간 아쉬운 정도로 줄입니다", "paras": [seg('267', (19, 22))], "src": src('267')},
            {"heading": "이런 콧볼·콧구멍에 잘 맞습니다", "paras": [seg('267', (7, 9), 11, (16, 18))], "src": src('267')},
            {"heading": "비공내리기 대신 콧구멍축소술을 한 경우", "paras": [raw('406', 61, 71)], "src": src('406')},
        ]
    },
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": raw('406', 63, 65), "icon": "tip"},
            {"text": seg('406', (78, 82)), "icon": "fill"},
            {"text": seg('406', (114, 116)), "icon": "deviation"},
        ],
        "steps_src": src('406'),
        "note": {"text": seg('170', (37, 38), (45, 49)), "src": src('170')},
        "pros_cons": {"paras": [seg('406', (83, 84)), seg('406', (87, 91))], "src": src('406')}
    },
    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 후 10일", "lines": [seg('406', (92, 94))], "src": src('406')},
            {"label": "6~12개월", "lines": [seg('267', (33, 34))], "src": src('267')},
            {"label": "1년", "lines": [seg('406', (103, 104))], "src": src('406')},
            {"label": "흉터가 볼록해진 경우", "lines": [seg('406', (95, 100))], "src": src('406')},
        ],
        "note": {"text": seg('406', (85, 86)), "src": src('406')}
    },
    "before_after": {
        "title": "콧구멍축소술 전후",
        "alt": "콧구멍축소술 전후 사진",
        "items": [
            {"src": src('406'), "image": D + "202203081238181944144824.jpg", "caption": "수술전과 수술 후 10일째 사진입니다.", "label": "정면 10일"},
            {"src": src('406'), "image": D + "202203081238371500016224.jpg", "caption": "우사면 전후사진입니다.", "label": "우사면"},
            {"src": src('406'), "image": D + "20220308123843905245282.jpg", "caption": "우측면 전후사진입니다.", "label": "우측면"},
            {"src": src('406'), "image": D + "2022030812384926439817.jpg", "caption": "좌사면 전후사진입니다.", "label": "좌사면"},
            {"src": src('406'), "image": D + "20220308123856480014240.jpg", "caption": "좌측면 전후사진입니다.", "label": "좌측면"},
            {"src": src('406'), "image": D + "202203081239031222083649.jpg", "caption": "실내조명에서 전후사진입니다.", "label": "실내조명 정면"},
            {"src": src('170'), "image": D + "201703031275713663.jpg", "caption": "수술 전과 수술 후 일주일째 실밥제거하고 찍은 사진입니다.", "label": "정면 1주"},
            {"src": src('170'), "image": D + "201703031498835119.jpg", "caption": "아래쪽에서 본 전후사진입니다.", "label": "아래쪽 1주"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('51'), "tag": "콧날개 줄이는 세 가지 방법"},
            {"src": src('170'), "tag": "콧날개·콧구멍 줄이기 + V콧구멍"},
            {"src": src('267'), "tag": "콧볼축소술 병행"},
            {"src": src('406'), "tag": "콧구멍 가리기"},
            {"src": src('623'), "tag": "비주 말린 코 + 콧구멍·콧볼축소"},
        ]
    },
    "faq": [
        {"q": "콧구멍이 많이 보이는 원인은 무엇인가요?", "a": raw('406', 10, 15), "src": src('406')},
        {"q": "콧구멍을 줄이면 숨쉬기가 불편해질 수 있나요?", "a": seg('170', (45, 49)), "src": src('170')},
        {"q": "콧구멍축소술은 되돌릴 수 있나요?", "a": seg('406', (87, 91)), "src": src('406')},
        {"q": "콧구멍축소술 흉터는 눈에 띄나요?", "a": seg('406', (83, 86)), "src": src('406')},
        {"q": "콧날개를 줄이는 수술에는 어떤 방법이 있나요?", "a": seg('51', (7, 9)), "src": src('51')},
    ],
    "related": [
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nostril/v-shape", "name": "V형 콧구멍교정"},
        {"href": "nostril/alar-base", "name": "콧볼축소술"},
        {"href": "nose/bulbous", "name": "복코"},
        {"href": "nose/columella", "name": "비주성형"},
    ],
    "review_banner_subject": "콧구멍축소술",
    "cases_visible": 9
}
write(data, 'nostril-reduction')
