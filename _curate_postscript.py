# postscript_safe.json → 저널용 후보 선별
# 1) 실질 내용 있는 글만 (빈 글/한글자 낙서 제외)
# 2) 제목(subject)에서 매칭되는 시술 키워드를 전부 뽑아 다중 카테고리로 태그
#    (빈님 확인: "제목에 보이는 모든 키워드를 카테고리로 잡는걸로" — 복합시술 후기가
#    여러 카테고리 리스트에 다 노출되게. 본문 텍스트는 보지 않음 — 예전엔 본문 앞부분까지
#    봐서 "저번에 코수술 받았었는데 오늘은 광대수술..." 같은 글이 본문의 "복코" 때문에
#    코성형으로 잘못 분류되는 문제가 있었음(예: num=596))
# 3) 장기경과·상세도 기준 점수화 → 상위 후보 리스트 출력 (전문 아님, 검토용 요약만)
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'tools')
from mcolumn_map import classify

with open('postscript_safe.json', encoding='utf-8') as f:
    rows = json.load(f)

LONGTERM_KW = ['년차', '년째', '주년', '개월째', '개월차', '경과', '추가후기', '재후기']
GOOD_KW = ['만족', '감사', '후기', '추천']
BAD_KW = ['환불', '불만', '실망']  # 있어도 배제하진 않되 검토 시 표시만

# mcolumn_map.py의 _rules()와 동일한 키워드 규칙을 "첫 매칭에서 멈추지 않고 전부 수집"하도록 재구성.
# 대표 카테고리(cats[0], 캐노니컬 페이지 위치)는 규칙 순서가 아니라 "제목에 실제로 먼저
# 등장하는 키워드"를 기준으로 정함 — 안 그러면 "15분 광대축소술+...+턱보톡스"처럼 부가
# 시술(보톡스)이 룰 순서상 앞서서 엉뚱하게 대표로 잡히는 문제가 생김.
def _rules_all(s):
    out = []  # (position, cat)
    def add(cond, keywords, cat):
        # keywords: 이 규칙을 매칭시켰을 수 있는 후보 부분문자열들 — 실제 등장 위치 중 가장 이른 것을 사용
        if cond:
            positions = [s.find(k) for k in keywords if k in s]
            pos = min(positions) if positions else len(s)
            out.append((pos, cat))
    add('비공내리기' in s or '비공 내리기' in s or '콧구멍 가리' in s or '콧구멍가리' in s,
        ['비공내리기', '비공 내리기', '콧구멍 가리', '콧구멍가리'], ('nostril', 'alar-lowering'))
    add(('비공' in s and ('올리기' in s or '올림' in s)) or '콧날개올리기' in s or '콧날개 올리기' in s or '콧날개올림' in s,
        ['비공', '콧날개올리기', '콧날개 올리기', '콧날개올림'], ('nostril', 'alar-raising'))
    add('콧볼' in s or '콧날개 줄이' in s or '콧날개축소' in s or '콧날개 축소' in s,
        ['콧볼', '콧날개 줄이', '콧날개축소', '콧날개 축소'], ('nostril', 'alar-base'))
    add('콧구멍' in s and ('축소' in s or '줄이' in s), ['콧구멍'], ('nostril', 'reduction'))
    add('V형' in s or 'V자' in s, ['V형', 'V자'], ('nostril', 'v-shape'))
    add('비주' in s, ['비주'], ('nose', 'columella'))
    add('고양이' in s or '입매교정' in s or '비순각' in s, ['고양이', '입매교정', '비순각'], ('nose', 'cat'))
    add('절골' in s, ['절골'], ('nose', 'osteotomy'))
    add('긴 코' in s or '긴코' in s, ['긴 코', '긴코'], ('nose', 'long'))
    add('흉터없' in s or '흉터 없' in s or '비개방' in s, ['흉터없', '흉터 없', '비개방'], ('nose', 'scarless'))
    add('매부리' in s, ['매부리'], ('nose', 'hump'))
    add('복코' in s, ['복코'], ('nose', 'bulbous'))
    add('비중격' in s, ['비중격'], ('nose', 'septal'))
    add('비염' in s or '하비갑개' in s, ['비염', '하비갑개'], ('nose', 'rhinitis'))
    add('남자' in s and '코' in s, ['남자'], ('nose', 'male'))
    add('재수술' in s and ('코' in s or '늑연골' in s or '들린코' in s), ['재수술'], ('nose', 'revision'))
    add('늑연골' in s, ['늑연골'], ('nose', 'rib-cartilage'))
    add('눈매교정' in s, ['눈매교정'], ('eye', 'correction'))
    add('쌍커풀' in s or '쌍꺼풀' in s, ['쌍커풀', '쌍꺼풀'], ('eye', 'double'))
    add('트임' in s, ['트임'], ('eye', 'incision'))
    add('눈썹' in s and '거상' in s, ['눈썹'], ('eye', 'brow-lift'))
    add('꺼진눈' in s or '꺼진 눈' in s, ['꺼진눈', '꺼진 눈'], ('eye', 'fat-graft'))
    add('눈밑지방' in s or '눈밑 지방' in s, ['눈밑지방', '눈밑 지방'], ('eye', 'lower-fat'))
    add('안검' in s, ['안검'], ('anti-aging', 'blepharoplasty'))
    add('실리프팅' in s or '엘라스티꿈' in s, ['실리프팅', '엘라스티꿈'], ('anti-aging', 'lifting'))
    add('필러' in s or '보톡스' in s, ['필러', '보톡스'], ('anti-aging', 'filler-botox'))
    add('무턱' in s, ['무턱'], ('anti-aging', 'chin'))
    add('미세지방' in s, ['미세지방'], ('anti-aging', 'fat-graft'))
    add('이마' in s and '지방' in s, ['이마'], ('anti-aging', 'fat-graft'))  # 이마 지방이식 — 빈님 확인(num=30)
    add('이마' in s and '거상' in s, ['이마'], ('forehead', 'endoscopic'))
    add('이마' in s and '축소' in s, ['이마'], ('forehead', 'reduction'))
    add('15분' in s or '변형15분' in s or '변형 15분' in s or '퀵광대' in s,
        ['15분', '변형15분', '변형 15분', '퀵광대'], ('cheekbone', 'quick'))
    add('뒷광대' in s, ['뒷광대'], ('cheekbone', 'rear'))
    add('광대' in s and '재수술' in s, ['광대'], ('cheekbone', 'revision'))
    add('관자 지방이식' in s or '심부볼' in s, ['관자 지방이식', '심부볼'], ('cheekbone', 'fat-graft'))
    add('광대' in s and '지방흡입' in s, ['광대'], ('cheekbone', 'liposuction'))
    add('광대' in s, ['광대'], ('cheekbone', 'quick'))
    # 세부 시술명 없이 "코"/"명품코"만 있는 경우 — 간판 시술(늑연골 명품코성형)로 기본 배정.
    # 이미 더 구체적인 nose 카테고리가 잡혔으면(예: 복코 안에 '코'가 포함됨) 중복 태그하지 않음
    if '코' in s and not any(c[0] == 'nose' for _, c in out):
        add(True, ['명품코', '코'], ('nose', 'rib-cartilage'))
    # 제목 내 등장 위치 순으로 정렬(먼저 나온 시술이 대표), 카테고리 중복 제거(첫 등장만 유지)
    out.sort(key=lambda x: x[0])
    seen = set()
    result = []
    for _, cat in out:
        if cat not in seen:
            seen.add(cat)
            result.append(cat)
    return result

def score(r):
    text = r['subject'] + ' ' + r['contents_text']
    s = 0
    n = r['contents_len']
    if n < 300: return -999  # 너무 짧음 — 소스로 부적합
    s += min(n, 3000) / 100  # 길이 가점 (최대 30점)
    if any(k in text for k in LONGTERM_KW): s += 25  # 장기경과 — 가장 중요한 가점
    if any(k in text for k in GOOD_KW): s += 5
    if r['photos']: s += 10
    if r['isbest'] == 'Y': s += 15
    if r['isauth'] == 'Y': s += 5
    return s

cands = []
for r in rows:
    sc = score(r)
    if sc <= 0:
        continue
    cats = _rules_all(r['subject'])
    if not cats:
        # 제목만으로 매칭 안 되면(순수 감사글 등 시술 단서가 제목에 없는 경우) 본문 전체로
        # 확장(빈님 확인: "본문 전체를 봐야겠는데" — 앞 300자 안에 키워드가 없는 경우가 있었음)
        cats = _rules_all(r['subject'] + ' ' + r['contents_text'])
        if not cats:
            # 그래도 안 되면 작성자 닉네임도 확인(빈님 확인: "광대이제그만"처럼 닉네임 자체가
            # 시술을 가리키는 경우가 있음)
            cats = _rules_all(r['writer'] or '')
        if not cats:
            fallback = classify(r['category'], r['subject'] + ' ' + r['contents_text'][:200])
            cats = [fallback] if fallback else []
    cat = cats[0] if cats else None  # 대표 카테고리 — 개별 페이지가 실제로 생성되는 위치
    cands.append({**r, 'score': round(sc,1), 'cat': cat, 'cats': cats, 'flag_bad': any(k in r['contents_text'] for k in BAD_KW)})

# 그래도 미분류인 글은 같은 작성자 닉네임의 다른(이미 분류된) 글에서 카테고리를 빌려옴
# — 빈님 확인: "동명이인이 올린 2차후기 아닐까" (예: num=406 "지방2차 사진 다시 올려요"는
# 같은 작성자 num=407의 후속글이고 407은 이미 코성형으로 분류돼 있었음)
by_writer = {}
for c in cands:
    if c['cat'] and c['writer']:
        by_writer.setdefault(c['writer'], c['cat'])
for c in cands:
    if not c['cat'] and c['writer'] in by_writer:
        c['cat'] = by_writer[c['writer']]
        c['cats'] = [c['cat']]

# 그래도 안 잡히면 "기타"로 — 빈님 확인: "남은건 그냥 기타 카테고리 만들어서 넣어줘"
for c in cands:
    if not c['cat']:
        c['cat'] = ('etc', 'general')
        c['cats'] = [c['cat']]

cands.sort(key=lambda x: -x['score'])

print(f"점수 매겨진 후보: {len(cands)}건 (전체 {len(rows)}건 중, 300자 미만 제외)\n")

multi = [c for c in cands if len(c['cats']) > 1]
print(f"복수 카테고리 태그된 글: {len(multi)}건\n")

print("=== 카테고리 분류 실패(수동 확인 필요) 상위 10건 ===")
unmapped = [c for c in cands if not c['cat']][:10]
for c in unmapped:
    print(f"  num={c['num']:>4} score={c['score']:>5} | {c['subject'][:40]}")
print(f"  (분류 실패 총 {len([c for c in cands if not c['cat']])}건 / {len(cands)}건)\n")

print("=== 상위 30건 (저널 후보) ===")
for c in cands[:30]:
    cat = f"{c['cat'][0]}/{c['cat'][1]}" if c['cat'] else "미분류"
    extra = f" +{len(c['cats'])-1}개 더" if len(c['cats']) > 1 else ""
    flag = " ⚠️불만어감" if c['flag_bad'] else ""
    print(f"  num={c['num']:>4} score={c['score']:>5} [{cat:<22}]{extra} {c['udate'][:7]} {c['contents_len']:>5}자 사진{len(c['photos'])} | {c['subject'][:40]}{flag}")

with open('postscript_curated.json', 'w', encoding='utf-8') as f:
    json.dump(cands, f, ensure_ascii=False, indent=1)
print(f"\n전체 점수화 결과 저장: postscript_curated.json ({len(cands)}건)")
