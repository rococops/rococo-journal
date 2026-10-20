"""data/landing/cheekbone-quick.json 생성 (15분 광대축소술·퀵광대 대표페이지 데이터).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/cheekbone-quick.py   →  data/landing/cheekbone-quick.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'cheekbone/quick/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


IMG = 'https://rococops.com/files/editor/'

data = {
    "_comment": "시술별 대표페이지 데이터(15분 광대축소술·퀵광대). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "cheekbone/quick",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "퀵광대(15분 광대축소술) | 수면마취·두피 작은 절개, 옆광대와 45도 광대 | 로코코성형외과 김상호 원장",
        "description": "퀵광대(15분 광대축소술)는 수면마취로 입안 절개 없이 하는 광대축소술입니다. 옆광대·45도 광대(변형15분) 차이, 수술 방법, 회복 기간, 부작용을 김상호 원장의 글로 정리했습니다.",
        "h1": "퀵광대(15분 광대축소술)",
        "procedure_name": "퀵광대(15분 광대축소술)"
    },

    "hero": {
        "eyebrow": "QUICK CHEEKBONE · 퀵광대",
        "question": "퀵광대(15분 광대축소술)는 어떻게 수술하나요?",
        "summary": {"text": seg('19', (103, 105)), "src": src('19')},
        "stats": [
            {"from": 10, "to": 20, "unit": "분", "label": "수술 시간 (퀵광대 · 변형15분)",
             "quote": seg('19', 106), "src": src('19'),
             "extra": [{"quote": seg('19', (120, 121)), "src": src('19')}]},
            {"from": 1, "to": 2, "unit": "주", "label": "변형15분 광대축소술 일반적인 회복 기간",
             "quote": seg('19', (122, 123)), "src": src('19')},
            {"to": 17, "unit": "년", "label": "퀵광대 방식 수술 집도 기간",
             "quote": seg('546', 5), "src": src('546')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('504'), "image": IMG + "20240207094438716212032.jpg",
                 "alt": "퀵광대 방식 광대축소술 수술 전후 정면 사진", "label": "CASE · 정면 전후", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · QUICK CHEEKBONE",
        "toc": "퀵광대 방식이란",
        "title": seg('546', (22, 23)),
        "items": [re.sub(r'^\d\.\s+', '', lines('546')[i]) for i in range(24, 27)],
        "note": seg('546', 27),
        "src": src('546')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "옆광대와 45도 광대",
             "paras": [seg('19', (260, 262)), seg('19', (382, 384))], "src": src('19')},
            {"heading": "광대는 광대뼈만으로 만들어지지 않습니다",
             "paras": [seg('19', (12, 16)), seg('19', (24, 26))], "src": src('19')},
            {"heading": "퀵광대(15분 광대축소술)를 만들기까지",
             "paras": [seg('19', (180, 183)), seg('19', (189, 192)), seg('19', (206, 207))], "src": src('19')},
            {"heading": "17년간의 퀵광대",
             "paras": [seg('546', 5), seg('546', (15, 18))], "src": src('546')},
        ]
    },

    "icons": {
        # 두피 작은 절개: 옆얼굴 윤곽 + 귀 위쪽 짧은 절개선(붉은색)
        "scalp": '<path d="M30 78 C26 40 44 18 66 20 C88 22 98 44 92 72 C90 86 82 96 70 98 C58 100 48 92 44 84 C38 82 32 82 30 78 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/>'
                 '<path d="M30 78 C26 50 40 26 64 22 C46 28 38 48 40 70 Z" fill="#6b4a3a" fill-opacity=".75"/>'
                 '<path d="M52 44 L66 38" stroke="#c46a5a" stroke-width="3.4" stroke-linecap="round"/>'
                 '<path d="M86 58 C92 62 92 70 86 74" fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round"/>',
        # 내시경 확인: 내시경(막대+렌즈)과 뼈
        "scope": '<path d="M24 84 L74 44" stroke="#4a4a4a" stroke-width="9" stroke-linecap="round"/>'
                 '<path d="M24 84 L74 44" stroke="#efe4d3" stroke-width="4" stroke-linecap="round"/>'
                 '<circle cx="82" cy="38" r="12" fill="#efe4d3" stroke="#b8956a" stroke-width="2.4"/>'
                 '<circle cx="82" cy="38" r="5" fill="#b8956a"/>'
                 '<path d="M52 98 C62 88 78 88 96 96" fill="none" stroke="#a9834f" stroke-width="3" stroke-linecap="round"/>',
        # 고정핀 없음: 나사 + 금지선
        "nopin": '<path d="M60 22 L60 86" stroke="#4a4a4a" stroke-width="7" stroke-linecap="round"/>'
                 '<path d="M48 34 L72 40 M48 48 L72 54 M48 62 L72 68" stroke="#4a4a4a" stroke-width="3" stroke-linecap="round"/>'
                 '<path d="M50 20 L70 20" stroke="#4a4a4a" stroke-width="5" stroke-linecap="round"/>'
                 '<circle cx="60" cy="60" r="40" fill="none" stroke="#c46a5a" stroke-width="3.4"/>'
                 '<path d="M32 88 L88 32" stroke="#c46a5a" stroke-width="3.4" stroke-linecap="round"/>',
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('19', 195), "icon": "sleep"},
            {"text": seg('19', 264), "icon": "scalp"},
            {"text": seg('19', 272), "icon": "scope"},
            {"text": seg('19', (203, 204)), "icon": "nopin"},
            {"text": seg('19', (115, 117)), "icon": "tape"},
        ],
        "steps_src": src('19'),
        "note": {"text": seg('19', (386, 391)), "src": src('19')},
        "pros_cons": {"paras": [seg('87', (99, 101)), seg('87', (155, 158))], "src": src('87')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "퀵광대(옆광대)", "lines": [seg('19', (106, 110))], "src": src('19')},
            {"label": "변형15분(45도 포함)", "lines": [seg('19', (120, 125))], "src": src('19')},
            {"label": "스펀지", "lines": [seg('19', (115, 117)), seg('19', (130, 132))], "src": src('19')},
            {"label": "다음날~1개월", "lines": [seg('19', (142, 144))], "src": src('19')},
            {"label": "붓기", "lines": [seg('19', 175, (176, 177))], "src": src('19')},
        ],
        "note": {"text": seg('19', (359, 362)), "src": src('19')}
    },

    "before_after": {
        "title": "퀵광대 수술 전후",
        "alt": "퀵광대 방식 광대축소술 수술 전후 사진",
        "items": [
            {"src": src('504'), "image": IMG + "20240207094438716212032.jpg",
             "caption": "수술 전과 수술 후 2개월 사진입니다.", "label": "정면 2개월"},
            {"src": src('504'), "image": IMG + "202402070944492139015357.jpg",
             "caption": "좌측 광대 수술 전후 2개월 사진입니다.", "label": "좌측 2개월"},
            {"src": src('504'), "image": IMG + "202402070944551483367038.jpg",
             "caption": "아래쪽에서 본 전후사진", "label": "아래쪽에서"},
            {"src": src('502'), "image": IMG + "2024011817331746835447.jpg",
             "caption": "수술 전과 수술 후 2주 전후사진입니다.", "label": "정면 2주"},
            {"src": src('502'), "image": IMG + "202401181733001406463600.jpg",
             "caption": "수술 전과 수술 후 2주 전후사진입니다.", "label": "측면 2주"},
            {"src": src('502'), "image": IMG + "20240118173324832153605.jpg",
             "caption": "아래쪽에서 본 전후사진입니다.", "label": "아래쪽에서"},
            {"src": src('467'), "image": IMG + "20230217100411567269004.jpg",
             "caption": "우측 광대 수술전과 수술 후 2주째", "label": "우측 2주"},
            {"src": src('467'), "image": IMG + "20230217100437161504679.jpg",
             "caption": "아래쪽에서 본 광대 전후사진입니다.", "label": "아래쪽에서"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('19'), "tag": "종합 설명"},
            {"src": src('87'), "tag": "회복 기간"},
            {"src": src('546'), "tag": "부작용"},
            {"src": src('94'), "tag": "자주 묻는 질문"},
            {"src": src('89'), "tag": "수술 종류 비교"},
            {"src": src('106'), "tag": "얼굴형별 효과"},
        ]
    },

    "faq": [
        {"q": "광대축소술 후 10년이 지나면 볼처짐이 생기나요?",
         "a": seg('94', (67, 68), (78, 79)), "src": src('94')},
        {"q": "비고정(자연고정) 수술을 하면 뼈가 다시 나오나요?",
         "a": seg('94', (112, 114), 118), "src": src('94')},
        {"q": "흉터는 어디에 어떻게 남나요?",
         "a": seg('546', (54, 56), (64, 69)), "src": src('546')},
        {"q": "고정하지 않는데 뼈가 안 붙는 불유합은 없나요?",
         "a": seg('546', (117, 122)), "src": src('546')},
        {"q": "광대수술로 안면비대칭이 교정되나요?",
         "a": seg('19', (150, 152)), "src": src('19')},
    ],

    "related": [
        {"href": "cheekbone/rear", "name": "뒷광대축소술"},
        {"href": "cheekbone/fat-graft", "name": "심부볼·관자 지방이식"},
        {"href": "cheekbone/liposuction", "name": "광대라인 지방흡입"},
        {"href": "cheekbone/revision", "name": "광대 재수술"},
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
    ],

    "review_banner_subject": "퀵광대 수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'cheekbone-quick.json')
from _companions import companions_for  # 함께 알아두면 좋은 시술(3순위 하위 메뉴 흡수)
data['companions'] = companions_for(data['page'])
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
