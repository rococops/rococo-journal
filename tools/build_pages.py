"""sitecontents.sql -> 카테고리별 목록/상세 페이지 일괄 생성 스크립트.

SUBCATS 테이블에서 keywords가 None인 항목은 SEO 키워드가 아직 정해지지 않아 스킵한다.
"""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))

from sql_parse import iter_insert_tuples, split_tuple_fields, parse_field
from clean_content import build_article_blocks, clean_text, html_escape, first_paragraph_text
from mcolumn_map import classify as classify_mcolumn
from templates import (NAV_HTML, HEADER_HTML, FOOTER_HTML, CTA_SECTION_HTML,
                        DETAIL_PAGE, LIST_PAGE, CARD_HTML)

BASE = os.path.join(os.path.dirname(__file__), '..')
DEFAULT_IMG = 'https://rococops.com/images/main/mcs/2.jpg'

ACTIVE_KEYS = ['active_cheekbone', 'active_nose', 'active_nostril',
               'active_forehead', 'active_eye', 'active_anti_aging']

CAT_NAMES = {
    'cheekbone': '광대성형',
    'nose': '코성형',
    'nostril': '콧구멍성형',
    'forehead': '이마성형',
    'eye': '눈성형',
    'anti-aging': '동안성형',
}

ACTIVE_MAP = {
    'cheekbone': 'active_cheekbone',
    'nose': 'active_nose',
    'nostril': 'active_nostril',
    'forehead': 'active_forehead',
    'eye': 'active_eye',
    'anti-aging': 'active_anti_aging',
}

# (sql_categories, cat_path, sub_dir, sub_name, sub_name_en, keywords)
# keywords = None  ->  SEO 키워드 미정, 이번 배치에서 스킵
SUBCATS = [
    (['0101000000'], 'cheekbone', 'quick', '15분 광대축소술', 'Quick Cheekbone Reduction', '퀵광대 광대축소술'),
    (['0102000000'], 'cheekbone', 'fat-graft', '심부볼·관자 지방이식', 'Deep Cheek & Temple Fat Graft', '심부볼지방이식 관자지방이식'),
    (['0103000000'], 'cheekbone', 'liposuction', '광대라인 지방흡입', 'Cheekline Liposuction', '광대지방흡입 얼굴지방흡입'),
    (['0104000000'], 'cheekbone', 'rear', '뒷광대축소술', 'Rear Cheekbone Reduction', '뒷광대축소술 뒷광대'),
    (['0105000000'], 'cheekbone', 'revision', '광대 재수술', 'Cheekbone Revision', '광대재수술 광대수술재수술'),

    (['0201000000'], 'nose', 'column', '진료단상', 'Rhinoplasty Column', '코성형 코성형칼럼'),
    (['0202000000'], 'nose', 'revision', '코재수술', 'Rhinoplasty Revision', '코재수술 코성형재수술'),
    (['0203000000'], 'nose', 'rib-cartilage', '늑연골 명품코성형', 'Rib Cartilage Rhinoplasty', '자가늑연골 늑연골코성형'),
    (['0204000000'], 'nose', 'septal', '비중격연골 코성형', 'Septal Cartilage Rhinoplasty', '비중격연골코성형 비중격코성형'),
    (['0205000000'], 'nose', 'scarless', '흉터없는 코성형', 'Scarless Rhinoplasty', '흉터없는코성형 비개방코성형'),
    (['0206000000'], 'nose', 'hump', '매부리코', 'Hump Nose Correction', '매부리코 매부리코수술'),
    (['0207000000'], 'nose', 'bulbous', '복코', 'Bulbous Nose Correction', '복코성형 복코교정'),
    (['0208000000'], 'nose', 'osteotomy', '절골술', 'Osteotomy', '절골술 콧대좁히기'),
    (['0209000000'], 'nose', 'long', '긴코', 'Long Nose Correction', '긴코수술 긴코교정'),
    (['0210000000'], 'nose', 'columella', '비주성형', 'Columella Plasty', '비주내리기 비주성형'),
    (['0211000000'], 'nose', 'cat', '비순각 고양이 입매교정', 'Cat Eye Lip Line', '비순각수술 입매교정'),
    (['0212000000'], 'nose', 'male', '남자의 코성형', 'Rhinoplasty for Men', '남자코성형 남자성형'),
    (['0213000000'], 'nose', 'rhinitis', '비염수술', 'Rhinitis Surgery', '비염수술 하비갑개축소술'),

    (['0301000000'], 'nostril', 'alar-lowering', '비공내리기', 'Alar Lowering', '비공내리기 콧구멍내리기'),
    (['0302000000', '0303000000'], 'nostril', 'alar-raising', '콧날개올리기', 'Alar Raising', '콧날개올리기 콧날개성형'),
    (['0304000000'], 'nostril', 'v-shape', 'V형 콧구멍교정', 'V-shape Nostril Correction', 'V형콧구멍교정 콧구멍교정'),
    (['0305000000'], 'nostril', 'reduction', '콧구멍축소술', 'Nostril Reduction', '콧구멍축소술 콧구멍줄이기'),
    (['0306000000'], 'nostril', 'alar-base', '콧볼축소술', 'Alar Base Reduction', '콧볼축소술 콧볼줄이기'),

    (['0401000000'], 'forehead', 'endoscopic', '내시경 이마거상술', 'Endoscopic Brow Lift', '내시경이마거상술 이마거상술'),
    (['0402000000'], 'forehead', 'reduction', '이마축소술', 'Forehead Reduction', '이마축소술 이마성형'),

    (['0501000000', '0502000000'], 'eye', 'correction', '눈매교정술', 'Ptosis Correction', '눈매교정 비절개눈매교정'),
    (['0503000000'], 'eye', 'double', '쌍커풀 자연유착법', 'Natural Adhesion Double Eyelid', '쌍커풀수술 자연유착법'),
    (['0504000000', '0505000000', '0506000000'], 'eye', 'incision', '트임성형', 'Canthoplasty', '뒷트임 밑트임 앞트임'),
    (['0601000000'], 'eye', 'brow-lift', '눈썹하거상술', 'Sub-brow Lift', '눈썹하거상술 눈썹거상'),
    (['0603000000'], 'eye', 'fat-graft', '꺼진눈 지방이식', 'Sunken Eye Fat Graft', '꺼진눈지방이식 눈지방이식'),
    (['0604000000'], 'eye', 'lower-fat', '눈밑지방 재배치', 'Lower Eyelid Fat Repositioning', '눈밑지방재배치 눈밑성형'),

    (['0602000000', '0605000000'], 'anti-aging', 'blepharoplasty', '상·하안검성형', 'Upper & Lower Blepharoplasty', '상안검성형 하안검성형'),
    (['0606000000'], 'anti-aging', 'lifting', '엘라스티꿈 실리프팅', 'Elasticum Thread Lift', '실리프팅 엘라스티꿈리프팅'),
    (['0607000000'], 'anti-aging', 'filler-botox', '필러·보톡스', 'Filler & Botox', '필러 보톡스'),
    (['0701000000'], 'anti-aging', 'chin', '무턱성형', 'Chin Augmentation', '무턱수술 무턱성형'),
    (['0702000000', '0703000000'], 'anti-aging', 'fat-graft', '미세지방이식', 'Micro Fat Grafting', '미세지방이식 지방이식'),
]


def nav(root, active_key):
    active = {k: ('active' if k == active_key else '') for k in ACTIVE_KEYS}
    return NAV_HTML.format(root=root, **active)


def header(root, active_key):
    return HEADER_HTML.format(root=root, nav=nav(root, active_key))


def footer(root):
    return FOOTER_HTML.format(root=root)


def truncate(text, n):
    text = text.strip()
    if len(text) <= n:
        return text
    return text[:n].rstrip() + '...'


def load_all_rows_by_category(sql):
    """sitecontents.sql을 한 번만 순회하여 category 코드별로 행을 묶어서 반환."""
    by_category = defaultdict(list)
    for tup in iter_insert_tuples(sql, 'sitecontents'):
        fields = split_tuple_fields(tup)
        if len(fields) != 15:
            continue
        (num, category, subject, summary, contents, mcontents,
         attach1, attach2, attach3, visited, udate, rank,
         ishtml, isupdate, part) = [parse_field(f) for f in fields]
        by_category[category].append({
            'num': int(num),
            'slug': str(int(num)),
            'subject': clean_text(subject or ''),
            'summary': clean_text(summary or ''),
            'contents': contents or '',
        })
    return by_category


def load_rows(by_category, category_codes):
    rows = []
    for code in category_codes:
        rows.extend(by_category.get(code, []))
    return rows


def load_mcolumn_rows(sql):
    """mcolumn.sql 전체 행을 로드하고, 제목 키워드 기반으로 (cat_path, sub_dir)를 분류해서 반환.
    folder slug는 sitecontents의 num과 충돌하지 않도록 'c{num}' 형태로 만든다."""
    rows = []
    unmapped = []
    for tup in iter_insert_tuples(sql, 'mcolumn'):
        fields = split_tuple_fields(tup)
        if len(fields) != 15:
            continue
        (num, category, subject, rdate, contents, attach1, attach2, attach3,
         visited, udate, isnoti, ishtml, ip, rank, isview) = [parse_field(f) for f in fields]

        title = clean_text(subject or '')
        loc = classify_mcolumn(category, title)
        if loc is None:
            unmapped.append((num, category, title))
            continue
        cat_path, sub_dir = loc

        description = first_paragraph_text(contents or '') or title
        rows.append({
            'num': int(num),
            'slug': f'c{int(num)}',
            'subject': title,
            'summary': clean_text(description),
            'contents': contents or '',
            'cat_path': cat_path,
            'sub_dir': sub_dir,
        })

    if unmapped:
        print(f'경고: 분류되지 않은 mcolumn 글 {len(unmapped)}개')
        for num, category, title in unmapped:
            print(f'  num={num} category={category} subject={title!r}')

    return rows


def og_url_for(cat_path, sub_dir, slug):
    return f'https://journal.rococops.com/{cat_path}/{sub_dir}/{slug}/'


def build_canonical_map(all_rows):
    """all_rows: list of (num, slug, title, cat_path, sub_dir). 같은 title을 가진 글 중
    num이 가장 작은 글을 원본으로 보고, 나머지는 canonical을 원본 URL로 지정."""
    groups = defaultdict(list)
    for num, slug, title, cat_path, sub_dir in all_rows:
        if title:
            groups[title].append((num, slug, cat_path, sub_dir))

    canonical = {}
    for title, items in groups.items():
        if len(items) < 2:
            continue
        original = min(items, key=lambda x: x[0])
        original_url = og_url_for(original[2], original[3], original[1])
        for num, slug, cat_path, sub_dir in items:
            if slug != original[1]:
                canonical[slug] = original_url
    return canonical


def build_subcat(cfg, rows, canonical_map):
    sql_categories, cat_path, sub_dir, sub_name, sub_name_en, keywords = cfg

    if keywords is None:
        print(f'스킵 (SEO 키워드 미지정): {cat_path}/{sub_dir} ({sub_name})')
        return

    cat_name = CAT_NAMES[cat_path]
    active_key = ACTIVE_MAP[cat_path]
    meta_title = f'{keywords} — 로코코성형외과 김상호 원장'
    img_alt = f'{keywords} 로코코성형외과'

    if not rows:
        print(f'경고: 데이터 없음: {cat_path}/{sub_dir}')
        return

    out_dir = os.path.join(BASE, cat_path, sub_dir)
    os.makedirs(out_dir, exist_ok=True)

    cards = []
    for row in rows:
        slug = row['slug']
        title = row['subject']
        description = row['summary'] or title
        content_html, images = build_article_blocks(row['contents'], img_alt)
        hero_image = images[0] if images else DEFAULT_IMG

        post_dir = os.path.join(out_dir, slug)
        os.makedirs(post_dir, exist_ok=True)

        root = '../../../'
        list_root = '../'
        og_url = og_url_for(cat_path, sub_dir, slug)
        canonical_url = canonical_map.get(slug, og_url)

        page = DETAIL_PAGE.format(
            title=html_escape(title),
            title_short=html_escape(truncate(title, 24)),
            title_json=title.replace('"', '\\"'),
            meta_title=html_escape(meta_title),
            description=html_escape(description),
            description_json=description.replace('"', '\\"'),
            og_image=hero_image,
            og_url=og_url,
            canonical_url=canonical_url,
            img_alt=html_escape(img_alt),
            root=root,
            header=header(root, active_key),
            footer=footer(root),
            cat_path=cat_path,
            cat_name=cat_name,
            sub_name=sub_name,
            sub_name_en=sub_name_en,
            list_root=list_root,
            hero_image=hero_image,
            content=content_html,
            cta_section=CTA_SECTION_HTML.format(root=root, cat_name=sub_name),
        )

        with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page)

        cards.append(CARD_HTML.format(
            num=slug,
            img=hero_image,
            title=html_escape(truncate(title, 60)),
            desc=html_escape(truncate(description, 70)),
            sub_name=sub_name,
        ))

    # 목록 페이지 생성
    root = '../../'
    list_description = f'{sub_name}({len(rows)}개 케이스) — 로코코성형외과 김상호 원장의 {sub_name} 시술 케이스 모음'
    list_page = LIST_PAGE.format(
        sub_name=sub_name,
        sub_name_en=sub_name_en,
        description=html_escape(list_description),
        og_image=DEFAULT_IMG,
        og_url=f'https://journal.rococops.com/{cat_path}/{sub_dir}/',
        root=root,
        header=header(root, active_key),
        footer=footer(root),
        cat_path=cat_path,
        cat_name=cat_name,
        count=len(rows),
        cards='\n'.join(cards),
        cta_section=CTA_SECTION_HTML.format(root=root, cat_name=sub_name),
    )

    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(list_page)

    print(f'완료: {cat_path}/{sub_dir} - {len(rows)}개 상세페이지 + 목록페이지')


def main():
    sql_path = os.path.join(BASE, 'sitecontents.sql')
    with open(sql_path, encoding='utf-8') as f:
        sql = f.read()

    mcolumn_path = os.path.join(BASE, 'mcolumn.sql')
    with open(mcolumn_path, encoding='utf-8') as f:
        mcolumn_sql = f.read()

    mcolumn_rows = load_mcolumn_rows(mcolumn_sql)
    mcolumn_by_loc = defaultdict(list)
    for row in mcolumn_rows:
        mcolumn_by_loc[row['cat_path'], row['sub_dir']].append(row)

    by_category = load_all_rows_by_category(sql)

    # 1차: 모든 서브카테고리의 행을 미리 로드하고 중복글(canonical) 매핑 계산
    cfg_rows = {}
    all_rows = []
    for cfg in SUBCATS:
        sql_categories, cat_path, sub_dir, sub_name, sub_name_en, keywords = cfg
        if keywords is None:
            continue
        rows = load_rows(by_category, sql_categories)
        rows += mcolumn_by_loc.get((cat_path, sub_dir), [])
        cfg_rows[sub_dir, cat_path] = rows
        for row in rows:
            all_rows.append((row['num'], row['slug'], row['subject'], cat_path, sub_dir))

    canonical_map = build_canonical_map(all_rows)
    print(f'중복글 그룹: {sum(1 for n in canonical_map.values())}개 글에 canonical 적용')
    print(f'mcolumn 추가: {len(mcolumn_rows)}개')

    # 2차: 페이지 생성
    for cfg in SUBCATS:
        sql_categories, cat_path, sub_dir, sub_name, sub_name_en, keywords = cfg
        if keywords is None:
            print(f'스킵 (SEO 키워드 미지정): {cat_path}/{sub_dir} ({sub_name})')
            continue
        rows = cfg_rows[sub_dir, cat_path]
        build_subcat(cfg, rows, canonical_map)


if __name__ == '__main__':
    main()
