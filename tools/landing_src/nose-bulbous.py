"""data/landing/nose-bulbous.json 생성 (복코 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
복코 하위 메뉴 칼럼이 짧은 사례 글 위주라, 원리·한계 설명은 다른 메뉴의 원장님 1인칭 칼럼(nose/column/394, nostril/alar-base/295)에서도 가져온다.
사용: python tools/landing_src/nose-bulbous.py   →  data/landing/nose-bulbous.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/bulbous/'


# 번호 목록('1. ', '2. ')이 문장 중간에 있는 줄은 seg()가 번호를 떼어 원문과 달라지므로 lines()를 그대로 이어붙인다.
def seg(n, *ranges):
    """n 이 '394' 처럼 번호만이면 복코 메뉴, 'nose/column/394' 처럼 경로면 그 칼럼."""
    return L.seg(src(n), *ranges)


def src(n):
    return n if '/' in n else f'{P}{n}'


data = {
    "_comment": "시술별 대표페이지 데이터(복코). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nose/bulbous",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "복코 수술 | 찝혀 보이지 않게 코끝 좁히는 복코교정, 콧볼축소·절골술과의 관계 | 로코코성형외과 김상호 원장",
        "description": "복코 수술은 코끝이 작아지되 집게로 집은 것처럼 보이지 않아야 합니다. 코끝 연골 정리 방법, 피부 두께와 피부 표면적의 한계, 콧볼축소·절골술과 함께 하는 경우, 회복과 전후사진을 김상호 원장의 글로 정리했습니다.",
        "h1": "복코 수술",
        "procedure_name": "복코 수술"
    },

    "hero": {
        "eyebrow": "BULBOUS NOSE · 복코",
        "question": "복코는 어떻게 수술하나요?",
        "summary": {"text": seg('10', (4, 7)), "src": src('10')},
        "stats": [
            {"to": 1, "unit": "시간", "label": "수술 시간 (전후)",
             "quote": seg('10', 17), "src": src('10')},
            {"to": 1, "unit": "주", "label": "회복기간",
             "quote": seg('10', 18), "src": src('10')},
            {"to": 1, "unit": "주", "label": "세안·화장 시작",
             "quote": seg('10', 19), "src": src('10')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('136'), "image": "https://rococops.com/files/editor/20151001493206366.jpg",
                 "alt": "복코 수술 전후 정면 사진", "label": "CASE · 정면 전후", "layout": "stack"}
    },

    "features": {
        "type": "AREA · BULBOUS NOSE",
        "toc": "좁힐 수 있는 부위",
        "title": "넓은 코, 어디까지 좁힐 수 있나요?",
        "items": [seg('574', 13), seg('574', (14, 15)), seg('574', (17, 18)), seg('574', (19, 20))],
        "note": seg('574', (5, 7)),
        "src": src('574')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "찝혀 보이지 않게, 정면에서 좁아 보이게",
             "paras": [' '.join(L.lines(src('112'))[38:42]), seg('112', (42, 45))], "src": src('112')},
            {"heading": "코끝을 좁힐 수는 있어도, 작게 만들기는 어렵습니다",
             "paras": [seg('nose/column/394', (40, 45)), seg('nose/column/394', (69, 72)),
                       seg('nose/column/394', (80, 82))], "src": 'nose/column/394'},
            {"heading": "복코교정과 콧볼축소술을 함께 하는 이유",
             "paras": [seg('nostril/alar-base/295', (7, 13))], "src": 'nostril/alar-base/295'},
            {"heading": "얻는 것과 잃는 것의 경계점",
             "paras": [seg('50', 34), seg('50', 38), seg('50', 45)], "src": src('50')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('112', (7, 8)).rstrip(','), "icon": "tip"},
            {"text": seg('112', 36).rstrip(','), "icon": "graft"},
            {"text": seg('112', 37), "icon": "fill"},
            {"text": seg('112', (53, 54)), "icon": "tip"},
            {"text": seg('112', 55), "icon": "tip"},
        ],
        "steps_src": src('112'),
        "note": {"text": seg('112', (56, 57)), "src": src('112')},
        "pros_cons": {"paras": [seg('112', (67, 69)), seg('112', (70, 72))], "src": src('112')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('10', 16), seg('10', 17)], "src": src('10')},
            {"label": "1주", "lines": [seg('10', 18), seg('10', 19)], "src": src('10')},
            {"label": "절골술 병행 시", "lines": [seg('44', (17, 18))], "src": src('44')},
            {"label": "1개월", "lines": [seg('10', (35, 36))], "src": src('10')},
            {"label": "붓기", "lines": [seg('229', 14)], "src": src('229')},
        ],
        "note": {"text": seg('226', 12), "src": src('226')}
    },

    "before_after": {
        "title": "복코 수술 전후",
        "alt": "복코 수술 전후 사진",
        "items": [
            {"src": src('136'), "image": "https://rococops.com/files/editor/20151001493206366.jpg",
             "caption": "수술 전과 수술 후 10개월째 사진입니다.", "label": "정면 10개월"},
            {"src": src('112'), "image": "https://rococops.com/files/editor/1385686931.jpg",
             "caption": "코끝이 자연스럽게 좁아지면서", "label": "정면 · 코끝 피부가 얇은 경우"},
            {"src": src('112'), "image": "https://rococops.com/files/editor/1385687075.jpg",
             "caption": "벌어져있던 양측 코끝 연골이 잘 모아져서", "label": "아래쪽에서"},
            {"src": src('113'), "image": "https://rococops.com/files/editor/1385885069.jpg",
             "caption": "비중격 연골로 코끝을 높이면서 코끝연골을 모아주어 코끝이 좁아지게 만듭니다.",
             "label": "정면 · 복코 재수술"},
            {"src": src('76'), "image": "https://rococops.com/files/album/attach1/1_20110508184752036.jpg",
             "caption": "일반적인 복코교정 사례였습니다.", "label": "정면 · 콧날개 줄이기 함께"},
            {"src": src('226'), "image": "https://rococops.com/files/editor/1307882493.jpg",
             "caption": "코끝 복코교정을 동시에 시행하였습니다.", "label": "정면 · 코필러 재수술 함께"},
            {"src": src('239'), "image": "https://rococops.com/files/editor/1342967352.jpg",
             "caption": "정면 수술 전사진을 보면", "label": "정면 · 매부리 교정·절골 함께"},
            {"src": src('10'), "image": "https://rococops.com/files/album/attach1/1_201105071528782768.jpg",
             "caption": "복코 교정하신지 한달 정도 되는 사진입니다.", "label": "얼굴 정면 1개월"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('112'), "tag": "코끝 피부가 얇은 경우"},
            {"src": src('136'), "tag": "복코수술의 핵심"},
            {"src": src('574'), "tag": "좁힐 수 있는 부위"},
            {"src": src('565'), "tag": "얼굴이 넓어 보일까?"},
            {"src": src('50'), "tag": "복코 재수술"},
            {"src": src('76'), "tag": "콧날개 함께"},
        ]
    },

    "faq": [
        {"q": "복코교정으로 코끝이 작아지면 얼굴이 넓어 보이지 않나요?",
         "a": seg('565', (16, 17), (21, 22)), "src": src('565')},
        {"q": "콧날개(콧볼)도 같이 줄여야 하나요?", "a": seg('76', (8, 11)), "src": src('76')},
        {"q": "비절개 콧볼축소술만 받아도 되나요?", "a": seg('565', (24, 28)), "src": src('565')},
        {"q": "넓은 콧대는 어떻게 좁히나요?", "a": seg('44', (7, 8)), "src": src('44')},
        {"q": "복코 재수술은 어떤 경우에 많이 하나요?", "a": seg('136', (34, 39)), "src": src('136')},
    ],

    "related": [
        {"href": "nostril/alar-base", "name": "콧볼축소술"},
        {"href": "nose/osteotomy", "name": "절골술"},
        {"href": "nose/hump", "name": "매부리코"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/septal", "name": "비중격연골 코성형"},
        {"href": "nose/rib-cartilage", "name": "늑연골 명품코성형"},
    ],

    "review_banner_subject": "복코 수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-bulbous.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
