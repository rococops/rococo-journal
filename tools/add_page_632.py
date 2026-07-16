# nostril/alar-raising/632/index.html 생성 스크립트
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from templates import (DETAIL_PAGE, NAV_HTML, HEADER_HTML, FOOTER_HTML,
                       CTA_SECTION_HTML, ORIGIN_LINK_CARD)

ROOT       = '../../../'
CAT_PATH   = 'nostril'
CAT_NAME   = '콧구멍성형'
SUB_DIR    = 'alar-raising'
SUB_NAME   = '콧날개올리기'
SUB_NAME_EN= 'Alar Raising'
NUM        = '632'
DATE       = '2025-08-01'

TITLE = '콧구멍이 큰 용코에서 콧구멍·콧볼축소술 + 콧날개올리기'
DESCRIPTION = ('복코 자체 교정에는 한계가 있지만, 콧구멍이 지나치게 넓은 경우 '
               '콧볼축소술(30분)과 콧날개올리기를 동시에 진행해 정면·측면 균형을 개선할 수 있습니다. '
               '로코코성형외과 김상호 원장의 실제 케이스 전후 비교입니다.')

BASE = 'https://rococops.com'
IMGS = [
    '/files/editor/202607131645191844490817.jpg',
    '/files/editor/20260713164622208310113.jpg',
    '/files/editor/202607131646422104808459.jpg',
    '/files/editor/20260713164642164625279.jpg',
    '/files/editor/202607131646421377833096.jpg',
    '/files/editor/202607131647141949951450.jpg',
    '/files/editor/20260713164714514336753.jpg',
    '/files/editor/20260713164731103649462.jpg',
    '/files/editor/202607131647421476154293.jpg',
    '/files/editor/202607131647481199700795.jpg',
    '/files/editor/20260713164806244944137.jpg',
    '/files/editor/202607131648061650339854.jpg',
    '/files/editor/2026071316480626800305.jpg',
    '/files/editor/20260713164830186546214.jpg',
    '/files/editor/202607131648301536190966.jpg',
    '/files/editor/202607131648391592603676.jpg',
]

def img_tag(src, alt=''):
    return f'<img src="{BASE}{src}" alt="{alt}" loading="lazy" style="max-width:100%;height:auto;display:block;margin:1rem 0;border-radius:8px;">'

content_blocks = [
    '<p>복코(용코)는 코끝 연골의 형태가 원인이기 때문에 단순 피부 절제나 작은 시술로는 교정에 한계가 있습니다. 그러나 콧구멍 바닥이 아래쪽으로 \'V\'자 모양으로 뾰족하게 노출되고 콧볼이 넓게 퍼져 있는 경우에는, 다음 두 가지 수술을 병행해 정면과 측면 균형을 크게 개선할 수 있습니다.</p>',
    '<h2>수술 구성</h2>',
    '<p><strong>① 콧구멍·콧볼축소술</strong> — 약 20분 소요. 콧볼이 지나치게 넓은 경우 콧볼 바깥쪽에서 타원형으로 피부를 제거하여 콧볼 폭을 줄이는 수술입니다. 실밥 제거는 수술 후 5~7일.</p>',
    '<p><strong>② 콧날개올리기(알라 레이징)</strong> — 약 20분 소요. 콧날개가 처지거나 콧구멍이 지나치게 많이 보이는 경우 콧날개를 위로 올려줍니다. 실밥 제거는 수술 후 10~14일.</p>',
    '<p>두 수술을 수면마취 하에 동시 진행하므로 총 수술 시간은 약 30~40분입니다.</p>',
    img_tag(IMGS[0], '수술 전 정면 사진'),
    img_tag(IMGS[1], '수술 전 콧구멍 확대'),
    '<h2>수술 전후 비교</h2>',
    '<p>아래 사진들은 실제 시술 전후를 정면·측면·올려본 각도에서 촬영한 결과입니다.</p>',
    img_tag(IMGS[2], '수술 전후 비교 1'),
    img_tag(IMGS[3], '수술 전후 비교 2'),
    img_tag(IMGS[4], '수술 전후 비교 3'),
    img_tag(IMGS[5], '수술 전후 비교 4'),
    img_tag(IMGS[6], '수술 전후 비교 5'),
    img_tag(IMGS[7], '수술 전후 비교 6'),
    img_tag(IMGS[8], '수술 전후 비교 7'),
    img_tag(IMGS[9], '수술 전후 비교 8'),
    img_tag(IMGS[10], '수술 전후 비교 9'),
    img_tag(IMGS[11], '수술 전후 비교 10'),
    img_tag(IMGS[12], '수술 전후 비교 11'),
    img_tag(IMGS[13], '수술 전후 비교 12'),
    img_tag(IMGS[14], '수술 전후 비교 13'),
    img_tag(IMGS[15], '수술 전후 비교 14'),
    '<h2>주의사항</h2>',
    '<p>수술 후 붓기는 1~2주 내 많이 가라앉으며, 최종 결과는 3개월 이후 확인할 수 있습니다. 흉터는 코 주름선을 따라 절개하므로 시간이 지나면 거의 보이지 않습니다.</p>',
]

content_html = '\n'.join(content_blocks)

HERO_IMAGE = f'{BASE}{IMGS[0]}'
OG_URL = f'https://journal.rococops.com/{CAT_PATH}/{SUB_DIR}/{NUM}/'

def json_esc(s):
    return s.replace('"', '\\"')

nav = NAV_HTML.format(
    root=ROOT,
    active_cheekbone='', active_nose='',
    active_nostril='active', active_forehead='',
    active_eye='', active_anti_aging='',
)
header = HEADER_HTML.format(root=ROOT, nav=nav)
footer = FOOTER_HTML.format(root=ROOT)
cta = CTA_SECTION_HTML.format(root=ROOT, cat_name=CAT_NAME)
origin = ORIGIN_LINK_CARD.format(
    origin_url=f'https://rococops.com/htm/sitecontents_read.php?id={NUM}&sitecode=0303'
)

html = DETAIL_PAGE.format(
    root=ROOT,
    meta_title=f'{TITLE} | 로코코 저널',
    description=DESCRIPTION,
    og_image=HERO_IMAGE,
    og_url=OG_URL,
    canonical_url=OG_URL,
    title_json=json_esc(TITLE),
    description_json=json_esc(DESCRIPTION),
    sub_name_json=json_esc(SUB_NAME),
    cat_name_json=json_esc(CAT_NAME),
    cat_path=CAT_PATH,
    sub_dir=SUB_DIR,
    date=DATE,
    cat_name=CAT_NAME,
    sub_name=SUB_NAME,
    sub_name_en=SUB_NAME_EN,
    title=TITLE,
    title_short=TITLE[:20] + '…',
    hero_image=HERO_IMAGE,
    img_alt=TITLE,
    list_root=f'{ROOT}{CAT_PATH}/{SUB_DIR}/',
    content=content_html,
    origin_link_card=origin,
    cta_section=cta,
    header=header,
    footer=footer,
)

out_dir = os.path.join(os.path.dirname(__file__), '..', CAT_PATH, SUB_DIR, NUM)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'생성 완료: {out_path}')
