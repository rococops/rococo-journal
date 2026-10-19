"""data/landing/nostril-alar-raising.json 생성 (대표페이지 데이터 작성 예시 — 새 페이지는 이 파일을 복사해서 시작).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nostril-alar-raising.py   →  data/landing/nostril-alar-raising.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nostril/alar-raising/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


data = {
    "_comment": "시술별 대표페이지 데이터(콧날개올리기). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nostril/alar-raising",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "콧날개올리기 수술 | 처진 콧볼·V자 콧구멍 교정, 3세대·4세대 방법과 한계 | 로코코성형외과 김상호 원장",
        "description": "콧날개올리기는 처진 콧볼을 위로 올려 콧구멍 노출과 콧볼 비대칭을 줄이는 수술입니다. 3세대·4세대 방법, 올라가는 정도(1~2mm), 인중축소술 후 한계와 흉터를 김상호 원장의 글로 정리했습니다.",
        "h1": "콧날개올리기 수술",
        "procedure_name": "콧날개올리기 수술"
    },

    "hero": {
        "eyebrow": "ALAR RAISING · 콧날개올리기",
        "question": "콧날개올리기는 어떻게 수술하나요?",
        "summary": {"text": seg('396', 1), "src": src('396')},
        "stats": [
            {"from": 1, "to": 2, "unit": "mm", "label": "콧구멍이 올라가는 정도",
             "quote": seg('396', 44), "src": src('396'),
             "extra": [{"quote": seg('276', (7, 8)), "src": src('276')}]},
            {"from": 15, "to": 30, "unit": "분", "label": "수술 시간 (수술법·범위에 따라)",
             "quote": seg('610', 47), "src": src('610'),
             "extra": [{"quote": seg('265', 67), "src": src('265')},
                       {"quote": seg('523', 57), "src": src('523')}]},
            {"to": 1, "unit": "주", "label": "코 안 실밥 제거 시기",
             "quote": seg('265', 73), "src": src('265')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('396'), "image": "https://rococops.com/files/editor/20210802105650722899894.jpg",
                 "alt": "콧날개올리기 수술 전후 사진", "label": "CASE · 전후", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · ALAR RAISING",
        "toc": "콧날개올리기가 필요한 경우",
        "title": seg('117', 22),
        "items": [seg('117', (23, 26)).rstrip(','), seg('117', 27), seg('117', (30, 31))],
        "note": seg('117', (42, 44)),
        "src": src('117')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "콧구멍을 가리는 대표적인 두 가지 수술",
             "paras": [seg('396', (9, 14)), seg('396', (27, 31))], "src": src('396')},
            {"heading": "3세대와 4세대 콧날개올리기",
             "paras": [seg('610', (5, 11)), seg('610', (12, 17))], "src": src('610')},
            {"heading": "정면 콧구멍 노출을 줄이는 수술입니다",
             "paras": [seg('475', (62, 64)), seg('475', (69, 73))], "src": src('475')},
            {"heading": "처진 콧볼 옆라인도 교정됩니다",
             "paras": [seg('361', (23, 26)), seg('361', (35, 37))], "src": src('361')},
            {"heading": "인중축소술을 받으셨다면",
             "paras": [seg('286', (20, 24)), seg('286', (34, 41))], "src": src('286')},
        ]
    },

    "icons": {
        "stitch": '<path d="M24 60 L96 60" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="3 4"/><path d="M34 46 L44 74 M54 46 L64 74 M74 46 L84 74" fill="none" stroke="#b8956a" stroke-width="3" stroke-linecap="round"/>',
        "week": '<rect x="26" y="30" width="68" height="64" rx="8" fill="#efe4d3" stroke="#b8956a" stroke-width="2.2"/><path d="M26 48 L94 48 M44 22 L44 36 M76 22 L76 36" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round"/><text x="60" y="82" font-size="26" font-weight="700" text-anchor="middle" fill="#b8956a" font-family="sans-serif">7</text>'
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('265', 66).rstrip(','), "icon": "sleep"},
            {"text": seg('265', 67), "icon": "clock"},
            {"text": seg('265', 71).rstrip(','), "icon": "tape"},
            {"text": seg('265', 72), "icon": "stitch"},
            {"text": seg('265', 73), "icon": "week"},
        ],
        "steps_src": src('265'),
        "note": {"text": seg('325', (93, 96)), "src": src('325')},
        "pros_cons": {"paras": [seg('307', (76, 78)), seg('307', (79, 81)), seg('307', (82, 84), 87)], "src": src('307')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('276', (21, 23))], "src": src('276')},
            {"label": "다음 날", "lines": [seg('265', (69, 70))], "src": src('265')},
            {"label": "1주", "lines": [seg('265', 73)], "src": src('265')},
            {"label": "붓기", "lines": [seg('396', (61, 63))], "src": src('396')},
            {"label": "흉터", "lines": [seg('396', (52, 53))], "src": src('396')},
        ],
        "note": {"text": seg('396', (64, 71)), "src": src('396')}
    },

    "before_after": {
        "title": "콧날개올리기 수술 전후",
        "alt": "콧날개올리기 수술 전후 사진",
        "items": [
            {"src": src('396'), "image": "https://rococops.com/files/editor/20210802105650722899894.jpg",
             "caption": "콧구멍이 가려진 것이 확인됩니다.", "label": "정면 전후"},
            {"src": src('396'), "image": "https://rococops.com/files/editor/202108021057011368269132.jpg",
             "caption": "아래쪽에서 본 수술전후 사진입니다.", "label": "아래쪽에서"},
            {"src": src('475'), "image": "https://rococops.com/files/editor/202306231325461285619966.jpg",
             "caption": "수술 전과 수술 후 2개월 사진입니다.", "label": "3세대 2개월"},
            {"src": src('475'), "image": "https://rococops.com/files/editor/202306231325551095620263.jpg",
             "caption": "아래쪽에서 본 전후 사진입니다.", "label": "아래쪽에서"},
            {"src": src('265'), "image": "https://rococops.com/files/editor/20190702101137981230328.jpg",
             "caption": "정면에서 찍은 사진인데요..", "label": "V-콧구멍 교정 정면"},
            {"src": src('265'), "image": "https://rococops.com/files/editor/201907021012491023792582.jpg",
             "caption": "아래쪽에서 본 전후사진에서는", "label": "V-콧구멍 교정 아래쪽"},
            {"src": src('307'), "image": "https://rococops.com/files/editor/202001151230211715724244.jpg",
             "caption": "수술전과", "label": "2세대 3주"},
            {"src": src('610'), "image": "https://rococops.com/files/editor/2025082612304954238861.jpg",
             "caption": "수술 전과 수술 후 2주째 전후 사진입니다.", "label": "4세대 2주"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('396'), "tag": "3세대 · 콧구멍 가리기"},
            {"src": src('475'), "tag": "3세대 · 한계"},
            {"src": src('610'), "tag": "4세대"},
            {"src": src('361'), "tag": "처진 콧볼 옆라인"},
            {"src": src('307'), "tag": "장점과 단점"},
            {"src": src('325'), "tag": "인중축소술과 함께"},
        ]
    },

    "faq": [
        {"q": "콧날개올리기와 인중축소술을 동시에 할 수 있나요?", "a": seg('325', (93, 96)), "src": src('325')},
        {"q": "수술 후 콧구멍이 좁아지거나 호흡이 불편해질 수 있나요?", "a": seg('265', (44, 49)), "src": src('265')},
        {"q": "수술 후 콧구멍 안쪽에 흉터가 보이나요?", "a": seg('396', (52, 53)), "src": src('396')},
        {"q": "콧구멍이 얼마나 가려지나요?", "a": seg('396', (44, 46)), "src": src('396')},
        {"q": "4세대 콧날개올리기는 겉에 흉터가 남나요?", "a": seg('610', (50, 52)), "src": src('610')},
    ],

    "related": [
        {"href": "nostril/alar-lowering", "name": "비공내리기"},
        {"href": "nostril/v-shape", "name": "V형 콧구멍교정"},
        {"href": "nostril/reduction", "name": "콧구멍축소술"},
        {"href": "nostril/alar-base", "name": "콧볼축소술"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/columella", "name": "비주성형"},
    ],

    "review_banner_subject": "콧날개올리기 수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nostril-alar-raising.json')
from _companions import companions_for  # 함께 알아두면 좋은 시술(3순위 하위 메뉴 흡수)
data['companions'] = companions_for(data['page'])
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
