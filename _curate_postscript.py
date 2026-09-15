# postscript_safe.json → 저널용 후보 선별
# 1) 실질 내용 있는 글만 (빈 글/한글자 낙서 제외)
# 2) 기존 mcolumn_map.py 분류 로직으로 시술 카테고리 매칭
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
    cat = classify(r['category'], r['subject'] + ' ' + r['contents_text'][:200])
    cands.append({**r, 'score': round(sc,1), 'cat': cat, 'flag_bad': any(k in r['contents_text'] for k in BAD_KW)})

cands.sort(key=lambda x: -x['score'])

print(f"점수 매겨진 후보: {len(cands)}건 (전체 {len(rows)}건 중, 300자 미만 제외)\n")

print("=== 카테고리 분류 실패(수동 확인 필요) 상위 10건 ===")
unmapped = [c for c in cands if not c['cat']][:10]
for c in unmapped:
    print(f"  num={c['num']:>4} score={c['score']:>5} | {c['subject'][:40]}")
print(f"  (분류 실패 총 {len([c for c in cands if not c['cat']])}건 / {len(cands)}건)\n")

print("=== 상위 30건 (저널 후보) ===")
for c in cands[:30]:
    cat = f"{c['cat'][0]}/{c['cat'][1]}" if c['cat'] else "미분류"
    flag = " ⚠️불만어감" if c['flag_bad'] else ""
    print(f"  num={c['num']:>4} score={c['score']:>5} [{cat:<22}] {c['udate'][:7]} {c['contents_len']:>5}자 사진{len(c['photos'])} | {c['subject'][:40]}{flag}")

with open('postscript_curated.json', 'w', encoding='utf-8') as f:
    json.dump(cands, f, ensure_ascii=False, indent=1)
print(f"\n전체 점수화 결과 저장: postscript_curated.json ({len(cands)}건)")
