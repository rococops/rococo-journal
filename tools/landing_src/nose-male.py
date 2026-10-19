"""data/landing/nose-male.json 생성 (남자의 코성형 대표페이지).
원장님 문장은 직접 타이핑하지 않고 칼럼 본문의 줄 범위(landing_lib.py dump 의 줄 번호)를 그대로 이어붙여 만든다.
사용: python tools/landing_src/nose-male.py   →  data/landing/nose-male.json
"""
import sys, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import landing_lib as L
sys.stdout.reconfigure(encoding='utf-8')
P = 'nose/male/'


def seg(n, *ranges):
    return L.seg(P + n, *ranges)


def src(n):
    return f'{P}{n}'


data = {
    "_comment": "시술별 대표페이지 데이터(남자의 코성형). 원장님 글은 1인칭 칼럼 원문 그대로만 사용(가이드 3인칭 요약은 인용하지 않음). 문장 단위 대조: tools/verify_landing_quotes.py. 소제목·질문형 부제·라벨은 제작 문구. 복제본(c134=17, c112=230, c113=233, 237≈203)은 숫자 번호 글을 src로 씀.",
    "page": "nose/male",

    "seo": {
        "_comment": "apply=false 이면 <title>·description·H1·구조화데이터는 지금 그대로 둔다.",
        "apply": True,
        "title": "남자 코성형 | 남자 매부리코·휜코 교정, 여자 코와 다른 디자인 | 로코코성형외과 김상호 원장",
        "description": "남자 코성형은 코끝 각도·미간 높이·일자 콧대처럼 여자 코와 디자인이 다르고, 피부가 두껍고 질겨 수술이 더 까다롭습니다. 남자 매부리코·휜코 교정 방법과 한계, 수술 후 경과를 김상호 원장의 글로 정리했습니다.",
        "h1": "남자 코성형",
        "procedure_name": "남자 코성형"
    },

    "hero": {
        "eyebrow": "MALE RHINOPLASTY · 남자 코성형",
        "question": "남자 코성형은 무엇이 다른가요?",
        "summary": {"text": seg('17', (11, 12)), "src": src('17')},
        "stats": [
            {"to": 20, "unit": "%", "label": "집도 수술 중 남자 환자 비율 (최소)",
             "quote": seg('612', 8), "src": src('612')},
            {"to": 80, "unit": "%", "label": "안면비대칭 중 인중 축이 우측으로 돌아간 경우 (원장 경험)",
             "quote": seg('314', 41).rstrip(','), "src": src('314')},
            {"to": 1, "unit": "년", "label": "최종 경과를 보는 시점",
             "quote": seg('314', (83, 84)), "src": src('314')},
        ],
        "bg_image": "images/landing/nose-hump-hero.jpg",
        "case": {"src": src('338'), "image": "https://rococops.com/files/editor/202007011144341946882598.jpg",
                 "alt": "남자 매부리코·휜코 수술 전후 정면 사진", "label": "CASE · 정면 3개월", "layout": "stack"}
    },

    "features": {
        "type": "DESIGN · MALE NOSE",
        "toc": "남자 코의 특징",
        "title": seg('17', (5, 6)),
        "items": [seg('17', (7, 8)), seg('17', 9).rstrip(','), seg('17', 10)],
        "note": seg('17', (17, 19)),
        "src": src('17')
    },

    "story": {
        "title": "김상호 원장 이야기",
        "blocks": [
            {"heading": "남자 환자분들이 많이 늘었습니다",
             "paras": [seg('612', (6, 10))], "src": src('612')},
            {"heading": "남자 매부리코, 여자와 다를까요?",
             "paras": [seg('338', (13, 16)), seg('338', (17, 21))], "src": src('338')},
            {"heading": "휜코의 가장 큰 원인은 안면비대칭입니다",
             "paras": [seg('314', (30, 36)), seg('314', (37, 42))], "src": src('314')},
            {"heading": "얼굴 축이 틀어진 휜코의 한계",
             "paras": [seg('338', (38, 41)), seg('338', (92, 95))], "src": src('338')},
        ]
    },

    "method": {
        "title": "수술 방법",
        "steps": [
            {"text": seg('338', (139, 140)), "icon": "sleep"},
            {"text": seg('338', (124, 125)).rstrip(','), "icon": "tip"},
            {"text": seg('338', 126), "icon": "hump"},
            {"text": seg('338', 127), "icon": "fill"},
            {"text": seg('338', (145, 147)), "icon": "deviation"},
        ],
        "steps_src": src('338'),
        "note": {"text": seg('338', (128, 129)), "src": src('338')},
        "pros_cons": {"paras": [' '.join(L.lines(src('338'))[71:82]),  # 77줄 '- ' 원문 유지(seg는 줄머리 '- '를 뗌)
                                 seg('338', (82, 85))], "src": src('338')}
    },

    "recovery": {
        "title": "수술 후 경과",
        "items": [
            {"label": "붓기", "lines": [seg('230', 14)], "src": src('230')},
            {"label": "3개월", "lines": [seg('338', (116, 120))], "src": src('338')},
            {"label": "호흡", "lines": [seg('338', (86, 91))], "src": src('338')},
            {"label": "1년", "lines": [seg('314', (83, 87))], "src": src('314')},
            {"label": "코끝을 많이 높였다면", "lines": [seg('612', (49, 53))], "src": src('612')},
        ],
        "note": {"text": seg('101', 11), "src": src('101')}
    },

    "before_after": {
        "title": "남자 코성형 전후",
        "alt": "남자 코성형 수술 전후 사진",
        "items": [
            {"src": src('338'), "image": "https://rococops.com/files/editor/202007011144341946882598.jpg",
             "caption": "정면 수술전과 수술 후 3개월째 사진입니다.", "label": "매부리코·휜코 정면 3개월"},
            {"src": src('338'), "image": "https://rococops.com/files/editor/20200701114451596040831.jpg",
             "caption": "우사면 수술 전과 수술 후 3개월째 사진입니다.", "label": "우사면 3개월"},
            {"src": src('338'), "image": "https://rococops.com/files/editor/202007011145081520496504.jpg",
             "caption": "우측면 수술전후 사진입니다.", "label": "측면"},
            {"src": src('338'), "image": "https://rococops.com/files/editor/20200701114517476597136.jpg",
             "caption": "좌사면 전후사진입니다.", "label": "좌사면"},
            {"src": src('314'), "image": "https://rococops.com/files/editor/202002281452322136557617.jpg",
             "caption": "수술전과 수술 후 2주째 사진입니다.", "label": "휜코 정면 2주"},
            {"src": src('314'), "image": "https://rococops.com/files/editor/20200228145307748988585.jpg",
             "caption": "아래쪽에서 본 사진에서", "label": "휜코 아래쪽에서"},
            {"src": src('203'), "image": "https://rococops.com/files/editor/1303221317.jpg",
             "caption": "정면모습입니다.", "label": "무보형물 매부리코 정면"},
            {"src": src('101'), "image": "https://rococops.com/files/editor/1342968212.jpg",
             "caption": "우사면입니다.", "label": "무보형물 매부리코 사면"},
        ]
    },

    "logs": {
        "title": "대표 사례 — 원장 기록",
        "items": [
            {"src": src('338'), "tag": "남자 매부리코·휜코"},
            {"src": src('314'), "tag": "휜코 원인·한계"},
            {"src": src('17'), "tag": "남자 코 디자인"},
            {"src": src('612'), "tag": "남자 코재수술"},
            {"src": src('203'), "tag": "무보형물 매부리코"},
            {"src": src('230'), "tag": "휜코·복코·매부리"},
        ]
    },

    "faq": [
        {"q": "비중격만곡증이 있으면 꼭 펴야 하나요?", "a": seg('314', (17, 29)), "src": src('314')},
        {"q": "콧구멍이 M자 모양인데 코끝을 높이면 어떻게 되나요?", "a": seg('338', (42, 51)), "src": src('338')},
        {"q": "보형물 없이 매부리코를 교정하면 굴곡이 남지 않나요?", "a": seg('338', (159, 162)), "src": src('338')},
        {"q": "매부리코 교정은 어떤 방법이 있나요?", "a": seg('203', (7, 8)), "src": src('203')},
        {"q": "비주가 말려 들어간 남자 코도 교정할 수 있나요?", "a": seg('612', (16, 17)), "src": src('612')},
    ],

    "related": [
        {"href": "nose/hump", "name": "매부리코 수술"},
        {"href": "nose/septal", "name": "비중격연골 코성형"},
        {"href": "nose/osteotomy", "name": "절골술"},
        {"href": "nose/revision", "name": "코재수술"},
        {"href": "nose/rib-cartilage", "name": "자가늑연골 코성형"},
        {"href": "nose/rhinitis", "name": "비염수술"},
    ],

    "review_banner_subject": "남자 코성형",
    "cases_visible": 9
}

out = os.path.join(ROOT, 'data', 'landing', 'nose-male.json')
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', os.path.normpath(out))
