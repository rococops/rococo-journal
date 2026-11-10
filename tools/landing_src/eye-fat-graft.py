"""data/landing/eye-fat-graft.json 생성 (꺼진눈 지방이식 대표페이지).
옛 글 5편(29·255·279·511·549) 중 29·255·279·549 의 1인칭 칼럼 줄 범위만 그대로 이어붙인다(511 은 대표 사례 링크).
사용: python tools/landing_src/eye-fat-graft.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('eye/fat-graft')
D = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(꺼진눈 지방이식). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "eye/fat-graft",
    "seo": {
        "apply": True,
        "title": "꺼진눈 지방이식 | 눈 위가 꺼져 피곤해 보일 때 · 단점과 회복 · 전후사진 | 로코코성형외과 김상호 원장",
        "description": "눈 위가 꺼져 피곤하고 나이 들어 보이거나 쌍커풀이 여러 겹일 때, 꺼진눈 지방이식은 어떤 수술인지 단점과 회복, 이마거상술 뒤에 꺼지는 경우를 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "꺼진눈 지방이식",
        "procedure_name": "꺼진눈 지방이식"
    },
    "hero": {
        "eyebrow": "SUNKEN EYE · 꺼진눈 지방이식",
        "question": "꺼진눈 지방이식은 어떤 수술인가요?",
        "summary": {"text": seg('29', (3, 6)), "src": src('29')},
        "stats": [
            {"to": 20, "unit": "분", "label": "수술 시간", "quote": seg('29', 8), "src": src('29')},
            {"to": 3, "unit": "일", "label": "회복 기간", "quote": seg('29', 9), "src": src('29')},
            {"to": 3, "unit": "개월", "label": "2차 지방이식(지방터치)을 고려하는 시점", "quote": seg('29', (26, 28)), "src": src('29')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('29'), "image": D + "201605281804163823.jpg",
                 "alt": "꺼진눈 지방이식 전후 사진", "label": "CASE · 1주 · 3개월", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · SUNKEN EYE",
        "toc": "꺼진 눈을 해결하는 방법",
        "title": seg('549', (5, 8)),
        "items": [raw('549', 56, 57), raw('549', 58, 59), raw('549', 60, 61), raw('549', 62, 63)],
        "note": seg('549', (49, 54)),
        "src": src('549')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "눈 위가 꺼지면 인상이 달라집니다", "paras": [seg('29', (3, 6)), seg('29', (17, 19))], "src": src('29')},
            {"heading": "쌍커풀이 여러 겹이 되는 이유", "paras": [seg('549', (44, 48))], "src": src('549')},
            {"heading": "이마거상술 뒤에 꺼질 수 있습니다", "paras": [seg('279', (12, 20))], "src": src('279')},
            {"heading": "눈 뜨는 힘이 약한 경우", "paras": [seg('29', (41, 43))], "src": src('29')},
        ]
    },
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('29', 7), "icon": "sleep"},
            {"text": seg('29', (23, 24)), "icon": "graft"},
            {"text": seg('29', 8), "icon": "clock"},
            {"text": seg('29', 10), "icon": "tape"},
        ],
        "steps_src": src('29'),
        "note": {"text": seg('29', 25), "src": src('29')},
        "pros_cons": {"paras": [raw('29', 29, 32), raw('29', 33, 40)], "src": src('29')}
    },
    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 다음날", "lines": [seg('29', 10)], "src": src('29')},
            {"label": "3일", "lines": [seg('29', 9)], "src": src('29')},
            {"label": "1주", "lines": [seg('29', (20, 21))], "src": src('29')},
            {"label": "지방이 일부 흡수된 경우", "lines": [seg('255', (62, 68))], "src": src('255')},
        ],
        "note": {"text": seg('255', (35, 36)), "src": src('255')}
    },
    "before_after": {
        "title": "꺼진눈 지방이식 전후",
        "alt": "꺼진눈 지방이식 전후 사진",
        "items": [
            {"src": src('29'), "image": D + "201605281804163823.jpg", "caption": "수술전과 수술 후 일주일, 마지막 사진은 수술 후 3개월째", "label": "1주 · 3개월"},
            {"src": src('29'), "image": D + "20160528934149801.jpg", "caption": "꺼진 눈 부위에 눈 위 지방이식을 하고 수술 후 일주일째 모습입니다", "label": "1주"},
            {"src": src('255'), "image": D + "20170619234733802.jpg", "caption": "수술전과 수술후 5주째 사진입니다.", "label": "5주"},
            {"src": src('255'), "image": D + "201706191187305963.jpg", "caption": "눈밑지방이동술 비절개눈매교정 수술전후 5주째 사진입니다", "label": "5주 실내조명"},
            {"src": src('255'), "image": D + "201706191724728939.jpg", "caption": "눈밑지방이동술과 비절개눈매교정 눈위지방이식 수술 후", "label": "3개월 2주"},
            {"src": src('255'), "image": D + "20170619327985530.jpg", "caption": "실내조명에서 수술 후 3개월2주째 전후사진입니다.", "label": "3개월 2주 실내조명"},
            {"src": src('279'), "image": D + "20190906132527427669570.jpg", "caption": "이마거상술 상태에서", "label": "이마거상술 + 지방이식 1개월"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('29'), "tag": "종합 설명"},
            {"src": src('255'), "tag": "눈밑지방재배치 병행"},
            {"src": src('279'), "tag": "이마거상술 뒤 꺼진눈"},
            {"src": src('549'), "tag": "쌍커풀이 여러 겹이 되는 이유"},
            {"src": src('511'), "tag": "꺼진눈 지방이식"},
        ]
    },
    "faq": [
        {"q": "꺼진눈 지방이식은 어떻게 하나요?", "a": seg('29', (23, 24)), "src": src('29')},
        {"q": "꺼진눈 지방이식의 단점은 무엇인가요?", "a": raw('29', 29, 32), "src": src('29')},
        {"q": "눈 뜨는 힘이 약한데 눈 위가 꺼졌다면요?", "a": seg('29', (41, 43)), "src": src('29')},
        {"q": "이식한 지방이 꺼지면 어떻게 하나요?", "a": seg('255', (62, 68)), "src": src('255')},
        {"q": "쌍커풀이 여러 겹으로 바뀌는 이유는 무엇인가요?", "a": seg('549', (44, 48)), "src": src('549')},
    ],
    "related": [
        {"href": "eye/lower-fat", "name": "눈밑지방 재배치"},
        {"href": "eye/correction", "name": "눈매교정"},
        {"href": "eye/double", "name": "쌍커풀"},
        {"href": "forehead/endoscopic", "name": "내시경 이마거상술"},
        {"href": "anti-aging/fat-graft", "name": "미세지방이식"},
        {"href": "eye/brow-lift", "name": "눈썹하거상술"},
    ],
    "review_banner_subject": "꺼진눈 지방이식",
    "cases_visible": 9
}
write(data, 'eye-fat-graft')
