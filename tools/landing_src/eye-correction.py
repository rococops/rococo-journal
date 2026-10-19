"""data/landing/eye-correction.json 생성 (시술별 대표페이지: 눈매교정술).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
한 줄 안에 여러 문장이 붙어 있는 칼럼(248·250)은 part()로 문장 경계에서만 잘라 쓴다(문장 안은 자르지 않음).
사용: python tools/landing_src/eye-correction.py   →  data/landing/eye-correction.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'eye/correction/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def part(n, i, first, last):
    """n번 칼럼 i번째 줄에서 first 로 시작해 last 로 끝나는 구간(문장 경계에서만 사용)."""
    l = lines(n)[i]
    a = l.index(first)
    return l[a:l.index(last, a) + len(last)]


def src(n):
    return f'{P}{n}'


# 눈 선화 공통 요소 (120x120)
_EYE = ('<path d="M14 70 C34 46 86 46 106 70 C86 92 34 92 14 70 Z" fill="#fff" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/>'
        '<circle cx="60" cy="70" r="15" fill="#6b4a3a"/><circle cx="60" cy="70" r="6" fill="#2f2420"/><circle cx="55" cy="64" r="3" fill="#fff"/>')

data = {
    "_comment": "시술별 대표페이지 데이터(눈매교정술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "eye/correction",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "눈매교정술 | 졸린 눈·안검하수, 비절개·무절개(무쌍) 눈매교정과 재수술 | 로코코성형외과 김상호 원장",
        "description": "눈매교정술은 눈 뜨는 힘을 강하게 만들어 졸려 보이는 눈을 또렷하게 하는 수술입니다. 절개·비절개·무절개(무쌍) 눈매교정의 차이, 수술 방법과 회복, 절개 후 비절개 재수술과 비대칭 교정을 김상호 원장의 글로 정리했습니다.",
        "h1": "눈매교정술",
        "procedure_name": "눈매교정술"
    },

    "hero": {
        "eyebrow": "PTOSIS CORRECTION · 눈매교정술",
        "question": "눈매교정술은 어떻게 수술하나요?",
        "summary": {"text": part('248', 6, '눈 뜨는 힘을 강하게', '만들어 주는 수술입니다'), "src": src('248')},
        "stats": [
            {"from": 10, "to": 20, "unit": "분", "label": "수술 시간 (무쌍눈매교정 · 비절개 양쪽)",
             "quote": seg('251', 37), "src": src('251'),
             "extra": [{"quote": seg('251', 39), "src": src('251')}]},
            {"from": 5, "to": 7, "unit": "일", "label": "회복 기간 (드물게 멍이 들면 2주 전후)",
             "quote": seg('256', (42, 43)), "src": src('256')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('256'), "image": "https://rococops.com/files/editor/201902181311378335.jpg",
                 "alt": "남자 비절개 눈매교정 전후 사진", "label": "CASE · 비절개 1주", "layout": "stack"}
    },

    "features": {
        "type": "SIGNS · 졸린 눈",
        "toc": "졸린 눈의 신호",
        "title": "이런 말을 자주 듣는다면",
        "items": [seg('253', 74), seg('253', 75), seg('253', 76)],
        "note": seg('253', (77, 79)),
        "src": src('253')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "눈 뜨는 근육을 조작해 눈이 더 잘 떠지게 하는 수술",
             "paras": [seg('246', (7, 9)), seg('246', (10, 11))], "src": src('246')},
            {"heading": "비절개와 무절개(무쌍) 눈매교정",
             "paras": [seg('248', (14, 15)), seg('248', (33, 35)), seg('248', (36, 38)), seg('248', (53, 55))],
             "src": src('248')},
            {"heading": "절개 눈매교정을 하지 않게 된 이유",
             "paras": [seg('258', (33, 38)), seg('258', (44, 47)), seg('258', (48, 51))], "src": src('258')},
            {"heading": "쌍꺼풀이 흐려지거나 여러 겹이 될 때",
             "paras": [seg('548', (5, 7)), seg('548', (44, 48)), seg('548', (62, 63))], "src": src('548')},
        ]
    },

    # 눈매교정 전용 아이콘 (공용 build_landing.py 는 고치지 않음)
    "icons": {
        # 눈 뜨는 근육 강화: 눈꺼풀 위 근육(붉은 띠)을 실로 묶어 끌어올림
        "lift": _EYE + '<path d="M24 52 C42 34 78 34 96 52" fill="none" stroke="#c46a5a" stroke-width="4" stroke-linecap="round"/>'
                       '<circle cx="60" cy="39" r="4.5" fill="#c9a26f" stroke="#a9834f" stroke-width="1.4"/>'
                       '<path d="M60 30 L60 12 M53 19 L60 12 L67 19" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
        # 자연유착 쌍꺼풀 라인: 쌍꺼풀 선 + 바늘구멍 점
        "fold": _EYE + '<path d="M20 56 C40 36 80 36 100 56" fill="none" stroke="#4a4a4a" stroke-width="2" stroke-linecap="round"/>'
                       '<circle cx="38" cy="44" r="2.6" fill="#b8956a"/><circle cx="60" cy="38.5" r="2.6" fill="#b8956a"/><circle cx="82" cy="44" r="2.6" fill="#b8956a"/>',
        # 회복 기간: 달력
        "calendar": '<rect x="22" y="28" width="76" height="68" rx="8" fill="#fff" stroke="#b8956a" stroke-width="2.4"/>'
                    '<path d="M22 46 L98 46" stroke="#b8956a" stroke-width="2.4"/>'
                    '<path d="M40 20 L40 34 M80 20 L80 34" stroke="#4a4a4a" stroke-width="3" stroke-linecap="round"/>'
                    '<g fill="#efe4d3"><rect x="32" y="56" width="12" height="10" rx="2"/><rect x="54" y="56" width="12" height="10" rx="2"/>'
                    '<rect x="76" y="56" width="12" height="10" rx="2"/><rect x="32" y="74" width="12" height="10" rx="2"/>'
                    '<rect x="76" y="74" width="12" height="10" rx="2"/></g>'
                    '<rect x="54" y="74" width="12" height="10" rx="2" fill="#c9a26f"/>',
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('256', 40).rstrip(','), "icon": "sleep"},
            {"text": seg('256', (38, 39)), "icon": "lift"},
            {"text": seg('256', (21, 23)), "icon": "fold"},
            {"text": seg('256', 41), "icon": "clock"},
            {"text": seg('256', (42, 43)), "icon": "calendar"},
        ],
        "steps_src": src('256'),
        "note": {"text": seg('248', (16, 20)), "src": src('248')},
        "pros_cons": {"paras": [seg('258', (110, 116)), seg('258', (117, 119))], "src": src('258')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "1~2일", "lines": [part('250', 36, '수술 후 1~2일', '부을 수 있답니다')], "src": src('250')},
            {"label": "5일", "lines": [part('250', 36, '보통 남자들이', '할 정도는 됩니다')], "src": src('250')},
            {"label": "5~7일", "lines": [seg('256', (42, 43))], "src": src('256')},
            {"label": "쌍꺼풀 라인", "lines": [seg('251', (33, 34))], "src": src('251')},
            {"label": "초기 비대칭", "lines": [seg('253', (56, 58))], "src": src('253')},
        ],
        "note": {"text": part('250', 36, '붓기나 멍은', '작용을 합니다'), "src": src('250')}
    },

    "before_after": {
        "title": "눈매교정술 전후",
        "alt": "눈매교정술 전후 사진",
        "items": [
            {"src": src('256'), "image": "https://rococops.com/files/editor/201902181311378335.jpg",
             "caption": "비절개눈매교정 전후사진입니다.", "label": "남자 비절개 · 1주"},
            {"src": src('256'), "image": "https://rococops.com/files/editor/20190218566384885.jpg",
             "caption": "스트로보 없이 찍은 남자 비절개눈매교정 전후사진입니다.", "label": "남자 비절개 · 7일 (조명 없이)"},
            {"src": src('251'), "image": "https://rococops.com/files/editor/201702201584486742.jpg",
             "caption": "비절개눈매교정 전후사진", "label": "절개 후 비절개 재수술 · 2일"},
            {"src": src('250'), "image": "https://rococops.com/files/editor/201603151728289966.jpg",
             "caption": "수술 전 사진과 수술 후 3주째 사진입니다", "label": "무쌍(무절개) 눈매교정 · 3주"},
            {"src": src('253'), "image": "https://rococops.com/files/editor/201706191187305963.jpg",
             "caption": "눈밑지방이동술 비절개눈매교정 수술전후 5주째 사진입니다", "label": "비절개 + 눈밑지방이동술 · 5주"},
            {"src": src('247'), "image": "https://rococops.com/files/editor/1386141008.jpg",
             "caption": "비절개눈매교정 전후사진입니다.", "label": "남자 비절개 · 비대칭"},
            {"src": src('247'), "image": "https://rococops.com/files/editor/1386141147.jpg",
             "caption": "수술 전의 약간 힘이 빠진듯하고 잠이 오는 느낌,", "label": "졸린 눈 · 비대칭"},
            {"src": src('246'), "image": "https://rococops.com/files/editor/1375860914.jpg",
             "caption": "비절개 눈매교정술과 뒷트임을 같이 하신 분입니다.", "label": "비절개 + 뒷트임"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('248'), "tag": "종합 설명"},
            {"src": src('258'), "tag": "심한 비대칭"},
            {"src": src('251'), "tag": "절개 후 재수술"},
            {"src": src('250'), "tag": "무쌍(무절개)"},
            {"src": src('256'), "tag": "남자 비절개"},
            {"src": src('548'), "tag": "쌍꺼풀 겹주름"},
        ]
    },

    "faq": [
        {"q": "절개 눈매교정을 받은 눈도 비절개로 재수술할 수 있나요?", "a": seg('251', (21, 25)), "src": src('251')},
        {"q": "비절개 눈매교정은 절개법보다 빨리 풀리지 않나요?", "a": seg('258', (120, 123)), "src": src('258')},
        {"q": "남자도 수술한 티 나지 않게 할 수 있나요?", "a": seg('256', (17, 18), (21, 23)), "src": src('256')},
        {"q": "쌍꺼풀이 있는 눈에 무절개 눈매교정을 하면 어떻게 되나요?", "a": seg('248', (41, 45)), "src": src('248')},
        {"q": "눈 위가 꺼진 눈에도 눈매교정이 도움이 되나요?", "a": seg('278', 37, (40, 42)), "src": src('278')},
    ],

    "related": [
        {"href": "eye/fat-graft", "name": "꺼진눈 지방이식"},
        {"href": "eye/lower-fat", "name": "눈밑지방 재배치"},
        {"href": "anti-aging/blepharoplasty", "name": "상·하안검성형"},
        {"href": "eye/double", "name": "쌍커풀 자연유착법"},
        {"href": "eye/incision", "name": "트임성형"},
        {"href": "forehead/endoscopic", "name": "내시경 이마거상술"},
    ],

    "review_banner_subject": "눈매교정술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'eye-correction.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
