"""data/landing/eye-double.json 생성 (쌍커풀 자연유착법 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/eye-double.py   →  data/landing/eye-double.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'eye/double/'


def seg(n, *ranges):
    # 'eye/correction/256' 처럼 다른 하위 메뉴 칼럼은 전체 경로로 받음
    return L.seg(n if '/' in n else P + n, *ranges)


def src(n):
    return n if '/' in n else f'{P}{n}'


# 시술명 표기: 지금 부르는 이름(자연유착법) + 옛 이름(매몰법)
NAME = '자연유착법 쌍커풀 수술(매몰법)'

# 이 페이지 전용 수술 단계 아이콘 (120x120 선화, 눈 모양)
_EYE = ('<path d="M18 70 C36 48 84 48 102 70 C84 90 36 90 18 70 Z" fill="#fff" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/>'
        '<circle cx="60" cy="70" r="13" fill="#6b4a3a"/><circle cx="64" cy="66" r="3" fill="#fff"/>')
ICONS = {
    # 바늘구멍 흉터: 눈 위 쌍커풀 라인(금색) + 작은 바늘구멍 점
    'pinhole': _EYE + '<path d="M22 58 C40 36 80 36 98 58" fill="none" stroke="#b8956a" stroke-width="2.6" stroke-linecap="round"/>'
                      '<circle cx="40" cy="44" r="2.4" fill="#c46a5a"/><circle cx="60" cy="38.5" r="2.4" fill="#c46a5a"/>'
                      '<circle cx="80" cy="44" r="2.4" fill="#c46a5a"/>',
    # 회복기간: 달력 + 감은 눈(쌍커풀 라인)
    'calendar': '<rect x="22" y="28" width="76" height="70" rx="8" fill="#fff" stroke="#b8956a" stroke-width="2.4"/>'
                '<path d="M22 46 L98 46" stroke="#b8956a" stroke-width="2.4"/>'
                '<path d="M40 20 L40 34 M80 20 L80 34" stroke="#4a4a4a" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M38 74 C48 84 72 84 82 74" fill="none" stroke="#4a4a4a" stroke-width="2.4" stroke-linecap="round"/>'
                '<path d="M40 64 C50 56 70 56 80 64" fill="none" stroke="#b8956a" stroke-width="2.2" stroke-linecap="round"/>'
                '<path d="M46 80 L43 86 M60 83 L60 89 M74 80 L77 86" stroke="#4a4a4a" stroke-width="2" stroke-linecap="round"/>',
    # 세안·화장: 눈 + 물방울
    'wash': _EYE + '<path d="M28 30 C28 30 18 42 18 48 A10 10 0 0 0 38 48 C38 42 28 30 28 30 Z" fill="#cfe3ef" stroke="#6f97ad" stroke-width="2"/>'
                   '<path d="M96 22 C96 22 88 32 88 37 A8 8 0 0 0 104 37 C104 32 96 22 96 22 Z" fill="#cfe3ef" stroke="#6f97ad" stroke-width="2"/>'
                   '<path d="M26 58 C42 40 78 40 94 58" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round"/>',
}

data = {
    "_comment": "시술별 대표페이지 데이터(쌍커풀 자연유착법). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "eye/double",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": f"{NAME} | 수면마취 10분, 매몰·절개 차이와 풀림·회복 | 로코코성형외과 김상호 원장",
        "description": f"{NAME}은 수면마취 후 국소마취를 하고 10분 정도 걸리는 쌍꺼풀 수술입니다. 매몰·절개·부분절개의 차이, 풀림, 쌍커풀의 깊이, 흉터와 회복 과정을 김상호 원장의 글로 정리했습니다.",
        "h1": NAME,
        "procedure_name": NAME
    },

    "hero": {
        "eyebrow": f"DOUBLE EYELID · {NAME}",
        "question": f"{NAME}은 어떻게 수술하나요?",
        "summary": {"text": seg('509', (7, 9)), "src": src('509')},
        "stats": [
            {"to": 10, "unit": "분", "label": "수술 시간",
             "quote": seg('509', 9), "src": src('509'),
             "extra": [{"quote": seg('199', 76), "src": src('199')}]},
            {"to": 2, "unit": "일", "label": "회복기간",
             "quote": seg('26', 10), "src": src('26')},
            {"to": 3, "unit": "년", "label": "전문의 취득 후 눈수술 전문",
             "quote": seg('392', (7, 9)), "src": src('392')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('26'), "image": "https://rococops.com/files/editor/201505171445206497.jpg",
                 "alt": "자연유착법 쌍커풀 수술 전후 사진", "label": "CASE · 수술 전후 2주", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · DOUBLE EYELID",
        "toc": "매몰·절개·부분절개",
        "title": "쌍커풀 수술의 세 가지 방법",
        "items": [seg('26', (4, 5)), seg('26', (82, 84)), seg('26', (95, 99))],
        "note": seg('26', 49),
        "src": src('26')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "얼굴이 가장 많이 변할 수 있는 수술",
             "paras": [seg('26', (16, 17)), seg('26', (18, 20)), seg('26', (21, 22))], "src": src('26')},
            {"heading": "같은 높이라도 쌍커풀의 깊이는 다릅니다",
             "paras": [seg('392', (29, 33)), seg('392', (63, 66))], "src": src('392')},
            {"heading": "처진살이 많을 때는 쌍커풀만으로 해결하지 않습니다",
             "paras": [seg('392', (85, 93)), seg('392', (95, 101))], "src": src('392')},
            {"heading": "원래 눈수술이 전문이었습니다",
             "paras": [seg('392', (5, 6)), seg('392', (7, 11)), seg('392', (12, 13))], "src": src('392')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('26', 8), "icon": "sleep"},
            {"text": seg('26', 9), "icon": "clock"},
            {"text": seg('26', (18, 19)).rstrip(','), "icon": "pinhole"},
            {"text": seg('26', 10), "icon": "calendar"},
            {"text": seg('26', 11), "icon": "wash"},
        ],
        "steps_src": src('26'),
        "note": {"text": seg('509', 10), "src": src('509')},
        "pros_cons": {"paras": [seg('26', 56), seg('26', (87, 89))], "src": src('26')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "수술 당일", "lines": [seg('509', (7, 9))], "src": src('509')},
            {"label": "다음날", "lines": [seg('26', 11)], "src": src('26')},
            {"label": "2일", "lines": [seg('26', 10)], "src": src('26')},
            {"label": "2주", "lines": [seg('26', 41), seg('26', 42)], "src": src('26')},
        ],
        "note": {"text": seg('26', 20), "src": src('26')}
    },

    "before_after": {
        "title": f"{NAME} 전후",
        "alt": "자연유착법 쌍커풀 수술 전후 사진",
        "items": [
            {"src": src('26'), "image": "https://rococops.com/files/editor/1319855124.jpg",
             "label": "4중 고정 매몰법"},
            {"src": src('26'), "image": "https://rococops.com/files/editor/201505171445206497.jpg",
             "caption": "수술 후 2주째 사진입니다.", "label": "2주 (눈밑 애교필러 함께)"},
            {"src": src('509'), "image": "https://rococops.com/files/editor/202402261122261379530516.jpg",
             "caption": "쌍커풀(자연유착) + 밑트임 + 코성형 후 2일째 모습입니다.", "label": "2일째 (밑트임·코성형 함께)"},
            {"src": src('26'), "image": "https://rococops.com/files/editor/1319020280.jpg",
             "label": "낮은 라인 (앞트임·뒷트임 함께)"},
            {"src": src('26'), "image": "https://rococops.com/files/editor/1342969984.jpg",
             "label": "매몰법 (앞트임·뒷트임 함께)"},
            {"src": src('26'), "image": "https://rococops.com/files/editor/1319158898.jpg",
             "label": "쌍커풀 (앞트임·뒷트임 함께)"},
            {"src": src('26'), "image": "https://rococops.com/files/editor/1318813021.jpg",
             "label": "재수술 · 인라인→아웃라인"},
            {"src": src('25'), "image": "https://rococops.com/files/editor/1330050962.jpg",
             "label": "절개 후 매몰법 재수술"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('26'), "tag": "종합 설명"},
            {"src": src('509'), "tag": "수술 시간·통증"},
            {"src": src('392'), "tag": "쌍커풀의 깊이"},
            {"src": src('199'), "tag": "이마거상술과 함께"},
            {"src": src('25'), "tag": "눈 재수술"},
            {"src": src('611'), "tag": "절개 쌍커풀(피부절제)"},
        ]
    },

    "faq": [
        {"q": "매몰법은 풀리지 않나요?", "a": seg('26', (4, 5), (87, 89)), "src": src('26')},
        {"q": "흉터가 남나요?", "a": seg('eye/correction/256', (21, 23)), "src": src('eye/correction/256')},
        {"q": "남자도 티 나지 않게 할 수 있나요?", "a": seg('eye/correction/256', (15, 20)),
         "src": src('eye/correction/256')},
        {"q": "결과가 마음에 들지 않으면 어떻게 하나요?", "a": seg('26', (21, 22)), "src": src('26')},
    ],

    "related": [
        {"href": "eye/correction", "name": "눈매교정술"},
        {"href": "eye/incision", "name": "트임성형"},
        {"href": "eye/brow-lift", "name": "눈썹하거상술"},
        {"href": "forehead/endoscopic", "name": "내시경 이마거상술"},
        {"href": "eye/fat-graft", "name": "꺼진눈 지방이식"},
        {"href": "eye/lower-fat", "name": "눈밑지방 재배치"},
    ],

    "icons": ICONS,
    "review_banner_subject": NAME,
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'eye-double.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
