"""data/landing/anti-aging-fat-graft.json 생성 (리포킷 미세지방이식 대표페이지).
옛 글 7편(31·119·234·254·419·520·615) 중 31(3~33행만, 이후는 코 연골 글이라 제외)·419·520 의 1인칭 칼럼 줄 범위만 그대로 이어붙인다.
119(아큐스컬프)·615(이중턱 지방흡입)는 지방이식이 아니라 제외, 234 는 대표 사례 링크.
사용: python tools/landing_src/anti-aging-fat-graft.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('anti-aging/fat-graft')
D = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(리포킷 미세지방이식). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "anti-aging/fat-graft",
    "seo": {
        "apply": True,
        "title": "리포킷 미세지방이식 | 자가혈 지방이식 · 생착과 부작용 · 흘러내림 | 로코코성형외과 김상호 원장",
        "description": "얼굴 지방이식은 지방을 어떻게 채취하고 이식하느냐에 따라 달라집니다. 리포킷 자가혈 미세지방이식, 지방이 흘러내린다는 말의 진실, 이마·미간 지방이식의 한계를 김상호 원장의 글로 정리했습니다.",
        "h1": "리포킷 미세지방이식",
        "procedure_name": "리포킷 미세지방이식"
    },
    "hero": {
        "eyebrow": "MICRO FAT GRAFT · 리포킷 미세지방이식",
        "question": "리포킷 미세지방이식은 어떤 수술인가요?",
        "summary": {"text": seg('31', (3, 5)), "src": src('31')},
        "stats": [
            {"from": 30, "to": 60, "unit": "분", "label": "수술 시간", "quote": seg('31', 31), "src": src('31')},
            {"to": 3, "unit": "일", "label": "회복 기간", "quote": seg('31', 32), "src": src('31')},
            {"to": 2, "unit": "가지", "label": "지방이식에서 중요한 것 (디자인·생착률)", "quote": raw('419', 36, 38), "src": src('419')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('520'), "image": D + "202403071308502054754296.jpg",
                 "alt": "미간 지방이식 전후 사진", "label": "CASE · 미간 지방이식", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · GRAFT SURVIVAL",
        "toc": "이식한 지방이 죽는 경우",
        "title": seg('419', (27, 28)),
        "items": [seg('419', (29, 30)), seg('419', (31, 35)), seg('419', (59, 64))],
        "note": raw('419', 36, 40),
        "src": src('419')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "지방이식이란 무엇인가", "paras": [seg('419', (16, 20))], "src": src('419')},
            {"heading": "지방은 채취가 더 중요합니다", "paras": [seg('31', (6, 17))], "src": src('31')},
            {"heading": "자가혈을 함께 씁니다", "paras": [seg('31', (25, 29))], "src": src('31')},
            {"heading": "줄기세포 지방이식은 그만두었습니다", "paras": [seg('31', (21, 24))], "src": src('31')},
        ]
    },
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('31', 30), "icon": "sleep"},
            {"text": seg('31', 31), "icon": "clock"},
            {"text": seg('31', (14, 17)), "icon": "tip"},
            {"text": seg('31', (25, 27)), "icon": "fill"},
            {"text": seg('31', 33), "icon": "tape"},
        ],
        "steps_src": src('31'),
        "note": {"text": seg('31', (18, 20)), "src": src('31')},
        "pros_cons": {"paras": [seg('419', (69, 73))], "src": src('419')}
    },
    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 다음날", "lines": [seg('31', 33)], "src": src('31')},
            {"label": "3일", "lines": [seg('31', 32)], "src": src('31')},
            {"label": "지방이 자리를 잡은 뒤", "lines": [seg('31', (75, 76))], "src": src('31')},
        ],
        "note": {"text": seg('419', (22, 26)), "src": src('419')}
    },
    "before_after": {
        "title": "지방이식 전후",
        "alt": "지방이식 전후 사진",
        "items": [
            {"src": src('520'), "image": D + "202403071308502054754296.jpg", "caption": seg('520', 40), "label": "미간 지방이식 · 정면"},
            {"src": src('520'), "image": D + "202403071308571011570767.jpg", "label": "미간 지방이식 · 코재수술"},
            {"src": src('520'), "image": D + "202403071309091812924449.jpg", "label": "미간 지방이식 · 다른 각도"},
            {"src": src('520'), "image": D + "20240307130919635755695.jpg", "caption": seg('520', 46), "label": "우사면"},
            {"src": src('520'), "image": D + "20240307130941901788619.jpg", "caption": seg('520', 47), "label": "미간 지방이식 · 디자인 변경"},
            {"src": src('254'), "image": D + "20170619234733802.jpg", "caption": "수술전과 수술후 5주째 사진입니다.", "label": "꺼진눈 지방이식 5주"},
            {"src": src('254'), "image": D + "20170619327985530.jpg", "caption": "실내조명에서 수술 후 3개월2주째 전후사진입니다.", "label": "꺼진눈 지방이식 3개월 2주"},
            {"src": src('31'), "image": D + "1319161895.jpg", "caption": seg('31', 74), "label": "이마 지방이식 병행 코성형"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('31'), "tag": "리포킷 자가혈 지방이식"},
            {"src": src('419'), "tag": "지방이 흘러내리나요"},
            {"src": src('520'), "tag": "미간 지방이식"},
            {"src": src('254'), "tag": "꺼진눈·애교볼·팔자 지방이식"},
            {"src": src('234'), "tag": "이마 지방이식 병행"},
        ]
    },
    "faq": [
        {"q": "지방이식을 하면 지방이 아래로 흘러내리나요?", "a": seg('419', (75, 81)), "src": src('419')},
        {"q": "리포킷은 왜 쓰나요?", "a": seg('31', (14, 17)), "src": src('31')},
        {"q": "자가혈 지방이식은 무엇인가요?", "a": seg('31', (25, 29)), "src": src('31')},
        {"q": "미간 지방이식은 단독으로 하나요?", "a": seg('520', (27, 31)), "src": src('520')},
        {"q": "이마 지방이식에서 생길 수 있는 문제는 무엇인가요?", "a": seg('419', (59, 64), (69, 73)), "src": src('419')},
    ],
    "related": [
        {"href": "eye/fat-graft", "name": "꺼진눈 지방이식"},
        {"href": "cheekbone/fat-graft", "name": "심부볼·관자 지방이식"},
        {"href": "eye/lower-fat", "name": "눈밑지방 재배치"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "anti-aging/filler-botox", "name": "필러·보톡스"},
        {"href": "anti-aging/lifting", "name": "엘라스티꿈 실리프팅"},
    ],
    "review_banner_subject": "리포킷 미세지방이식",
    "cases_visible": 9
}
write(data, 'anti-aging-fat-graft')
