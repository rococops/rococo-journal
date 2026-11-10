"""data/landing/eye-lower-fat.json 생성 (눈밑지방 재배치 대표페이지).
옛 글 5편(27·191·198·252·330) 중 27·330 의 1인칭 칼럼 줄 범위만 그대로 이어붙인다(191·198·252 는 대표 사례 링크).
27 의 '흉터가 남지 않는' 절대 표현 문장(19·104~105·172·185행)은 쓰지 않는다.
사용: python tools/landing_src/eye-lower-fat.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('eye/lower-fat')
D = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(눈밑지방 재배치). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "eye/lower-fat",
    "seo": {
        "apply": True,
        "title": "눈밑지방 재배치 | 눈밑 불룩한 지방과 다크서클 · 재발과 한계 · 전후사진 | 로코코성형외과 김상호 원장",
        "description": "눈밑이 불룩하고 그림자가 져 피곤해 보일 때 눈밑지방 재배치는 어떤 수술인지, 수술로 고쳐지지 않는 다크서클과 재발을 줄이는 방법을 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "눈밑지방 재배치",
        "procedure_name": "눈밑지방 재배치"
    },
    "hero": {
        "eyebrow": "LOWER EYELID FAT · 눈밑지방 재배치",
        "question": "눈밑지방 재배치는 어떤 수술인가요?",
        "summary": {"text": seg('27', (3, 9)), "src": src('27')},
        "stats": [
            {"to": 15, "unit": "분", "label": "수술 시간", "quote": seg('27', 21), "src": src('27')},
            {"to": 3, "unit": "일", "label": "회복 기간", "quote": seg('27', 22), "src": src('27')},
            {"from": 3, "to": 5, "unit": "일", "label": "눈에 띄는 붓기·멍이 거의 사라지는 기간 (멍이 잘 드는 체질이 아닌 경우)", "quote": seg('27', 186), "src": src('27')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('27'), "image": D + "1306069757.jpg",
                 "alt": "눈밑지방이동술 전후 사진", "label": "CASE · 수술 전후", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · DARK CIRCLE",
        "toc": "다크서클의 네 가지 원인",
        "title": seg('27', (118, 120)),
        "items": [raw('27', 122, 123), raw('27', 124, 124), raw('27', 126, 128), raw('27', 129, 130)],
        "note": seg('27', (195, 196)),
        "src": src('27')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "눈 아래에는 그림자가 두 개 있습니다", "paras": [seg('27', (3, 9))], "src": src('27')},
            {"heading": "지방을 없애지 않고 옮깁니다", "paras": [seg('27', (10, 15))], "src": src('27')},
            {"heading": "재발을 줄이려면", "paras": [seg('330', (62, 73))], "src": src('330')},
            {"heading": "수술로 고쳐지지 않는 다크서클", "paras": [raw('27', 121, 125)], "src": src('27')},
        ]
    },
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('27', 20), "icon": "sleep"},
            {"text": seg('27', (49, 51)), "icon": "graft"},
            {"text": seg('27', (52, 53)), "icon": "tape"},
            {"text": seg('27', (54, 55)), "icon": "fill"},
        ],
        "steps_src": src('27'),
        "note": {"text": seg('27', (173, 176)), "src": src('27')},
        "pros_cons": {"paras": [seg('27', (59, 63)), seg('27', (206, 208))], "src": src('27')}
    },
    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 후 3일", "lines": [seg('27', (22, 23))], "src": src('27')},
            {"label": "3~5일", "lines": [seg('27', 186)], "src": src('27')},
            {"label": "2개월 반 (이마거상술 병행 사례)", "lines": [seg('27', (71, 72))], "src": src('27')},
        ],
        "note": {"text": seg('330', (74, 75)), "src": src('330')}
    },
    "before_after": {
        "title": "눈밑지방 재배치 전후",
        "alt": "눈밑지방 재배치 전후 사진",
        "items": [
            {"src": src('27'), "image": D + "20170221922805267.jpg", "caption": "이마거상술 눈밑지방재배치 전후사진 입니다.", "label": "이마거상술 병행 2개월 반"},
            {"src": src('27'), "image": D + "201702211365792500.jpg", "caption": "우사면 사진", "label": "우사면"},
            {"src": src('27'), "image": D + "201702211547317118.jpg", "label": "좌사면"},
            {"src": src('27'), "image": D + "1306069757.jpg", "caption": "눈밑지방이동술 수술전후 결과입니다.", "label": "수술 전후"},
            {"src": src('27'), "image": D + "1306069848.jpg", "caption": "아주 살짝 지방이 나온 눈이지만", "label": "지방이 살짝 나온 눈"},
            {"src": src('252'), "image": D + "201706191187305963.jpg", "caption": "눈밑지방이동술 비절개눈매교정 수술전후 5주째 사진입니다", "label": "5주 (눈매교정 병행)"},
            {"src": src('252'), "image": D + "20170619327985530.jpg", "caption": "실내조명에서 수술 후 3개월2주째 전후사진입니다.", "label": "3개월 2주 (눈매교정 병행)"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('27'), "tag": "종합 설명"},
            {"src": src('330'), "tag": "재발을 줄이는 방식"},
            {"src": src('191'), "tag": "이마거상술 동시수술"},
            {"src": src('198'), "tag": "이마거상술 병행"},
            {"src": src('252'), "tag": "눈위·눈밑 동시"},
        ]
    },
    "faq": [
        {"q": "눈밑지방 재배치는 어떻게 하나요?", "a": seg('27', (49, 53)), "src": src('27')},
        {"q": "수술 후에 다시 튀어나올 수 있나요?", "a": seg('330', (69, 73)), "src": src('330')},
        {"q": "눈밑 피부가 처졌다면 같은 수술로 되나요?", "a": seg('27', (59, 63)), "src": src('27')},
        {"q": "눈 아래에 지방이식을 같이 하면 어떤가요?", "a": seg('27', (182, 183)), "src": src('27')},
        {"q": "눈밑 피부 아래에 지방이식을 하는 것은 어떤가요?", "a": seg('27', (138, 145)), "src": src('27')},
    ],
    "related": [
        {"href": "eye/fat-graft", "name": "꺼진눈 지방이식"},
        {"href": "anti-aging/blepharoplasty", "name": "상·하안검성형"},
        {"href": "anti-aging/fat-graft", "name": "미세지방이식"},
        {"href": "forehead/endoscopic", "name": "내시경 이마거상술"},
        {"href": "eye/correction", "name": "눈매교정"},
        {"href": "eye/brow-lift", "name": "눈썹하거상술"},
    ],
    "review_banner_subject": "눈밑지방 재배치",
    "cases_visible": 9
}
write(data, 'eye-lower-fat')
