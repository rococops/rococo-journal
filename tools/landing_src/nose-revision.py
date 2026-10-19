"""data/landing/nose-revision.json 생성 (코재수술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nose-revision.py   →  data/landing/nose-revision.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/revision/'


def lines(n):
    return L.lines(n if '/' in n else P + n)


def seg(n, *ranges):
    return L.seg(n if '/' in n else P + n, *ranges)


def src(n):
    return n if '/' in n else f'{P}{n}'


HUMP550 = 'nose/hump/550'  # 다른 하위 메뉴 칼럼: 코재수술/첫수술 비율

# 페이지 전용 아이콘 (120x120 안의 SVG 요소)
_LINE = 'fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    # 수술 목표 정하기: 과녁
    "target": '<circle cx="60" cy="60" r="38" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
              '<circle cx="60" cy="60" r="24" fill="#efe4d3" stroke="#b8956a" stroke-width="2.2"/>'
              '<circle cx="60" cy="60" r="9" fill="#c46a5a"/>'
              '<path d="M60 12 L60 30 M60 90 L60 108 M12 60 L30 60 M90 60 L108 60" ' + _LINE + '/>',
    # 재료 선택: 늑연골(금색 곡선 막대)
    "rib": '<path d="M22 44 C40 30 80 30 98 44" fill="none" stroke="#b8956a" stroke-width="10" stroke-linecap="round"/>'
           '<path d="M22 64 C40 50 80 50 98 64" fill="none" stroke="#c9a26f" stroke-width="10" stroke-linecap="round"/>'
           '<path d="M22 84 C40 70 80 70 98 84" fill="none" stroke="#b8956a" stroke-width="10" stroke-linecap="round"/>',
}

data = {
    "_comment": "시술별 대표페이지 데이터(코재수술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nose/revision",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "코재수술 | 재료 선택과 수술 계획, 구축코·들린코·찝힌코 교정 | 로코코성형외과 김상호 원장",
        "description": "코재수술은 이전 수술과 현재 코 상태에 따라 방법이 달라집니다. 재료 선택 기준, 보형물 제거와 코재수술의 차이, 구축코·들린코 교정 사례를 김상호 원장의 글로 정리했습니다.",
        "h1": "코재수술",
        "procedure_name": "코재수술"
    },

    "hero": {
        "eyebrow": "REVISION RHINOPLASTY · 코재수술",
        "question": "코재수술은 어떻게 진행하나요?",
        "summary": {"text": seg('1', (35, 36)), "src": src('1')},
        "stats": [
            {"to": 80, "unit": "%", "label": "집도하는 코수술 중 코재수술 비중",
             "quote": seg(HUMP550, (5, 7)), "src": HUMP550},
            {"to": 3, "unit": "주", "label": "염증이 있을 때 보형물 제거 후 집중치료 기간",
             "quote": seg('1', (11, 12)), "src": src('1')},
            {"from": 90, "to": 120, "unit": "분", "label": "자가늑연골 들린코 교정 수술 시간 (채취 포함)",
             "quote": seg('122', (37, 38)), "src": src('122')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('122'), "image": "https://rococops.com/files/editor/1396866555.jpg",
                 "alt": "코재수술 전후 정면 사진", "label": "CASE · 정면 전후", "layout": "stack"}
    },

    "features": {
        "type": "CHECK · REVISION",
        "toc": "재수술 전에 따져볼 것",
        "title": seg('160', (13, 14)),
        "items": [re.sub(r'^\(\d\)\s+', '', lines('160')[i]) for i in range(16, 20)],
        "note": seg('160', (42, 46)),
        "src": src('160')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "코재수술을 하러 오신 분들의 코",
             "paras": [seg('1', (35, 37)), seg('1', (44, 45))], "src": src('1')},
            {"heading": "재수술은 언제 하나요?",
             "paras": [seg('1', (5, 14))], "src": src('1')},
            {"heading": "어떤 연골이 가장 좋은가요?",
             "paras": [seg('160', (10, 12)), seg('160', (21, 28))], "src": src('160')},
            {"heading": "제거수술과 코재수술은 다른 수술입니다",
             "paras": [seg('340', (23, 28)), seg('340', (52, 56))], "src": src('340')},
            {"heading": "코재수술을 많이 하는 이유",
             "paras": [seg(HUMP550, (5, 7))], "src": HUMP550},
        ]
    },

    "icons": ICONS,

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('160', (62, 63)), "icon": "target"},
            {"text": seg('160', (13, 14)), "icon": "rib"},
            {"text": seg('160', (79, 80)), "icon": "tip"},
            {"text": seg('160', (86, 90)), "icon": "deviation"},
            {"text": seg('160', (83, 84)).rstrip(','), "icon": "fill"},
        ],
        "steps_src": src('160'),
        "note": {"text": seg('60', (18, 23)), "src": src('60')},
        "pros_cons": {"paras": [seg('127', (54, 56)), seg('127', (57, 60))], "src": src('127')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "염증이 있었다면", "lines": [seg('122', (10, 11))], "src": src('122')},
            {"label": "7일 (찝힌코 교정)", "lines": [seg('603', (69, 70))], "src": src('603')},
            {"label": "3개월", "lines": [seg('127', (59, 60))], "src": src('127')},
            {"label": "6개월", "lines": [seg('160', 107)], "src": src('160')},
        ],
        "note": {"text": seg('122', (37, 39)), "src": src('122')}
    },

    "before_after": {
        "title": "코재수술 전후",
        "alt": "코재수술 전후 사진",
        "items": [
            {"src": src('122'), "image": "https://rococops.com/files/editor/1396866555.jpg",
             "caption": "정면 수술전후모습입니다.", "label": "정면"},
            {"src": src('122'), "image": "https://rococops.com/files/editor/1396866577.jpg",
             "caption": "아래쪽에서 본 사진입니다.", "label": "아래쪽에서"},
            {"src": src('160'), "image": "https://rococops.com/files/editor/20181115104173737.jpg",
             "caption": "실내조명에서 찍은 코재수술 전후사진입니다.", "label": "정면 실내조명"},
            {"src": src('160'), "image": "https://rococops.com/files/editor/20181115869990594.jpg",
             "caption": "우사면 전후사진", "label": "우사면"},
            {"src": src('160'), "image": "https://rococops.com/files/editor/20181115322384068.jpg",
             "caption": "우측면 전후사진에서 보면 코끝이 많이 늘어난 것이 보이는데요,", "label": "우측면"},
            {"src": src('160'), "image": "https://rococops.com/files/editor/2018111546564606.jpg",
             "caption": "좌측면 사진입니다.", "label": "좌측면"},
            {"src": src('425'), "image": "https://rococops.com/files/editor/202208121359072125474534.jpg",
             "caption": "수술전과 수술 후 2개월 사진입니다.", "label": "정면 2개월"},
            {"src": src('425'), "image": "https://rococops.com/files/editor/20220812140022867101548.jpg",
             "caption": "수술전후 우측면 사진입니다.", "label": "우측면 2개월"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('1'), "tag": "디자인이 잘못된 코"},
            {"src": src('160'), "tag": "재료 선택"},
            {"src": src('340'), "tag": "제거수술 vs 코재수술"},
            {"src": src('60'), "tag": "염증·구축코"},
            {"src": src('127'), "tag": "들린코 교정"},
            {"src": src('491'), "tag": "찝힌코 교정"},
        ]
    },

    "faq": [
        {"q": "코재수술에는 어떤 연골이 가장 좋은가요?", "a": seg('160', (10, 14)), "src": src('160')},
        {"q": "보형물 제거수술과 코재수술은 무엇이 다른가요?", "a": seg('340', (26, 28)), "src": src('340')},
        {"q": "보형물을 제거하면 코 모양을 예측할 수 있나요?", "a": seg('340', (34, 35), (42, 44)), "src": src('340')},
        {"q": "염증 뒤에 코가 들리고 일그러지는 이유는 무엇인가요?", "a": seg('60', (7, 10)), "src": src('60')},
        {"q": "기증늑연골로 코재수술을 할 수 있나요?", "a": seg('425', (177, 180)), "src": src('425')},
    ],

    "related": [
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nose/columella", "name": "비주성형"},
        {"href": "nose/hump", "name": "매부리코"},
        {"href": "nostril/v-shape", "name": "V형 콧구멍교정"},
    ],

    "review_banner_subject": "코재수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-revision.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
