"""data/landing/anti-aging-chin.json 생성 (무턱수술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/anti-aging-chin.py   →  data/landing/anti-aging-chin.json

참고: 30번 칼럼은 옛 글 여러 편(2017·2016·2015·2014·2011)이 날짜 줄로 이어 붙은 페이지다. 235번 줄 이후 2011.06.12 글은 이마 보형물 글이라 쓰지 않는다.
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'anti-aging/chin/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


# 수술 단계 아이콘(이 페이지 전용, 120x120 안의 요소)
ICONS = {
    # 입안(아랫입술 안쪽) 작은 절개
    "mouth": '<path d="M18 44 C40 30 80 30 102 44 C84 54 36 54 18 44 Z" fill="#e3a596" stroke="#4a4a4a" stroke-width="2.2"/>'
             '<path d="M20 58 C36 100 84 100 100 58 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
             '<path d="M28 60 C42 78 78 78 92 60 Z" fill="#f2bdb6" stroke="none"/>'
             '<path d="M50 70 L70 70" stroke="#c46a5a" stroke-width="3.4" stroke-linecap="round"/>',
    # 옆에서 본 턱끝: 뼈(골막) 위에 놓이는 보형물
    "implant": '<path d="M34 12 C40 30 46 40 50 50 C44 54 44 60 50 64 C46 70 48 78 56 82 C62 92 72 102 92 106 L112 106 L112 12 Z" fill="#f1cfb8" stroke="none"/>'
               '<path d="M34 12 C40 30 46 40 50 50 C44 54 44 60 50 64 C46 70 48 78 56 82 C62 92 72 102 92 106" fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
               '<path d="M74 66 C66 76 68 92 82 100" fill="none" stroke="#d8cdbd" stroke-width="6" stroke-linecap="round"/>'
               '<path d="M66 70 C56 80 58 96 72 102 C68 92 68 80 72 72 Z" fill="#c9a26f" stroke="#a9834f" stroke-width="1.8" stroke-linejoin="round"/>',
    # 정면에서 본 보형물 양쪽 날개와 골막 아래 포켓
    "wing": '<path d="M14 26 C18 70 40 102 60 102 C80 102 102 70 106 26" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
            '<path d="M24 70 C38 96 82 96 96 70 C84 80 36 80 24 70 Z" fill="#c9a26f" stroke="#a9834f" stroke-width="1.8" stroke-linejoin="round"/>'
            '<path d="M16 62 L28 76 M104 62 L92 76" stroke="#c46a5a" stroke-width="2" stroke-dasharray="3 3" stroke-linecap="round"/>',
    # 스크류 없이 고정
    "fix": '<path d="M14 26 C18 70 40 102 60 102 C80 102 102 70 106 26" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
           '<path d="M24 70 C38 96 82 96 96 70 C84 80 36 80 24 70 Z" fill="#c9a26f" stroke="#a9834f" stroke-width="1.8" stroke-linejoin="round"/>'
           '<circle cx="86" cy="34" r="14" fill="#c9a26f" stroke="#a9834f" stroke-width="1.8"/>'
           '<path d="M79 34 L84 39 L93 28" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>',
}

data = {
    "_comment": "시술별 대표페이지 데이터(무턱수술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "anti-aging/chin",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "무턱수술 | 입안 작은 절개 실리콘 보형물, 돌출입처럼 보이는 입매와 얼굴 밸런스 | 로코코성형외과 김상호 원장",
        "description": "무턱은 턱끝이 충분히 앞으로 나오지 못하고 뒤에 있는 상태로, 입이 튀어나와 보이고 얼굴 밸런스가 깨져 보이게 합니다. 수면마취·입안 절개로 하는 무턱수술의 방법, 보형물 고정, 회복과 전후사진을 김상호 원장의 글로 정리했습니다.",
        "h1": "무턱수술",
        "procedure_name": "무턱수술"
    },

    "hero": {
        "eyebrow": "CHIN AUGMENTATION · 무턱수술",
        "question": "무턱수술은 어떻게 하나요?",
        "summary": {"text": seg('368', (9, 14)), "src": src('368')},
        "stats": [
            {"to": 5, "unit": "분", "label": "수술 시간 (수면마취)",
             "quote": seg('560', (12, 13)), "src": src('560')},
            {"from": 3, "to": 5, "unit": "일", "label": "회복기간 (대부분의 경우)",
             "quote": seg('30', 162), "src": src('30')},
            {"to": 1000, "unit": "건 이상", "label": "무턱교정 시술 (2011년 글 기준)",
             "quote": seg('30', 331), "src": src('30')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('368'), "image": "https://rococops.com/files/editor/202103021018191424691391.jpg",
                 "alt": "무턱수술 전후 측면 사진", "label": "CASE · 측면 3주", "layout": "stack"}
    },

    "features": {
        "type": "SIGNS · CHIN",
        "toc": "무턱의 단점",
        "title": seg('30', 288),
        "items": [seg('30', i) for i in range(142, 145)],
        "note": seg('30', (148, 149)),
        "src": src('30')
    },

    "icons": ICONS,

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "이마, 코끝, 턱끝이 조화를 이뤄야 합니다",
             "paras": [seg('560', (5, 6)), seg('560', (7, 11)), seg('560', (12, 19))], "src": src('560')},
            {"heading": "매부리코와 무턱은 많이 동반됩니다",
             "paras": [seg('568', (5, 9)), seg('568', (16, 18)), seg('568', (19, 23))], "src": src('568')},
            {"heading": "코성형에서 무턱수술을 같이 권하는 이유",
             "paras": [seg('363', (51, 54)), seg('363', (55, 61))], "src": src('363')},
            {"heading": "무턱과 왜소턱",
             "paras": [seg('30', (103, 107)), seg('30', (108, 111))], "src": src('30')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('368', 37), "icon": "sleep"},
            {"text": seg('368', (38, 39)).rstrip(','), "icon": "mouth"},
            {"text": seg('368', 40), "icon": "implant"},
            {"text": seg('368', 41), "icon": "wing"},
            {"text": seg('368', (42, 43)), "icon": "fix"},
        ],
        "steps_src": src('368'),
        "note": {"text": seg('368', (52, 55)), "src": src('368')},
        "pros_cons": {"paras": [seg('30', (81, 83)), seg('30', (86, 91))], "src": src('30')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('30', 302)], "src": src('30')},
            {"label": "실밥", "lines": [seg('568', 46)], "src": src('568')},
            {"label": "3일째", "lines": [seg('30', 19)], "src": src('30')},
            {"label": "3~5일", "lines": [seg('30', 162)], "src": src('30')},
            {"label": "1주", "lines": [seg('568', (44, 45))], "src": src('568')},
        ],
        "note": {"text": seg('30', (163, 165)), "src": src('30')}
    },

    "before_after": {
        "title": "무턱수술 전후",
        "alt": "무턱수술 전후 사진",
        "items": [
            {"src": src('368'), "image": "https://rococops.com/files/editor/20210302101724635508794.jpg",
             "caption": "수술 전후 3주째 사진입니다.", "label": "정면 3주"},
            {"src": src('368'), "image": "https://rococops.com/files/editor/20210302101735223400442.jpg",
             "caption": "아래쪽에서 본 전후사진.", "label": "아래쪽에서 3주"},
            {"src": src('368'), "image": "https://rococops.com/files/editor/202103021017541949272652.jpg",
             "caption": "우측면 전후사진", "label": "측면 3주"},
            {"src": src('568'), "image": "https://rococops.com/files/editor/20240621131645397734268.jpg",
             "caption": "정면 수술 전과 수술 후 1주일 사진입니다.", "label": "정면 1주"},
            {"src": src('568'), "image": "https://rococops.com/files/editor/202406211317591509159475.jpg",
             "caption": "수술 후 일주일 전후사진입니다.", "label": "측면 1주"},
            {"src": src('30'), "image": "https://rococops.com/files/editor/20160321250075307.jpg",
             "caption": "우측면 사진을 보면 상당히 무턱이 심하신 분입니다", "label": "심한 무턱 측면 2주"},
            {"src": src('30'), "image": "https://rococops.com/files/editor/1397708620.jpg",
             "caption": "우측면사진입니다.", "label": "측면"},
            {"src": src('363'), "image": "https://rococops.com/files/editor/20210111151914213803877.jpg",
             "caption": "좌측면 들창코수술 무턱수술 전후사진입니다.", "label": "들창코수술 + 무턱수술 측면"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('568'), "tag": "매부리코와 무턱"},
            {"src": src('560'), "tag": "무턱 총정리"},
            {"src": src('368'), "tag": "수술법·3주 전후"},
            {"src": src('30'), "tag": "무턱 교정 기록 모음"},
            {"src": src('363'), "tag": "코성형 + 무턱"},
            {"src": src('269'), "tag": "코재수술 + 무턱"},
        ]
    },

    "faq": [
        {"q": "무턱수술을 하면 턱이 길어 보이지 않나요?", "a": seg('368', (46, 51)), "src": src('368')},
        {"q": "턱을 만지면 보형물이 있는 게 느껴지나요?", "a": seg('368', (58, 60)), "src": src('368')},
        {"q": "무턱수술만으로 돌출입처럼 보이는 입매가 달라지나요?", "a": seg('568', (57, 59)), "src": src('568')},
        {"q": "필러나 지방이식으로 무턱을 채우면 안 되나요?", "a": seg('30', (202, 205)), "src": src('30')},
        {"q": "보형물에 염증이 생기지는 않나요?", "a": seg('30', (50, 52)), "src": src('30')},
    ],

    "related": [
        {"href": "anti-aging/fat-graft", "name": "미세지방이식"},
        {"href": "anti-aging/filler-botox", "name": "필러·보톡스"},
        {"href": "anti-aging/lifting", "name": "엘라스티꿈 실리프팅"},
        {"href": "nose/hump", "name": "매부리코 수술"},
        {"href": "cheekbone/quick", "name": "퀵광대(15분 광대축소술)"},
        {"href": "nose/revision", "name": "코재수술"},
    ],

    "review_banner_subject": "무턱수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'anti-aging-chin.json')
from _companions import companions_for  # 함께 알아두면 좋은 시술(3순위 하위 메뉴 흡수)
data['companions'] = companions_for(data['page'])
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
