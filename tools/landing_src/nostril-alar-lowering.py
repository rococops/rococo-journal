"""data/landing/nostril-alar-lowering.json 생성 (대표페이지 데이터 작성 예시 — 새 페이지는 이 파일을 복사해서 시작).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nostril-alar-lowering.py   →  data/landing/nostril-alar-lowering.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nostril/alar-lowering/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


data = {
    "_comment": "시술별 대표페이지 데이터(비공내리기). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nostril/alar-lowering",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "비공내리기 수술 | 콧구멍 가리는 수술, M자 콧구멍 유형별 효과와 회복 | 로코코성형외과 김상호 원장",
        "description": "비공내리기는 정면에서 콧구멍이 보이는 것을 가려주는 수술입니다. M자 콧구멍 Type 1·2·3별 효과 차이, 수술 방법, 회복과 흉터를 김상호 원장의 글로 정리했습니다.",
        "h1": "비공내리기 수술",
        "procedure_name": "비공내리기 수술"
    },

    "hero": {
        "eyebrow": "ALAR LOWERING · 비공내리기",
        "question": "비공내리기는 어떻게 수술하나요?",
        "summary": {"text": seg('13', 3), "src": src('13')},
        "stats": [
            {"to": 97, "unit": "%", "label": "안쪽 흉터가 눈에 잘 띄지 않는 환자",
             "quote": seg('553', 64), "src": src('553')},
            {"from": 20, "to": 40, "unit": "분", "label": "수술 시간 (한쪽 · 양쪽)",
             "quote": seg('303', 58), "src": src('303'),
             "extra": [{"quote": "시간은 대략 40분 걸립니다.", "src": src('428')}]},
            {"to": 1, "unit": "주", "label": "코끝 반창고 유지 기간",
             "quote": seg('303', 59), "src": src('303')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('439'), "image": "https://rococops.com/files/editor/202211041149181214442072.jpg",
                 "alt": "비공내리기 수술 전후 정면 사진", "label": "CASE · 정면 전후", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · ALAR LOWERING",
        "toc": "콧구멍이 보이는 원인",
        "title": seg('366', 16),
        "items": [re.sub(r'^\d\.\s+', '', lines('366')[i]) for i in range(17, 21)],
        "note": seg('366', (21, 22)),
        "src": src('366')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "콧구멍이 보이는 분들이 많이 찾는 수술입니다",
             "paras": [seg('13', (3, 6)), seg('13', (117, 121))], "src": src('13')},
            {"heading": "M자 콧구멍의 세 가지 유형",
             "paras": [seg('13', (145, 147)), seg('13', (150, 152)), seg('13', (179, 181)), seg('13', (196, 198))],
             "src": src('13')},
            {"heading": "모든 M자 콧구멍이 교정이 필요한 것은 아닙니다",
             "paras": [seg('13', (137, 139)), seg('13', 140, 144)], "src": src('13')},
            {"heading": "17년간의 비공내리기",
             "paras": [seg('553', (5, 10)), seg('553', (11, 16))], "src": src('553')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('303', 56), "icon": "sleep"},
            {"text": seg('303', (50, 51)).rstrip(','), "icon": "ear"},
            {"text": seg('303', (52, 53)).rstrip(','), "icon": "graft"},
            {"text": seg('303', 58), "icon": "clock"},
            {"text": seg('303', 59), "icon": "tape"},
        ],
        "steps_src": src('303'),
        "note": {"text": seg('428', (164, 167)), "src": src('428')},
        "pros_cons": {"paras": [seg('553', (36, 39)), seg('553', (44, 46))], "src": src('553')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('303', 56), seg('303', 57)], "src": src('303')},
            {"label": "1주", "lines": [seg('303', 59), seg('303', (60, 61))], "src": src('303')},
            {"label": "2주", "lines": [seg('428', (169, 172))], "src": src('428')},
            {"label": "2개월", "lines": [seg('155', (39, 40)), seg('155', (41, 42))], "src": src('155')},
            {"label": "붓기", "lines": [seg('303', 64)], "src": src('303')},
        ],
        "note": {"text": seg('155', (34, 35)), "src": src('155')}
    },

    "before_after": {
        "title": "비공내리기 수술 전후",
        "alt": "비공내리기 수술 전후 사진",
        "items": [
            {"src": src('439'), "image": "https://rococops.com/files/editor/202211041149181214442072.jpg",
             "caption": "수술 전과 수술 후 2개월 사진입니다.", "label": "정면 2개월"},
            {"src": src('439'), "image": "https://rococops.com/files/editor/202211041149381880854033.jpg",
             "caption": "콧구멍 아래쪽에서 본 수술전후 사진입니다.", "label": "아래쪽에서"},
            {"src": src('449'), "image": "https://rococops.com/files/editor/202211181927441124968148.jpg",
             "caption": "수술 전과 수술 후 6주 사진입니다.", "label": "정면 6주"},
            {"src": src('364'), "image": "https://rococops.com/files/editor/20210111151010167322907.jpg",
             "caption": "수술 전과 수술 후 3주째 정면사진입니다.", "label": "정면 3주"},
            {"src": src('303'), "image": "https://rococops.com/files/editor/20191213170033175584088.jpg",
             "caption": "수술전과 수술 후 3주째 사진입니다.", "label": "정면 3주"},
            {"src": src('303'), "image": "https://rococops.com/files/editor/201912131702261543722594.jpg",
             "caption": "완전히 아래쪽에서 본 전후사진입니다.", "label": "아래쪽에서"},
            {"src": src('390'), "image": "https://rococops.com/files/editor/20210503153840937560940.jpg",
             "caption": "수술 전후 아래쪽에서 콧구멍 안쪽을 본 사진입니다.", "label": "용코(Type 3) 안쪽"},
            {"src": src('428'), "image": "https://rococops.com/files/editor/20221011154833270930423.jpg",
             "caption": "수술전과 수술 후 콧구멍 안쪽 사진입니다.", "label": "용코 안쪽"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('13'), "tag": "종합 설명"},
            {"src": src('366'), "tag": "원인별 해결법"},
            {"src": src('553'), "tag": "한계·부작용"},
            {"src": src('474'), "tag": "제거"},
            {"src": src('308'), "tag": "단독 수술 전후"},
            {"src": src('428'), "tag": "용코에서의 한계"},
        ]
    },

    "faq": [
        {"q": "비공내리기 수술은 제거할 수 있나요?", "a": seg('474', (42, 46)), "src": src('474')},
        {"q": "수술 후 콧구멍 안쪽에 흉터가 보이나요?", "a": seg('553', (64, 66)), "src": src('553')},
        {"q": "용코(Type 3)도 비공내리기가 되나요?", "a": seg('553', (52, 53), (60, 61)), "src": src('553')},
        {"q": "귀에서 연골과 피부를 채취하면 귀 모양이 변하나요?",
         "a": seg('553', 21).split(' (귀모양')[0] + ' ' + seg('553', 22), "src": src('553')},
        {"q": "수술 후 숨쉬기가 불편해지나요?", "a": seg('553', (87, 89)), "src": src('553')},
    ],

    "related": [
        {"href": "nostril/alar-raising", "name": "콧날개올리기"},
        {"href": "nostril/v-shape", "name": "V형 콧구멍교정"},
        {"href": "nostril/reduction", "name": "콧구멍축소술"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
        {"href": "nose/columella", "name": "비주성형"},
    ],

    "review_banner_subject": "비공내리기 수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nostril-alar-lowering.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
