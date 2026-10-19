"""data/landing/nose-osteotomy.json 생성 (코 절골술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nose-osteotomy.py   →  data/landing/nose-osteotomy.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/osteotomy/'


def seg(n, *ranges):
    # 다른 하위 메뉴 칼럼은 'nose/hump/185' 처럼 전체 경로로 넘긴다
    return L.seg(n if '/' in n else P + n, *ranges)


def src(n):
    return n if '/' in n else f'{P}{n}'


# 이 페이지 전용 아이콘 (정면 코 + 코뼈 부위)
_NOSE = ('<path d="M50 14 C49 40 46 62 40 78 C33 82 33 92 42 93 C46 93 49 91 52 92 L68 92 C71 91 74 93 78 93 '
         'C87 92 87 82 80 78 C74 62 71 40 70 14 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2" stroke-linejoin="round"/>'
         '<path d="M50 14 C49 30 48 42 47 52 L73 52 C72 42 71 30 70 14 Z" fill="#efe4d3" stroke="#b8956a" stroke-width="1.6"/>')
_CUT = 'fill="none" stroke="#c46a5a" stroke-width="2.4" stroke-dasharray="4 3" stroke-linecap="round"'
_MEDIAL = f'<path d="M57 16 L56 40 M63 16 L64 40" {_CUT}/>'
_LATERAL = f'<path d="M51 18 C50 32 49 42 47 52 M69 18 C70 32 71 42 73 52" {_CUT}/>'
ICONS = {
    # 내측·외측 두 군데 금
    "osteo_cut": _NOSE + _MEDIAL + _LATERAL,
    # 내측절골
    "osteo_in": _NOSE + _MEDIAL,
    # 외측절골: 피부 바깥에서 작은 절골도
    "osteo_out": _NOSE + _LATERAL +
                 '<path d="M18 30 L42 40" stroke="#b8956a" stroke-width="3" stroke-linecap="round"/>'
                 '<path d="M102 30 L78 40" stroke="#b8956a" stroke-width="3" stroke-linecap="round"/>',
    # 손가락으로 눌러 코뼈를 안쪽으로
    "press": _NOSE + _LATERAL +
             '<path d="M16 34 L38 34 M32 28 L38 34 L32 40" fill="none" stroke="#b8956a" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M104 34 L82 34 M88 28 L82 34 L88 40" fill="none" stroke="#b8956a" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
    # 코뼈가 새 위치에서 굳음: 달력
    "bone_set": '<rect x="24" y="28" width="72" height="66" rx="8" fill="#efe4d3" stroke="#b8956a" stroke-width="2.2"/>'
                '<path d="M24 46 L96 46 M42 20 L42 36 M78 20 L78 36" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round"/>'
                '<path d="M44 70 L56 82 L78 58" fill="none" stroke="#c46a5a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
}

data = {
    "_comment": "시술별 대표페이지 데이터(코 절골술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "nose/osteotomy",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "코 절골술 | 넓은 콧대·코뼈 좁히기, 휜코 교정과 회복 | 로코코성형외과 김상호 원장",
        "description": "코 절골술은 코뼈에 금을 내 안쪽으로 모아 넓은 콧대를 좁히거나 휜 콧대를 바로잡는 수술입니다. 절골로 좁아지는 부위와 한계, 보형물 수술과 함께 할 때의 염증 가능성, 회복을 김상호 원장의 글로 정리했습니다.",
        "h1": "코 절골술",
        "procedure_name": "코 절골술"
    },

    "icons": ICONS,

    "hero": {
        "eyebrow": "OSTEOTOMY · 코 절골술",
        "question": "코 절골술은 어떻게 수술하나요?",
        "summary": {"text": seg('205', (7, 8)), "src": src('205')},
        "stats": [
            {"to": 2, "unit": "주", "label": "밀려 들어간 코뼈가 굳는 기간",
             "quote": seg('562', 50), "src": src('562')},
            {"to": 2, "unit": "mm", "label": "외측절골에 쓰는 절골도",
             "quote": seg('562', (59, 60)), "src": src('562')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('205'), "image": "https://rococops.com/files/editor/1303658956.jpg",
                 "alt": "코 절골술 전후 아래쪽 사진", "label": "CASE · 아래쪽 전후", "layout": "stack"}
    },

    "features": {
        "type": "AREA · OSTEOTOMY",
        "toc": "좁힐 수 있는 부위",
        "title": seg('573', (6, 7)),
        "items": [seg('573', 13), seg('573', (14, 15)), seg('573', (17, 18)), seg('573', (19, 20))],
        "note": seg('573', (38, 39)),
        "src": src('573')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "코뼈를 다 깨는 수술이 아닙니다",
             "paras": [seg('205', (9, 13)), seg('205', (14, 16))], "src": src('205')},
            {"heading": "매부리를 다듬은 뒤 코뼈를 모아줍니다",
             "paras": [seg('nose/hump/329', (69, 70)), seg('nose/hump/329', (71, 75))], "src": src('nose/hump/329')},
            {"heading": "꼭 필요한 경우에만 절골합니다",
             "paras": [seg('562', (55, 56)), seg('562', (130, 131)), seg('562', (145, 148))], "src": src('562')},
            {"heading": "수면마취로 하는 절골",
             "paras": [seg('205', (26, 28)), seg('205', (29, 33))], "src": src('205')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('562', (45, 46)), "icon": "osteo_cut"},
            {"text": seg('562', 58).rstrip(','), "icon": "osteo_in"},
            {"text": seg('562', (59, 60)), "icon": "osteo_out"},
            {"text": seg('562', (47, 48)), "icon": "press"},
            {"text": seg('562', 50), "icon": "bone_set"},
        ],
        "steps_src": src('562'),
        "note": {"text": seg('205', (19, 23)), "src": src('205')},
        "pros_cons": {"paras": [seg('562', (20, 22)), seg('562', (32, 33))], "src": src('562')}
    },

    "recovery": {
        "title": "회복",
        "items": [
            {"label": "1주", "lines": [seg('225', (11, 12))], "src": src('225')},
            {"label": "2주", "lines": [seg('562', 50)], "src": src('562')},
            {"label": "2주 반", "lines": [seg('569', 47)], "src": src('569')},
            {"label": "잔붓기", "lines": [seg('569', 48)], "src": src('569')},
        ],
        "note": {"text": seg('205', 46), "src": src('205')}
    },

    "before_after": {
        "title": "코 절골술 전후",
        "alt": "코 절골술 전후 사진",
        "items": [
            {"src": src('205'), "image": "https://rococops.com/files/editor/1303658956.jpg",
             "caption": "절골술의 효과는 사진상으로는 아래쪽에서 볼 때 가장 잘 드러난답니다.", "label": "아래쪽에서"},
            {"src": src('205'), "image": "https://rococops.com/files/editor/1303657761.jpg",
             "caption": "남자분의 사진입니다.", "label": "정면 · 넓은 코뼈"},
            {"src": src('569'), "image": "https://rococops.com/files/editor/202406241209151489893901.jpg",
             "caption": "수술 전과, 수술 후 2주 반 정면 사진입니다.", "label": "정면 2주 반"},
            {"src": src('569'), "image": "https://rococops.com/files/editor/20240624121002936604266.jpg",
             "caption": "실내조명에서 정면 전후사진입니다.", "label": "정면 실내조명"},
            {"src": src('569'), "image": "https://rococops.com/files/editor/202406241209521564310462.jpg",
             "caption": "양 측면 전후사진입니다.", "label": "측면"},
            {"src": src('240'), "image": "https://rococops.com/files/editor/1342967352.jpg",
             "caption": "정면 수술 전사진을 보면", "label": "정면 · 매부리·복코"},
            {"src": src('240'), "image": "https://rococops.com/files/editor/1310913402.jpg",
             "caption": "수술 전 사진을 보시면 안면비대칭이 동반된 휜코로", "label": "휜코 정면"},
            {"src": src('207'), "image": "https://rococops.com/files/editor/1385885069.jpg",
             "caption": "비중격 연골로 코끝을 높이면서 코끝연골을 모아주어 코끝이 좁아지게 만듭니다.", "label": "재수술 정면"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('562'), "tag": "절골과 염증"},
            {"src": src('573'), "tag": "좁아지는 부위"},
            {"src": src('205'), "tag": "넓은 코뼈"},
            {"src": src('569'), "tag": "매부리·휜코 재수술"},
            {"src": src('240'), "tag": "매부리·복코 동시"},
            {"src": src('207'), "tag": "복코 재수술"},
        ]
    },

    "faq": [
        {"q": "절골술은 어떤 경우에 하나요?", "a": seg('562', (137, 144)), "src": src('562')},
        {"q": "보형물 코수술에 절골을 같이 하면 염증이 생기나요?",
         "a": seg('562', (103, 105), (132, 134)), "src": src('562')},
        {"q": "매부리코가 휘어 있으면 절골은 어떻게 하나요?", "a": seg('nose/hump/185', (16, 22)), "src": src('nose/hump/185')},
        {"q": "절골하면 멍이 드나요?", "a": seg('225', (8, 10)), "src": src('225')},
        {"q": "콧대 가운데 아래쪽(비밸브)은 왜 좁히지 못하나요?", "a": seg('573', (31, 37)), "src": src('573')},
    ],

    "related": [
        {"href": "nose/hump", "name": "매부리코"},
        {"href": "nose/bulbous", "name": "복코"},
        {"href": "nose/septal", "name": "비중격연골 코성형"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/male", "name": "남자의 코성형"},
        {"href": "nostril/reduction", "name": "콧구멍축소술"},
    ],

    "review_banner_subject": "코 절골술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-osteotomy.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
