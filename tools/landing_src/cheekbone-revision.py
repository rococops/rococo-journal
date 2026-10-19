"""data/landing/cheekbone-revision.json 생성 (광대 재수술 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
광대 재수술 메뉴 칼럼(79·354·356·418)을 주로 쓰고, 광대 재수술에 관한 문장만 퀵광대 메뉴 칼럼(94·102·110)에서 가져온다.
(c185~c188 은 79 의 옛 글을 나눠 복제한 글이라 쓰지 않음)
사용: python tools/landing_src/cheekbone-revision.py   →  data/landing/cheekbone-revision.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'cheekbone/revision/'
Q = 'cheekbone/quick/'


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def qseg(n, *ranges):
    return L.seg(Q + n, *ranges)


def src(n):
    return f'{P}{n}'


def qsrc(n):
    return f'{Q}{n}'


# 수술 방법 단계 전용 아이콘 (공용에 없는 것만, 120x120)
ICON_XRAY = ('<rect x="20" y="18" width="80" height="84" rx="8" fill="#2f3438" stroke="#4a4a4a" stroke-width="2.2"/>'
             '<path d="M40 40 C48 30 72 30 80 40 C86 50 84 66 76 76 C70 84 50 84 44 76 C36 66 34 50 40 40 Z" fill="none" stroke="#e8e2d6" stroke-width="2.2"/>'
             '<path d="M44 62 L56 60 M76 62 L64 60" stroke="#c9a26f" stroke-width="2.6" stroke-linecap="round"/>'
             '<circle cx="52" cy="52" r="4" fill="none" stroke="#e8e2d6" stroke-width="1.8"/>'
             '<circle cx="68" cy="52" r="4" fill="none" stroke="#e8e2d6" stroke-width="1.8"/>')
ICON_INCISION = ('<path d="M22 70 C22 36 44 18 62 18 C84 18 98 36 98 62 C98 86 82 102 60 102 C40 102 22 90 22 70 Z" fill="#f1cfb8" stroke="#4a4a4a" stroke-width="2.2"/>'
                 '<path d="M30 52 C36 30 52 22 64 22 C80 22 92 32 96 50" fill="none" stroke="#5a4a3e" stroke-width="8" stroke-linecap="round"/>'
                 '<path d="M84 34 L92 44" stroke="#c46a5a" stroke-width="3.2" stroke-linecap="round"/>'
                 '<path d="M70 64 C76 60 84 62 88 68" fill="none" stroke="#b8956a" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="4 4"/>')
ICON_WASH = ('<path d="M60 22 C60 22 40 48 40 62 C40 74 49 82 60 82 C71 82 80 74 80 62 C80 48 60 22 60 22 Z" fill="#cfe3ec" stroke="#4a4a4a" stroke-width="2.2"/>'
             '<path d="M30 92 C40 86 50 98 60 92 C70 86 80 98 90 92" fill="none" stroke="#7aa6b8" stroke-width="2.4" stroke-linecap="round"/>'
             '<path d="M52 62 C52 56 55 52 58 50" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>')

data = {
    "_comment": "시술별 대표페이지 데이터(광대 재수술). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구.",
    "page": "cheekbone/revision",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "광대 재수술 | 광대축소술 후 효과가 부족할 때, 재수술이 도움이 되는 경우와 한계 | 로코코성형외과 김상호 원장",
        "description": "광대축소술 후 옆광대가 덜 들어갔거나 이전 고정 철사·나사가 남아 있는 경우의 광대 재수술. 퀵광대 방식 재수술이 도움이 되는 조건과 한계, 넣은 광대를 다시 빼는 광대재건술까지 김상호 원장의 글과 전후 X-ray로 정리했습니다.",
        "h1": "광대 재수술",
        "procedure_name": "광대 재수술"
    },

    "hero": {
        "eyebrow": "CHEEKBONE REVISION · 광대 재수술",
        "question": "광대 재수술은 어떤 경우에 도움이 되나요?",
        "summary": {"text": seg('79', (3, 5)), "src": src('79')},
        "stats": [
            {"from": 15, "to": 20, "unit": "분", "label": "수술 시간 (안내 15분 · 재수술 사례 20분)",
             "quote": seg('79', 8), "src": src('79'),
             "extra": [{"quote": seg('79', (92, 93)), "src": src('79')}]},
            {"from": 2, "to": 3, "unit": "mm", "label": "플레이트로 옆광대를 더 넣을 수 있는 정도",
             "quote": seg('79', (59, 62)), "src": src('79')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('79'), "image": "https://rococops.com/files/editor/1304003225.jpg",
                 "alt": "광대 재수술 전후 사진", "label": "CASE · 정면 재수술 2주", "layout": "stack"}
    },

    "features": {
        "type": "TYPE · CHEEKBONE REVISION",
        "toc": "재수술이 도움이 되는 경우",
        "title": seg('418', 19),
        "items": [seg('418', 20), seg('418', 21), seg('418', 22), seg('418', 23)],
        "note": seg('418', (15, 18)),
        "src": src('418')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "효과는 타고난 얼굴형에서 이미 정해집니다",
             "paras": [seg('79', (63, 65)), seg('79', (70, 71))], "src": src('79')},
            {"heading": "이전 고정 철사·나사가 남아 있는 경우",
             "paras": [seg('79', (73, 74)), seg('79', (80, 83))], "src": src('79')},
            {"heading": "x-ray에서 뼈가 벌어져 보여도",
             "paras": [qseg('102', (146, 148)), qseg('102', (230, 233))], "src": qsrc('102')},
            {"heading": "고정이 필요한 재수술, 필요 없는 재수술",
             "paras": [seg('354', (36, 46))], "src": src('354')},
        ]
    },

    "icons": {"xray": ICON_XRAY, "incision": ICON_INCISION, "wash": ICON_WASH},

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('79', 6), "icon": "xray"},
            {"text": seg('79', 7), "icon": "sleep"},
            {"text": seg('79', 182), "icon": "incision"},
            {"text": seg('79', 8), "icon": "clock"},
            {"text": seg('79', 11), "icon": "wash"},
        ],
        "steps_src": src('79'),
        "note": {"text": seg('79', (112, 115)), "src": src('79')},
        "pros_cons": {"paras": [seg('79', (174, 176)), seg('79', (180, 181)), seg('79', (199, 202))], "src": src('79')}
    },

    "recovery": {
        "title": "뼈가 굳는 시기와 재수술",
        "items": [
            {"label": "2주 (빼는 재수술)", "lines": [seg('354', (25, 35))], "src": src('354')},
            {"label": "2개월 (빼는 재수술)", "lines": [seg('354', (145, 149))], "src": src('354')},
            {"label": "1년", "lines": [seg('354', (72, 73))], "src": src('354')},
            {"label": "1년 6개월", "lines": [qseg('102', (104, 107))], "src": qsrc('102')},
        ],
        "note": {"text": qseg('110', (51, 55)), "src": qsrc('110')}
    },

    "before_after": {
        "title": "광대 재수술 전후",
        "alt": "광대 재수술 전후 사진",
        "items": [
            {"src": src('79'), "image": "https://rococops.com/files/editor/1304003225.jpg",
             "caption": seg('79', (154, 155)), "label": "정면 재수술 2주"},
            {"src": qsrc('94'), "image": "https://rococops.com/files/editor/1322189019.jpg",
             "caption": qseg('94', 138), "label": "X-ray 정면 · 재수술 1개월"},
            {"src": qsrc('94'), "image": "https://rococops.com/files/editor/1322189068.jpg",
             "caption": qseg('94', 141), "label": "X-ray 아래쪽 · 재수술 1개월"},
            {"src": src('354'), "image": "https://rococops.com/files/editor/202010301035051447882318.jpg",
             "caption": seg('354', 240), "label": "광대재건술 X-ray 정면"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('79'), "tag": "고정식 수술 후 재수술"},
            {"src": src('418'), "tag": "재수술 조건"},
            {"src": src('354'), "tag": "광대재건술"},
            {"src": src('356'), "tag": "퀵광대 재수술 논란"},
            {"src": qsrc('102'), "tag": "고정 vs 비고정 x-ray"},
            {"src": qsrc('110'), "tag": "45도 추가 수술"},
        ]
    },

    "faq": [
        {"q": "광대 재수술도 퀵광대 방식으로 할 수 있나요?", "a": seg('418', (10, 14)), "src": src('418')},
        {"q": "수술법을 바꾸면 재수술 효과가 더 좋아지나요?", "a": seg('79', (66, 69)), "src": src('79')},
        {"q": "다른 병원에서 고정식 광대축소술을 받았는데 재수술이 되나요?",
         "a": seg('79', (87, 90), (92, 93)), "src": src('79')},
        {"q": "넣었던 광대를 다시 빼는 재수술(광대재건술)도 가능한가요?",
         "a": seg('354', (212, 217), (223, 228)), "src": src('354')},
        {"q": "퀵광대를 받은 환자가 재수술을 많이 한다던데 사실인가요?",
         "a": seg('356', (178, 200)), "src": src('356')},
    ],

    "related": [
        {"href": "cheekbone/quick", "name": "퀵광대(15분 광대축소술)"},
        {"href": "cheekbone/rear", "name": "뒷광대축소술"},
        {"href": "cheekbone/fat-graft", "name": "심부볼·관자 지방이식"},
        {"href": "cheekbone/liposuction", "name": "광대라인 지방흡입"},
        {"href": "guide/quick-cheekbone-safety", "name": "퀵광대 위험한 수술인가요? (성형 가이드)"},
        {"href": "guide/cheekbone-reduction-methods", "name": "광대축소술 수술법 비교 (성형 가이드)"},
    ],

    "review_banner_subject": "광대 재수술",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'cheekbone-revision.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
