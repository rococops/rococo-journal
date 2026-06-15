"""mcolumn.sql 글을 제목(subject) 키워드 기반으로 36개 서브카테고리에 매핑.

날짜만 있는 제목 등 키워드로 분류 불가능한 경우, category 코드별 주제 기본값(CODE_DEFAULT)을 사용.
"""

# category 코드(4자리) -> (cat_path, sub_dir) 기본 매핑
# _mcolumn_cats.txt 에서 각 코드의 실제 글 내용을 확인해 결정한 주제 기본값
CODE_DEFAULT = {
    '0101': ('cheekbone', 'quick'),
    '0102': ('cheekbone', 'quick'),
    '0103': ('cheekbone', 'quick'),
    '0104': ('cheekbone', 'quick'),
    '0105': ('cheekbone', 'quick'),
    '0106': ('cheekbone', 'quick'),
    '0107': ('cheekbone', 'quick'),
    '0108': ('cheekbone', 'quick'),
    '0109': ('cheekbone', 'quick'),
    '0110': ('cheekbone', 'quick'),
    '0111': ('cheekbone', 'quick'),
    '0112': ('cheekbone', 'quick'),
    '0113': ('cheekbone', 'quick'),
    '0114': ('cheekbone', 'quick'),
    '0116': ('cheekbone', 'revision'),
    '0117': ('cheekbone', 'quick'),
    '0118': ('cheekbone', 'rear'),
    '0201': ('nose', 'column'),
    '0202': ('nose', 'rib-cartilage'),
    '0203': ('nose', 'septal'),
    '0204': ('nose', 'scarless'),
    '0205': ('nose', 'hump'),
    '0206': ('nose', 'bulbous'),
    '0207': ('nose', 'long'),
    '0210': ('nose', 'cat'),
    '0211': ('nose', 'male'),
    '0212': ('nose', 'rhinitis'),
    '0213': ('nostril', 'alar-base'),
    '0214': ('nostril', 'alar-lowering'),
    '0304': ('eye', 'correction'),
    '0306': ('eye', 'incision'),
    '0307': ('eye', 'double'),
    '0308': ('eye', 'incision'),
    '0309': ('eye', 'incision'),
    '0401': ('nostril', 'alar-lowering'),
    '0402': ('nostril', 'alar-raising'),
}

# 제목 키워드 우선순위 규칙: (조건함수, (cat_path, sub_dir))
def _rules(s):
    if '비공내리기' in s or '비공 내리기' in s or '콧구멍 가리' in s or '콧구멍가리' in s:
        return ('nostril', 'alar-lowering')
    if ('비공' in s and ('올리기' in s or '올림' in s)) or '콧날개올리기' in s or '콧날개 올리기' in s or '콧날개올림' in s:
        return ('nostril', 'alar-raising')
    if '콧볼' in s or '콧날개 줄이' in s or '콧날개축소' in s or '콧날개 축소' in s:
        return ('nostril', 'alar-base')
    if '콧구멍' in s and ('축소' in s or '줄이' in s):
        return ('nostril', 'reduction')
    if 'V형' in s or 'V자' in s:
        return ('nostril', 'v-shape')
    if '비주' in s:
        return ('nose', 'columella')
    if '고양이' in s or '입매교정' in s or '비순각' in s:
        return ('nose', 'cat')
    if '절골' in s:
        return ('nose', 'osteotomy')
    if '긴 코' in s or '긴코' in s:
        return ('nose', 'long')
    if '흉터없' in s or '흉터 없' in s or '비개방' in s:
        return ('nose', 'scarless')
    if '매부리' in s:
        return ('nose', 'hump')
    if '복코' in s:
        return ('nose', 'bulbous')
    if '비중격' in s:
        return ('nose', 'septal')
    if '비염' in s or '하비갑개' in s:
        return ('nose', 'rhinitis')
    if '남자' in s and '코' in s:
        return ('nose', 'male')
    if '재수술' in s and ('코' in s or '늑연골' in s or '들린코' in s):
        return ('nose', 'revision')
    if '늑연골' in s:
        return ('nose', 'rib-cartilage')
    if '눈매교정' in s:
        return ('eye', 'correction')
    if '쌍커풀' in s or '쌍꺼풀' in s:
        return ('eye', 'double')
    if '트임' in s:
        return ('eye', 'incision')
    if '눈썹' in s and '거상' in s:
        return ('eye', 'brow-lift')
    if '꺼진눈' in s or '꺼진 눈' in s:
        return ('eye', 'fat-graft')
    if '눈밑지방' in s or '눈밑 지방' in s:
        return ('eye', 'lower-fat')
    if '안검' in s:
        return ('anti-aging', 'blepharoplasty')
    if '실리프팅' in s or '엘라스티꿈' in s:
        return ('anti-aging', 'lifting')
    if '필러' in s or '보톡스' in s:
        return ('anti-aging', 'filler-botox')
    if '무턱' in s:
        return ('anti-aging', 'chin')
    if '미세지방' in s:
        return ('anti-aging', 'fat-graft')
    if '이마' in s and '거상' in s:
        return ('forehead', 'endoscopic')
    if '이마' in s and '축소' in s:
        return ('forehead', 'reduction')
    if '15분' in s or '변형15분' in s or '변형 15분' in s or '퀵광대' in s:
        return ('cheekbone', 'quick')
    if '뒷광대' in s:
        return ('cheekbone', 'rear')
    if '광대' in s and '재수술' in s:
        return ('cheekbone', 'revision')
    if '관자 지방이식' in s or '심부볼' in s:
        return ('cheekbone', 'fat-graft')
    if '광대' in s and '지방흡입' in s:
        return ('cheekbone', 'liposuction')
    if '광대' in s:
        return ('cheekbone', 'quick')
    return None


def classify(category, subject):
    """category(4자리 코드), subject(clean_text 적용된 제목) -> (cat_path, sub_dir)"""
    matched = _rules(subject)
    if matched:
        return matched
    return CODE_DEFAULT.get(category)
