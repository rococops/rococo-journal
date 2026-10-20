"""data/landing/nose-columella.json 생성 (비주성형 대표페이지 — nostril-alar-lowering.py 를 복사해서 작성).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nose-columella.py   →  data/landing/nose-columella.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/columella/'
CAT = 'nose/cat/'  # 비순각 고양이 입매교정 메뉴의 '비주 말린 코끝' 설명 칼럼(346)


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


data = {
    "_comment": "시술별 대표페이지 데이터(비주성형: 비주내리기·비주올리기). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nose/columella",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "비주내리기·비주올리기 수술 | 비주말린 코·처진 비주 교정, 비개방 방법과 한계 | 로코코성형외과 김상호 원장",
        "description": "비주내리기(예전 이름 비주빼기)와 비주올리기는 콧구멍 사이 기둥인 비주와 콧볼의 높이를 맞추는 수술입니다. 비주말린 코의 원인, 비개방 비주내리기 방법과 조건, 재료, 회복과 한계를 김상호 원장의 글로 정리했습니다.",
        "h1": "비주내리기·비주올리기 수술",
        "procedure_name": "비주내리기·비주올리기 수술"
    },

    "hero": {
        "eyebrow": "COLUMELLA · 비주성형",
        "question": "비주내리기·비주올리기는 어떻게 수술하나요?",
        "summary": {"text": seg('297', (6, 7)), "src": src('297')},
        "stats": [
            {"to": 20, "unit": "분", "label": "수술 시간 (비개방 비주내리기)",
             "quote": seg('519', 12).rstrip(','), "src": src('519'),
             "extra": [{"quote": seg('524', (54, 55)), "src": src('524')}]},
            {"to": 2, "unit": "주", "label": "회복 기간 (비공내리기·코성형과 함께 할 때)",
             "quote": seg('538', (48, 50)), "src": src('538'),
             "extra": [{"quote": seg('494', (77, 78)), "src": src('494')}]},
            {"to": 15, "unit": "년+", "label": "비주말린 코 집중 수술",
             "quote": seg('498', 6), "src": src('498')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('500'), "image": "https://rococops.com/files/editor/20240118172125947907391.jpg",
                 "alt": "비개방 비주내리기 수술 전후 정면 사진", "label": "CASE · 비개방 비주내리기 4주", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · COLUMELLA",
        "toc": "비주말린 코에 필요한 네 가지 수술",
        "title": L.seg(CAT + '346', (79, 80)),
        "items": [L.seg(CAT + '346', i) for i in (81, 82, 83, 84)],
        "note": L.seg(CAT + '346', (85, 88)),
        "src": CAT + '346'
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "비주가 올라갔는지 내려갔는지, 기준은 콧볼과의 평행입니다",
             "paras": [seg('297', (6, 10)).rstrip(','), seg('297', (15, 18)), seg('297', (41, 43))], "src": src('297')},
            {"heading": "비주말린 코, 근본 문제는 처진 콧볼입니다",
             "paras": [seg('561', (8, 14)), seg('561', (30, 35))], "src": src('561')},
            {"heading": "정도에 따라 수술이 달라집니다",
             "paras": [seg('625', (17, 24)), seg('625', (31, 33))], "src": src('625')},
            {"heading": "큰 수술만이 좋은 수술은 아닙니다",
             "paras": [seg('498', (7, 11)), seg('498', (12, 17)), seg('498', (42, 44))], "src": src('498')},
        ]
    },

    "icons": {
        "inside": '<path d="M24 86 C24 50 44 30 60 30 C76 30 96 50 96 86 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/><ellipse cx="44" cy="80" rx="9" ry="6" fill="#4a4a4a"/><ellipse cx="76" cy="80" rx="9" ry="6" fill="#4a4a4a"/><path d="M53 62 L53 76" fill="none" stroke="#c46a5a" stroke-width="2.4" stroke-dasharray="3 3"/>',
        "notape": '<g transform="rotate(-20 60 62)"><rect x="18" y="48" width="84" height="28" rx="14" fill="#f3d9bf" stroke="#b8956a" stroke-width="2.2"/></g><path d="M28 28 L92 96" fill="none" stroke="#c46a5a" stroke-width="4" stroke-linecap="round"/>'
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('519', (5, 8)), "icon": "tip"},
            {"text": seg('519', 31), "icon": "ear"},
            {"text": seg('519', 12).rstrip(','), "icon": "sleep"},
            {"text": seg('519', 13).rstrip(','), "icon": "inside"},
            {"text": seg('519', 14).rstrip(','), "icon": "notape"},
        ],
        "steps_src": src('519'),
        "note": {"text": seg('500', (40, 43)), "src": src('500')},
        "pros_cons": {"paras": [seg('519', (9, 11)), seg('519', (24, 25))], "src": src('519')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "반창고", "lines": [seg('519', 14).rstrip(',')], "src": src('519')},
            {"label": "1~2일 (미니코끝성형)", "lines": [seg('206', 14)], "src": src('206')},
            {"label": "2주 (비공내리기와 함께)", "lines": [seg('538', (48, 50))], "src": src('538')},
            {"label": "18개월 (자가늑연골 코끝 연장술과 함께)", "lines": [seg('625', (119, 120))], "src": src('625')},
        ],
        "note": {"text": seg('500', 58), "src": src('500')}
    },

    "before_after": {
        "title": "비주내리기·비주올리기 수술 전후",
        "alt": "비주성형 수술 전후 사진",
        "items": [
            {"src": src('500'), "image": "https://rococops.com/files/editor/20240118172125947907391.jpg",
             "caption": "비개방 비주내리기 수술", "label": "비주내리기 정면 4주"},
            {"src": src('500'), "image": "https://rococops.com/files/editor/202401181721561716044556.jpg",
             "caption": "우측면 전후사진에서", "label": "비주내리기 측면 4주"},
            {"src": src('519'), "image": "https://rococops.com/files/editor/20240305143907716738474.jpg",
             "caption": "2주차 수술 전후사진입니다", "label": "비주내리기 측면 2주"},
            {"src": src('519'), "image": "https://rococops.com/files/editor/20240305143931399274080.jpg",
             "caption": "2주차 수술 전후사진입니다", "label": "반대쪽 측면 2주"},
            {"src": src('498'), "image": "https://rococops.com/files/editor/20240110105316339321002.jpg",
             "caption": "좌측면 전후사진에서 수술 후 비주와 콧구멍이 젓가락처럼 수평이 된 것이 보이는데,", "label": "구축코 측면 6주"},
            {"src": src('498'), "image": "https://rococops.com/files/editor/20240110105210417993186.jpg",
             "caption": "아래쪽에서 본 전후사진입니다.", "label": "구축코 아래쪽 6주"},
            {"src": src('297'), "image": "https://rococops.com/files/editor/20191111140523846135717.jpg",
             "caption": "수술전과 수술 후 2주째입니다.", "label": "비주올리기 정면 2주"},
            {"src": src('297'), "image": "https://rococops.com/files/editor/201911111406531899614061.jpg",
             "caption": "비주가 올라간 것이 확실히 보입니다.", "label": "비주올리기 측면 2주"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('625'), "tag": "재료 · 자가늑연골"},
            {"src": src('561'), "tag": "비주말린 코 · 한계"},
            {"src": src('519'), "tag": "비개방 단독 비주내리기"},
            {"src": src('498'), "tag": "구축코 · 리모델링"},
            {"src": src('297'), "tag": "비주올리기"},
            {"src": src('401'), "tag": "인중축소술 후 비주올리기"},
        ]
    },

    "faq": [
        {"q": "콧구멍이 들려 보이는데 들린코인가요?", "a": seg('524', (41, 44)), "src": src('524')},
        {"q": "귀연골로도 비주를 충분히 내릴 수 있나요?", "a": seg('625', (29, 33)), "src": src('625')},
        {"q": "비주를 내리면 콧구멍이 찝혀 올라가지 않나요?",
         "a": L.seg(CAT + '346', (35, 39), (41, 43)), "src": CAT + '346'},
        {"q": "비주내리기 후 다시 말려 올라가지 않나요?", "a": seg('498', (70, 71)), "src": src('498')},
        {"q": "처진 비주를 올리는 수술도 있나요?", "a": seg('401', (18, 26)), "src": src('401')},
    ],

    "related": [
        {"href": "nose/long", "name": "긴코"},
        {"href": "nose/cat", "name": "비순각 고양이 입매교정"},
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
        {"href": "nose/revision", "name": "코재수술"},
    ],

    "review_banner_subject": "비주성형 수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-columella.json')
from _companions import companions_for  # 함께 알아두면 좋은 시술(3순위 하위 메뉴 흡수)
data['companions'] = companions_for(data['page'])
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
