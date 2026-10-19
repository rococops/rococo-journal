"""data/landing/cheekbone-rear.json 생성 (뒷광대축소술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
한 줄에 여러 문장이 붙어 있는 칼럼(165)은 cut() 으로 원문 줄에서 시작·끝 표지 사이를 그대로 잘라 온다.
사용: python tools/landing_src/cheekbone-rear.py   →  data/landing/cheekbone-rear.json
"""
import sys, os, json, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'cheekbone/rear/'


def lines(n):
    return L.lines(P + n)


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


def cut(n, i, start, end):
    """칼럼 n 의 i번째 줄에서 start 표지부터 end 표지(포함)까지를 원문 그대로 잘라 온다."""
    t = lines(n)[i]
    a = t.index(start)
    b = t.index(end, a) + len(end)
    return t[a:b]


# 수술 방법 단계 전용 아이콘 (공용에 없는 것만, 120x120)
ICON_CUT = ('<path d="M44 16 C70 10 94 34 92 64 C90 88 72 102 54 100 C38 98 28 82 30 58 C31 40 36 24 44 16 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
            '<ellipse cx="93" cy="62" rx="6" ry="11" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
            '<path d="M74 46 L74 76" stroke="#c46a5a" stroke-width="3.2" stroke-linecap="round"/>'
            '<path d="M68 46 L80 46 M68 76 L80 76" stroke="#c46a5a" stroke-width="1.6" stroke-linecap="round"/>')
ICON_TRIM = ('<path d="M10 86 C34 86 40 46 60 46 C80 46 86 86 110 86 L110 104 L10 104 Z" fill="#efe4d3" stroke="none"/>'
             '<path d="M10 86 C34 86 40 46 60 46 C80 46 86 86 110 86" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="4 4"/>'
             '<path d="M10 86 C36 86 42 66 60 66 C78 66 84 86 110 86" fill="none" stroke="#4a4a4a" stroke-width="2.4" stroke-linecap="round"/>'
             '<path d="M60 30 L60 52 M54 46 L60 52 L66 46" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
ICON_JAW = ('<path d="M24 34 C40 22 78 22 96 34" fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round"/>'
            '<path d="M96 34 C100 62 92 84 72 96 C58 100 44 96 34 90" fill="none" stroke="#4a4a4a" stroke-width="2.2" stroke-linecap="round"/>'
            '<circle cx="90" cy="50" r="13" fill="#c9a26f" stroke="#a9834f" stroke-width="1.8"/>'
            '<path d="M84 50 L89 55 L97 44" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
ICON_SMOOTH = ('<path d="M18 22 C40 22 52 44 52 60 C52 78 66 96 100 98" fill="none" stroke="#c46a5a" stroke-width="2" stroke-dasharray="4 4"/>'
               '<path d="M18 22 C36 24 44 40 48 60 C52 80 66 94 100 98" fill="none" stroke="#4a4a4a" stroke-width="2.4" stroke-linecap="round"/>'
               '<path d="M78 30 L84 36 L96 22" fill="none" stroke="#b8956a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

data = {
    "_comment": "시술별 대표페이지 데이터(뒷광대축소술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "cheekbone/rear",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "뒷광대축소술 | 구레나룻 앞 뼈가 튀어나온 경우, 수술 방법·흉터·회복 | 로코코성형외과 김상호 원장",
        "description": "뒷광대는 귀 앞 구레나룻 부위가 혹처럼 튀어나온 뼈입니다. 어떤 경우에 뒷광대축소술이 도움이 되는지, 수술 방법과 한계, 흉터와 회복을 김상호 원장의 글과 전후사진으로 정리했습니다.",
        "h1": "뒷광대축소술",
        "procedure_name": "뒷광대축소술"
    },

    "hero": {
        "eyebrow": "REAR CHEEKBONE · 뒷광대축소술",
        "question": "뒷광대축소술은 어떻게 수술하나요?",
        "summary": {"text": seg('163', (6, 7)), "src": src('163')},
        "stats": [
            {"from": 15, "to": 20, "unit": "분", "label": "수술 시간 (양쪽)",
             "quote": cut('165', 7, '양측 수술하는데', '정도입니다.'), "src": src('165'),
             "extra": [{"quote": seg('163', 77), "src": src('163')}]},
            {"from": 3, "to": 5, "unit": "일", "label": "일상생활 복귀",
             "quote": cut('165', 7, '그리 심하게', '복귀하신답니다.'), "src": src('165')},
            {"from": 6, "to": 12, "unit": "개월", "label": "흉터가 연한 선으로 남기까지",
             "quote": seg('312', (35, 39)), "src": src('312')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('168'), "image": "https://rococops.com/files/editor/201801091659744858.jpg",
                 "alt": "뒷광대축소술 수술 전후 사진", "label": "CASE · 측면 3주", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · REAR CHEEKBONE",
        "toc": "뒷광대축소술이 필요한 경우",
        "title": seg('167', 19),
        "items": [seg('167', (8, 10)), seg('167', (21, 23)), seg('167', (24, 25))],
        "note": seg('167', 20),
        "src": src('167')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "뒷광대는 어떤 부위인가요",
             "paras": [seg('163', (8, 9)), seg('163', (20, 21))], "src": src('163')},
            {"heading": "꼭 넣는 것이 좋은 경우는 많지 않습니다",
             "paras": [cut('165', 3, '제가 그동안', '싶은데요..'), seg('165', 4)], "src": src('165')},
            {"heading": "줄인 만큼 얼굴이 달라지는 것은 아닙니다",
             "paras": [seg('166', (9, 14))], "src": src('166')},
            {"heading": "최근에는 이렇게 판단합니다",
             "paras": [seg('347', (26, 30))], "src": src('347')},
        ]
    },

    "icons": {"cut": ICON_CUT, "trim": ICON_TRIM, "jaw": ICON_JAW, "smooth": ICON_SMOOTH},

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('163', 77), "icon": "sleep"},
            {"text": seg('163', (73, 74)), "icon": "cut"},
            {"text": seg('163', 69), "icon": "trim"},
            {"text": seg('163', (70, 71)).rstrip(','), "icon": "jaw"},
            {"text": seg('163', 72), "icon": "smooth"},
        ],
        "steps_src": src('163'),
        "note": {"text": seg('167', (30, 35)), "src": src('167')},
        "pros_cons": {"paras": [seg('163', (65, 67)), seg('163', (57, 58))], "src": src('163')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "3~5일", "lines": [cut('165', 7, '그리 심하게', '복귀하신답니다.')], "src": src('165')},
            {"label": "2주", "lines": [seg('166', (28, 29))], "src": src('166')},
            {"label": "3주", "lines": [seg('168', (28, 30))], "src": src('168')},
            {"label": "6~12개월", "lines": [seg('312', (35, 39))], "src": src('312')},
            {"label": "1년", "lines": [seg('166', 30)], "src": src('166')},
        ],
        "note": {"text": seg('304', (68, 70)), "src": src('304')}
    },

    "before_after": {
        "title": "뒷광대축소술 전후",
        "alt": "뒷광대축소술 전후 사진",
        "items": [
            {"src": src('165'), "image": "https://rococops.com/files/editor/201706101817575656.jpg",
             "caption": "수술전과 수술 후 대략 3주째 사진입니다.", "label": "측면 3주"},
            {"src": src('168'), "image": "https://rococops.com/files/editor/201801091659744858.jpg",
             "caption": "뒷광대수술 후 3주째 전후사진입니다.", "label": "측면 3주"},
            {"src": src('168'), "image": "https://rococops.com/files/editor/201801091120965956.jpg",
             "caption": "역시 뒷광대수술 전후사진입니다.", "label": "측면 3주 (좌)"},
            {"src": src('166'), "image": "https://rococops.com/files/editor/201706141326719958.jpg",
             "caption": "변형15분광대축소술 + 뒷광대축소술 수술 후 2주째입니다.", "label": "측면 2주"},
            {"src": src('164'), "image": "https://rococops.com/files/editor/201703071984777612.jpg",
             "caption": "수술 후 2주 반 경과사진입니다.", "label": "측면 2주 반"},
            {"src": src('304'), "image": "https://rococops.com/files/editor/20191220102241646394003.jpg",
             "caption": "역시 좌측 퀵광대 + 뒷광대 축소술 3주째 수술 전후사진입니다.", "label": "사면 3주"},
            {"src": src('304'), "image": "https://rococops.com/files/editor/20191220102256238344942.jpg",
             "caption": "고개를 숙이고 위에서 찍은 전후사진입니다.", "label": "위에서 3주"},
            {"src": src('304'), "image": "https://rococops.com/files/editor/20191220102315202970684.jpg",
             "caption": "아래쪽에서 본 사진입니다.", "label": "아래쪽에서 3주"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('163'), "tag": "종합 설명"},
            {"src": src('165'), "tag": "수술 대상"},
            {"src": src('166'), "tag": "한계"},
            {"src": src('167'), "tag": "x-ray·안전"},
            {"src": src('312'), "tag": "흉터"},
            {"src": src('347'), "tag": "퀵광대와 함께"},
        ]
    },

    "faq": [
        {"q": "뒷광대축소술 흉터는 얼마나 남나요?", "a": seg('312', (32, 39)), "src": src('312')},
        {"q": "뒷광대는 얼마나 줄일 수 있나요?", "a": seg('166', 8) + ' ' + seg('166', (12, 13)), "src": src('166')},
        {"q": "뒷광대는 모든 사람이 줄여야 하나요?", "a": seg('347', (11, 15)), "src": src('347')},
        {"q": "뒷광대를 완전히 없앨 수 있나요?", "a": seg('164', (12, 13)), "src": src('164')},
        {"q": "다른 병원에서 광대축소술을 받았는데 뒷광대가 남았다면 뒷광대만 따로 수술받을 수 있나요?",
         "a": seg('312', (22, 31)), "src": src('312')},
    ],

    "related": [
        {"href": "cheekbone/quick", "name": "15분 광대축소술"},
        {"href": "cheekbone/revision", "name": "광대 재수술"},
        {"href": "cheekbone/fat-graft", "name": "심부볼·관자 지방이식"},
        {"href": "cheekbone/liposuction", "name": "광대라인 지방흡입"},
        {"href": "guide/cheekbone-reduction-guide", "name": "광대축소술 종류와 선택 기준 (성형 가이드)"},
        {"href": "guide/cheekbone-reduction-face-type", "name": "광대축소술 효과, 얼굴형별 차이 (성형 가이드)"},
    ],

    "review_banner_subject": "뒷광대축소술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'cheekbone-rear.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
