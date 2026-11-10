"""data/landing/cheekbone-fat-graft.json 생성 (관자·심부볼 지방이식 대표페이지).
옛 글 4편(91·184·530·554) 중 1인칭 칼럼 줄 범위만 그대로 이어붙인다.
91 의 홍보성 문장(수술 이름을 지은 경위·다른 병원 언급·'새로운 개념의 수술법' 등)은 쓰지 않는다.
사용: python tools/landing_src/cheekbone-fat-graft.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _thin import make, write
seg, src, cut, raw = make('cheekbone/fat-graft')
D = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(관자·심부볼 지방이식). 원장님 글은 1인칭 칼럼 원문 그대로만 사용. 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "cheekbone/fat-graft",
    "seo": {
        "apply": True,
        "title": "관자·심부볼 지방이식 | 광대가 튀어나와 보일 때 · 관자 필러·보형물 비교 | 로코코성형외과 김상호 원장",
        "description": "관자와 볼이 꺼져 광대가 더 튀어나와 보일 때 관자·심부볼 지방이식은 어떤 수술인지, 관자 필러·보형물과 무엇이 다른지, 지방터치와 회복을 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "관자·심부볼 지방이식",
        "procedure_name": "관자·심부볼 지방이식"
    },
    "hero": {
        "eyebrow": "TEMPLE · DEEP CHEEK FAT GRAFT · 관자·심부볼 지방이식",
        "question": "관자·심부볼 지방이식은 어떤 수술인가요?",
        "summary": {"text": seg('554', (18, 21)), "src": src('554')},
        "stats": [
            {"to": 3, "unit": "곳", "label": "광대가 더 튀어나와 보이게 하는 주변 구조물", "quote": seg('91', (28, 31)), "src": src('91')},
            {"to": 2, "unit": "회", "label": "관자 미세지방이식 시술 횟수 (한달 반~두달 간격)", "quote": seg('91', 178), "src": src('91')},
            {"to": 2, "unit": "개월", "label": "광대축소술 부위 얼굴폭이 계속 줄어드는 기간", "quote": seg('91', (181, 182)), "src": src('91')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('530'), "image": D + "202403141059141162074406.jpg",
                 "alt": "광대축소술과 지방이식 전후 사진", "label": "CASE · 정면 2주", "layout": "stack"}
    },
    "features": {
        "type": "TYPE · CHEEKBONE",
        "toc": "광대가 더 나와 보이는 이유",
        "title": seg('91', (28, 31)),
        "items": [seg('91', (32, 33)), seg('91', (34, 36)), seg('91', (79, 80))],
        "note": seg('91', (39, 41)),
        "src": src('91')
    },
    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "하관 볼륨이 적으면 광대가 더 튀어나와 보입니다", "paras": [seg('91', (63, 72))], "src": src('91')},
            {"heading": "관자 지방이식은 근육 안에 합니다", "paras": [seg('554', (39, 43))], "src": src('554')},
            {"heading": "관자 지방이식하면 다 빠진다는 말", "paras": [seg('554', (22, 31))], "src": src('554')},
            {"heading": "남자 광대축소술은 이렇게 다릅니다", "paras": [seg('530', (9, 13))], "src": src('530')},
        ]
    },
    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('554', (39, 41)), "icon": "graft"},
            {"text": seg('554', (20, 21)), "icon": "fill"},
            {"text": seg('554', (42, 43)), "icon": "tip"},
        ],
        "steps_src": src('554'),
        "note": {"text": seg('554', (50, 51)), "src": src('554')},
        "pros_cons": {"paras": [seg('554', (32, 38)), seg('554', (44, 49))], "src": src('554')}
    },
    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 후 2주", "lines": [seg('91', (135, 139))], "src": src('91')},
            {"label": "1.5~2개월 · 지방터치", "lines": [seg('91', (14, 15))], "src": src('91')},
            {"label": "2개월", "lines": [seg('91', (181, 182))], "src": src('91')},
            {"label": "남자의 경우", "lines": [seg('530', 13)], "src": src('530')},
        ],
        "note": {"text": seg('91', (177, 178)), "src": src('91')}
    },
    "before_after": {
        "title": "광대축소술 + 지방이식 전후",
        "alt": "광대축소술과 지방이식 전후 사진",
        "items": [
            {"src": src('530'), "image": D + "202403141059141162074406.jpg", "caption": seg('530', 18), "label": "정면 2주"},
            {"src": src('530'), "image": D + "202403141100391135265311.jpg", "caption": seg('530', 26), "label": "우측광대 정면 2주"},
            {"src": src('91'), "image": D + "20150924218025075.jpg", "caption": seg('91', 16), "label": "정면 2개월 (지방터치 전)"},
            {"src": src('91'), "image": D + "201509241552390460.jpg", "caption": seg('91', 18), "label": "아래쪽 2개월"},
            {"src": src('91'), "image": D + "1383904836.jpg", "caption": seg('91', 48), "label": "관자 지방이식"},
            {"src": src('91'), "image": D + "1383959416.jpg", "caption": seg('91', 89), "label": "심부볼 지방이식"},
            {"src": src('91'), "image": D + "1383961190.jpg", "caption": seg('91', 122), "label": "광대 + 심부볼 지방이식"},
            {"src": src('184'), "image": D + "1340352124.jpg", "caption": seg('184', 8), "label": "광대돌출이 심한 경우"},
        ]
    },
    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('91'), "tag": "광대축소술 + 미세지방이식"},
            {"src": src('554'), "tag": "관자 보형물 제거"},
            {"src": src('530'), "tag": "남자의 광대축소술"},
            {"src": src('184'), "tag": "광대돌출이 심한 경우"},
        ]
    },
    "faq": [
        {"q": "관자에 지방이식하면 다 빠진다던데요?", "a": seg('554', (22, 31)), "src": src('554')},
        {"q": "관자에 필러나 보형물을 넣어도 되나요?", "a": seg('554', (32, 38)), "src": src('554')},
        {"q": "관자 지방이식을 하면 머리가 커 보이나요?", "a": seg('554', (44, 49)), "src": src('554')},
        {"q": "광대축소술만 하면 부족한 경우는 어떤 경우인가요?", "a": seg('91', (79, 80)), "src": src('91')},
        {"q": "볼에 지방이식을 과하게 하면 어떻게 되나요?", "a": seg('91', (124, 127)), "src": src('91')},
    ],
    "related": [
        {"href": "cheekbone/quick", "name": "퀵광대(15분 광대축소술)"},
        {"href": "cheekbone/liposuction", "name": "광대라인 지방흡입"},
        {"href": "cheekbone/rear", "name": "후광대 축소술"},
        {"href": "anti-aging/fat-graft", "name": "미세지방이식"},
        {"href": "forehead/endoscopic", "name": "내시경 이마거상술"},
        {"href": "eye/fat-graft", "name": "꺼진눈 지방이식"},
    ],
    "review_banner_subject": "관자·심부볼 지방이식",
    "cases_visible": 9
}
write(data, 'cheekbone-fat-graft')
