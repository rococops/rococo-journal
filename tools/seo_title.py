# 글 상세 페이지의 <title>/og:title 규칙 (원문 H1은 절대 수정하지 않고 메타 제목만 만든다)
#
# 예전에는 서브카테고리별 고정 문구("퀵광대 광대축소술 — 로코코성형외과 김상호 원장")를
# 그 카테고리의 모든 글에 똑같이 썼음 → 광대 글 151개가 전부 같은 제목이라 검색엔진이 서로
# 구별하지 못하고, 구축코를 다룬 글이어도 제목에 구축코가 없었음.
# 원장님이 직접 쓴 글 제목(H1)에는 이미 환자가 검색하는 표현이 들어 있으므로 그것을 제목으로 씀.
#
# 같은 규칙이 api/publish.js(seoTitle)에도 있음 — 수정 시 두 곳을 함께 맞출 것.
import re

BRAND_FULL = '로코코성형외과 김상호 원장'
BRAND_SHORT = '로코코성형외과'
MAX_LEN = 60          # 구글은 대략 60자 안팎에서 잘림

# 초기 케이스 기록처럼 제목이 날짜뿐인 글 (예: 2011.06.16, 2012.2.14, 2011.11)
_DATE_ONLY = re.compile(r'^\s*\d{4}\s*[.\-/]?\s*(\d{1,2}\s*[.\-/]?\s*)?(\d{1,2}\.?)?\s*$')


def _has_keyword(h1, keywords):
    """띄어쓰기 차이("관자 지방이식" vs "관자지방이식")를 무시하고, 카테고리 키워드와 3글자 이상 겹치는지 본다"""
    h = re.sub(r'\s+', '', h1)
    k = re.sub(r'[\s,/·]+', '', keywords or '')
    return any(k[i:i + 3] in h for i in range(len(k) - 2))


def seo_title(h1, keywords):
    """h1: 원장님 글 제목, keywords: 서브카테고리 대표 키워드(예: '퀵광대 광대축소술')"""
    h1 = re.sub(r'\s+', ' ', (h1 or '')).strip()
    keywords = (keywords or '').strip()

    # 제목이 날짜뿐이거나 지나치게 짧으면 그 자체로는 검색어가 될 수 없으므로 카테고리 키워드와 결합
    if not h1 or _DATE_ONLY.match(h1) or len(h1) < 6:
        label = h1.rstrip('. ')
        base = f'{keywords} ({label})' if label else keywords
    else:
        base = h1
        # H1에 카테고리 키워드가 전혀 없으면(예: "입체적인 얼굴형 만드는 법") 키워드를 덧붙임.
        # 단, 덧붙여서 너무 길어지면 원문 제목을 우선
        if keywords and not _has_keyword(h1, keywords):
            candidate = f'{h1} — {keywords}'
            if len(candidate) + len(f' | {BRAND_SHORT}') <= MAX_LEN:
                base = candidate

    full = f'{base} | {BRAND_FULL}'
    if len(full) > MAX_LEN:
        full = f'{base} | {BRAND_SHORT}'
    return full
