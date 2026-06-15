import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from sql_parse import iter_insert_tuples, split_tuple_fields, parse_field
from clean_content import build_article_blocks, clean_text, html_escape
from templates import (NAV_HTML, HEADER_HTML, FOOTER_HTML, CTA_SECTION_HTML,
                        DETAIL_PAGE, LIST_PAGE, CARD_HTML)

BASE = os.path.join(os.path.dirname(__file__), '..')
CATEGORY_CODE = '0301000000'

CAT_PATH = 'nostril'
CAT_NAME = '콧구멍성형'
SUB_DIR = 'alar-lowering'
SUB_NAME = '비공내리기'
SUB_NAME_EN = 'Alar Lowering'
DEFAULT_IMG = 'https://rococops.com/images/main/mcs/2.jpg'

ACTIVE = {
    'active_cheekbone': '',
    'active_nose': '',
    'active_nostril': 'active',
    'active_forehead': '',
    'active_eye': '',
    'active_anti_aging': '',
}


def nav(root):
    return NAV_HTML.format(root=root, **ACTIVE)


def header(root):
    return HEADER_HTML.format(root=root, nav=nav(root))


def footer(root):
    return FOOTER_HTML.format(root=root)


def truncate(text, n):
    text = text.strip()
    if len(text) <= n:
        return text
    return text[:n].rstrip() + '...'


def main():
    sql_path = os.path.join(BASE, 'sitecontents.sql')
    with open(sql_path, encoding='utf-8') as f:
        sql = f.read()

    rows = []
    for tup in iter_insert_tuples(sql, 'sitecontents'):
        fields = split_tuple_fields(tup)
        if len(fields) != 15:
            continue
        (num, category, subject, summary, contents, mcontents,
         attach1, attach2, attach3, visited, udate, rank,
         ishtml, isupdate, part) = [parse_field(f) for f in fields]
        if category != CATEGORY_CODE:
            continue
        rows.append({
            'num': int(num),
            'subject': clean_text(subject or ''),
            'summary': clean_text(summary or ''),
            'contents': contents or '',
        })

    print(f'{len(rows)}개 항목 처리 시작')

    out_dir = os.path.join(BASE, CAT_PATH, SUB_DIR)
    os.makedirs(out_dir, exist_ok=True)

    cards = []
    for row in rows:
        num = row['num']
        title = row['subject']
        description = row['summary'] or title
        content_html, images = build_article_blocks(row['contents'], title)
        hero_image = images[0] if images else DEFAULT_IMG

        post_dir = os.path.join(out_dir, str(num))
        os.makedirs(post_dir, exist_ok=True)

        root = '../../../'
        list_root = '../'
        og_url = f'https://journal.rococops.com/{CAT_PATH}/{SUB_DIR}/{num}/'

        page = DETAIL_PAGE.format(
            title=html_escape(title),
            title_short=html_escape(truncate(title, 24)),
            title_json=title.replace('"', '\\"'),
            description=html_escape(description),
            description_json=description.replace('"', '\\"'),
            og_image=hero_image,
            og_url=og_url,
            root=root,
            header=header(root),
            footer=footer(root),
            cat_path=CAT_PATH,
            cat_name=CAT_NAME,
            sub_name=SUB_NAME,
            sub_name_en=SUB_NAME_EN,
            list_root=list_root,
            hero_image=hero_image,
            content=content_html,
            cta_section=CTA_SECTION_HTML.format(cat_name=SUB_NAME),
        )

        with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page)

        cards.append(CARD_HTML.format(
            num=num,
            img=hero_image,
            title=html_escape(truncate(title, 60)),
            desc=html_escape(truncate(description, 70)),
            sub_name=SUB_NAME,
        ))

    # 목록 페이지 생성
    root = '../../'
    list_description = f'{SUB_NAME}({len(rows)}개 케이스) — 로코코성형외과 김상호 원장의 {SUB_NAME} 시술 케이스 모음'
    list_page = LIST_PAGE.format(
        sub_name=SUB_NAME,
        sub_name_en=SUB_NAME_EN,
        description=html_escape(list_description),
        og_image=DEFAULT_IMG,
        og_url=f'https://journal.rococops.com/{CAT_PATH}/{SUB_DIR}/',
        root=root,
        header=header(root),
        footer=footer(root),
        cat_path=CAT_PATH,
        cat_name=CAT_NAME,
        count=len(rows),
        cards='\n'.join(cards),
        cta_section=CTA_SECTION_HTML.format(cat_name=SUB_NAME),
    )

    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(list_page)

    print(f'완료: {len(rows)}개 상세페이지 + 목록페이지 생성 -> {out_dir}')


if __name__ == '__main__':
    main()
