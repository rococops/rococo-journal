"""data/landing/forehead-endoscopic.json 생성 (내시경 이마거상술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/forehead-endoscopic.py   →  data/landing/forehead-endoscopic.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'forehead/endoscopic/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


# 수술 방법 단계 전용 아이콘 (공용에 없는 것만, 120x120)
_HEAD = ('<path d="M22 112 C18 70 22 30 60 18 C98 30 102 70 98 112 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/>'
         '<path d="M22 70 C22 34 40 18 60 18 C80 18 98 34 98 70 C88 54 76 48 60 48 C44 48 32 54 22 70 Z" fill="#6b4a3a" fill-opacity=".8"/>')
# 두피 속 작은 절개 세 군데: 머리카락 안쪽의 붉은 짧은 선
ICON_SCALP = (_HEAD +
              '<path d="M60 26 L60 38 M38 36 L42 46 M82 36 L78 46" stroke="#e58f7c" stroke-width="3.4" stroke-linecap="round"/>'
              '<path d="M38 84 C44 80 52 80 56 83 M64 83 C68 80 76 80 82 84" fill="none" stroke="#4a4a4a" stroke-width="2.6" stroke-linecap="round"/>')
# 내시경으로 보면서 박리: 이마 아래로 들어가는 가는 관 + 끝의 빛
ICON_SCOPE = ('<path d="M14 96 C30 60 50 40 96 30 L106 30 L106 104 L14 104 Z" fill="#f1cfb8" stroke="none"/>'
              '<path d="M14 96 C30 60 50 40 96 30" fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round"/>'
              '<path d="M104 40 L46 70" stroke="#4a4a4a" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M104 40 L46 70" stroke="#b8956a" stroke-width="2" stroke-linecap="round"/>'
              '<circle cx="44" cy="71" r="5" fill="#fff6ea" stroke="#b8956a" stroke-width="1.6"/>'
              '<path d="M36 64 L30 60 M34 74 L27 76 M42 80 L40 87" stroke="#c9a26f" stroke-width="2" stroke-linecap="round"/>')
# 미간 찡그리는 근육 힘 빼기: 미간 주름(점선) + 양쪽 눈썹
ICON_GLABELLA = ('<path d="M10 58 C24 44 40 44 52 54 M68 54 C80 44 96 44 110 58" fill="none" stroke="#6b4a3a" stroke-width="5" stroke-linecap="round"/>'
                 '<path d="M56 40 L56 66 M64 40 L64 66" stroke="#c46a5a" stroke-width="2" stroke-dasharray="4 4" stroke-linecap="round"/>'
                 '<path d="M22 82 C30 76 40 76 46 82 M74 82 C80 76 90 76 98 82" fill="none" stroke="#4a4a4a" stroke-width="2.4" stroke-linecap="round"/>'
                 '<path d="M48 98 L72 98" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round"/>')
# 이마를 끌어올려 고정: 처진 눈썹(점선) → 올라간 눈썹 + 위쪽 화살표
ICON_BROWLIFT = ('<path d="M14 76 C32 66 48 68 58 76" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="4 4" stroke-linecap="round"/>'
                 '<path d="M62 76 C72 68 88 66 106 76" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="4 4" stroke-linecap="round"/>'
                 '<path d="M14 62 C32 50 48 52 58 60 M62 60 C72 52 88 50 106 62" fill="none" stroke="#6b4a3a" stroke-width="5" stroke-linecap="round"/>'
                 '<path d="M26 96 C34 90 46 90 52 96 M68 96 C74 90 86 90 94 96" fill="none" stroke="#4a4a4a" stroke-width="2.4" stroke-linecap="round"/>'
                 '<path d="M60 44 L60 14 M52 22 L60 14 L68 22" fill="none" stroke="#b8956a" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')

data = {
    "_comment": "시술별 대표페이지 데이터(내시경 이마거상술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "forehead/endoscopic",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "내시경 이마거상술 | 처진 눈썹·이마 주름, 수술 방법과 유지 기간·회복 | 로코코성형외과 김상호 원장",
        "description": "내시경 이마거상술은 두피 속 작은 절개로 눈썹을 포함한 이마 전체를 들어올려 고정하는 수술입니다. 눈썹이 내려와 생기는 변화, 수술 방법, 효과 유지 기간, 붓기·멍과 회복을 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "내시경 이마거상술",
        "procedure_name": "내시경 이마거상술"
    },

    "hero": {
        "eyebrow": "ENDOSCOPIC FOREHEAD LIFT · 내시경 이마거상술",
        "question": "내시경 이마거상술은 어떻게 수술하나요?",
        "summary": {"text": seg('543', (61, 62)), "src": src('543')},
        "stats": [
            {"to": 30, "unit": "분", "label": "수술 시간 (수면마취)",
             "quote": seg('337', (103, 104)), "src": src('337')},
            {"from": 3, "to": 5, "unit": "군데", "label": "두피 속 작은 절개 (보통 3군데 · 경우에 따라 5군데)",
             "quote": seg('195', (56, 57)), "src": src('195'),
             "extra": [{"quote": seg('337', 93), "src": src('337')}]},
            {"to": 5, "unit": "년 이상", "label": "눈썹이 올라간 효과 (대부분 최소)",
             "quote": seg('543', (79, 80)), "src": src('543')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('193'), "image": "https://rococops.com/files/editor/201706271247758434.jpg",
                 "alt": "내시경 이마거상술 전후 정면 사진", "label": "CASE · 정면 전후", "layout": "stack"}
    },

    "features": {
        "type": "SIGNS · BROW PTOSIS",
        "toc": "눈썹이 내려올 때 생기는 변화",
        "title": seg('543', 18),
        "items": [seg('543', 35).rstrip(','), seg('543', 36).rstrip(','), seg('543', 37), seg('543', (38, 40))],
        "note": seg('543', (42, 46)),
        "src": src('543')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "눈꺼풀이 처진 것이 아니라 눈썹이 내려온 것입니다",
             "paras": [seg('201', (34, 40)), seg('201', 76)], "src": src('201')},
            {"heading": "나이와 관계없이, 눈썹이 올라가야 하는 얼굴에",
             "paras": [seg('200', (15, 17)), seg('200', (29, 32))], "src": src('200')},
            {"heading": "엔도타인 없이 3포인트로 고정합니다",
             "paras": [seg('193', (26, 31)), seg('193', (32, 35))], "src": src('193')},
            {"heading": "미간 근육은 완전히 자르지 않습니다",
             "paras": [seg('372', (28, 33)), seg('372', (34, 44)), seg('372', (45, 48))], "src": src('372')},
        ]
    },

    "icons": {"scalp": ICON_SCALP, "scope": ICON_SCOPE, "glabella": ICON_GLABELLA, "browlift": ICON_BROWLIFT},

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('337', (103, 104)), "icon": "sleep"},
            {"text": seg('337', 93), "icon": "scalp"},
            {"text": seg('337', (94, 96)), "icon": "scope"},
            {"text": seg('337', 97).rstrip(','), "icon": "glabella"},
            {"text": seg('337', (98, 102)), "icon": "browlift"},
        ],
        "steps_src": src('337'),
        "note": {"text": seg('195', (60, 62)), "src": src('195')},
        "pros_cons": {"paras": [seg('277', (8, 11)), seg('277', (12, 20))], "src": src('277')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('195', 64), seg('195', (66, 67))], "src": src('195')},
            {"label": "다음날 · 3일", "lines": [seg('195', 65), seg('195', 70)], "src": src('195')},
            {"label": "5일", "lines": [seg('195', (68, 69))], "src": src('195')},
            {"label": "2주", "lines": [seg('194', (29, 31))], "src": src('194')},
            {"label": "첫 6주", "lines": [seg('372', (42, 44))], "src": src('372')},
        ],
        "note": {"text": seg('195', (71, 72)), "src": src('195')}
    },

    "before_after": {
        "title": "내시경 이마거상술 전후",
        "alt": "내시경 이마거상술 전후 사진",
        "items": [
            {"src": src('193'), "image": "https://rococops.com/files/editor/201706271247758434.jpg",
             "caption": "수술전과 수술 후 3주째 모습입니다.", "label": "정면 3주"},
            {"src": src('193'), "image": "https://rococops.com/files/editor/201706271793151948.jpg",
             "caption": "우사면 내시경이마거상술 전후사진입니다.", "label": "사선 3주"},
            {"src": src('194'), "image": "https://rococops.com/files/editor/201703021481610103.jpg",
             "caption": "수술 후 한달 째 모습입니다.", "label": "정면 1개월"},
            {"src": src('194'), "image": "https://rococops.com/files/editor/20170302486459844.jpg",
             "caption": "이마 주름이 얼마나 펴지는지", "label": "이마 주름 1개월"},
            {"src": src('337'), "image": "https://rococops.com/files/editor/20200622124301408540357.jpg",
             "caption": "수술전과 내시경 이마거상술 후 18일째 모습입니다.", "label": "정면 18일"},
            {"src": src('337'), "image": "https://rococops.com/files/editor/20200622124348115416609.jpg",
             "caption": "눈과 눈썹 사이 거리가 거의 두 배로", "label": "측면 18일"},
            {"src": src('200'), "image": "https://rococops.com/files/editor/201605311677538535.jpg",
             "caption": "수술 전과 수술 후 5주째 사진입니다", "label": "20대 정면 5주"},
            {"src": src('195'), "image": "https://rococops.com/files/editor/20181110593554770.jpg",
             "caption": "내시경 이마거상술과 눈밑지방재배치 수술 전과 수술 후 3개월째 전후사진입니다.",
             "label": "눈밑지방재배치 동시 3개월"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('543'), "tag": "효과 유지 기간"},
            {"src": src('337'), "tag": "수술 방법·전후"},
            {"src": src('372'), "tag": "미간 근육 처리"},
            {"src": src('277'), "tag": "꺼진 눈 보완"},
            {"src": src('195'), "tag": "눈밑지방재배치 동시"},
            {"src": src('620'), "tag": "이마보형물 제거 동시"},
        ]
    },

    "faq": [
        {"q": "이마거상술 효과는 얼마나 지속되나요?", "a": seg('543', (66, 68), (77, 80)), "src": src('543')},
        {"q": "시간이 지나 눈썹이 다시 내려오면 재수술할 수 있나요?", "a": seg('195', (111, 114)), "src": src('195')},
        {"q": "두피 절개 흉터가 보이나요?", "a": seg('197', (63, 66)), "src": src('197')},
        {"q": "수술 후 이마가 넓어지나요?", "a": seg('201', (99, 103)), "src": src('201')},
        {"q": "이마 주름은 보톡스로 펴면 안 되나요?", "a": seg('197', (20, 22)), "src": src('197')},
    ],

    "related": [
        {"href": "forehead/reduction", "name": "이마축소술"},
        {"href": "eye/brow-lift", "name": "눈썹하거상술"},
        {"href": "anti-aging/blepharoplasty", "name": "상·하안검성형"},
        {"href": "eye/lower-fat", "name": "눈밑지방 재배치"},
        {"href": "eye/fat-graft", "name": "꺼진눈 지방이식"},
        {"href": "eye/correction", "name": "눈매교정술"},
    ],

    "review_banner_subject": "내시경 이마거상술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'forehead-endoscopic.json')
from _companions import companions_for  # 함께 알아두면 좋은 시술(3순위 하위 메뉴 흡수)
data['companions'] = companions_for(data['page'])
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
