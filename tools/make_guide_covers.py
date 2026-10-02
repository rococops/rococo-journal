# 성형 가이드 "사진 없는 글"용 키워드별 표지 이미지 생성 (1200x630, 목록 썸네일·카톡/SNS 공유 이미지 겸용)
#   python tools/make_guide_covers.py
# 결과: images/guide/covers/{name}.png
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'images', 'guide', 'covers')
FONT_DIR = r'C:\Windows\Fonts'

COVERS = [
    ('quick-cheekbone', '퀵광대', '옆광대 · 45도 광대 · 회복'),
    ('cheekbone', '광대축소술', '광대 유형 · 지방이식 · 재수술'),
    ('revision', '코재수술', '시기 · 보형물 제거 · 구축코'),
    ('alar', '비공내리기', '콧구멍 노출 · 짝짝이 · 흉터'),
    ('rib-cartilage', '늑연골 코성형', '자가늑연골 · 채취 · 코끝'),
    ('nose', '코성형', '재료 · 코끝 · 콧대'),
]

BG = (17, 17, 17)        # 사이트 헤더와 같은 검정
GOLD = (184, 149, 106)   # 사이트 강조색
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)


def font(names, size):
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise SystemExit('한글 폰트를 찾지 못했습니다: ' + ', '.join(names))


BOLD = ['NanumSquareEB.ttf', 'NanumSquareB.ttf', 'NanumBarunGothicBold.ttf', 'NanumGothicBold.ttf', 'malgunbd.ttf']
REG = ['NanumSquareR.ttf', 'NanumBarunGothic.ttf', 'NanumGothic.ttf', 'malgun.ttf']

os.makedirs(OUT, exist_ok=True)
for name, title, sub in COVERS:
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    x = 96
    d.text((x, 150), 'ROCOCO 성형 가이드', font=font(BOLD, 30), fill=GOLD)
    d.rectangle([x, 205, x + 64, 209], fill=GOLD)
    d.text((x, 250), title, font=font(BOLD, 108), fill=WHITE)
    d.text((x, 400), sub, font=font(REG, 36), fill=GRAY)
    d.text((x, 520), '로코코성형외과 김상호 원장', font=font(BOLD, 28), fill=WHITE)
    path = os.path.join(OUT, name + '.png')
    img.save(path, optimize=True)
    print('저장:', os.path.relpath(path, ROOT))
