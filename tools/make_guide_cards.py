# 성형 가이드 카드뉴스 이미지 생성 (1080x1080, 사진 없는 글의 본문 이미지·공유 이미지)
#   python tools/make_guide_cards.py <cards.json>
# cards.json: [{"slug": "...", "keyword": "퀵광대", "q": "질문 문장", "points": ["핵심1", "핵심2", "핵심3"]}]
# 결과: images/guide/cards/{slug}.png
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'images', 'guide', 'cards')
FONT_DIR = r'C:\Windows\Fonts'

BG = (17, 17, 17)
GOLD = (184, 149, 106)
WHITE = (255, 255, 255)
SOFT = (215, 215, 215)


def font(names, size):
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise SystemExit('한글 폰트를 찾지 못했습니다')


BOLD = ['NanumSquareEB.ttf', 'NanumSquareB.ttf', 'NanumBarunGothicBold.ttf', 'NanumGothicBold.ttf', 'malgunbd.ttf']
REG = ['NanumSquareR.ttf', 'NanumBarunGothic.ttf', 'NanumGothic.ttf', 'malgun.ttf']


def wrap(draw, text, fnt, width):
    """한글은 어절 단위로, 너무 긴 어절은 글자 단위로 줄바꿈"""
    lines, cur = [], ''
    for word in text.split(' '):
        cand = (cur + ' ' + word).strip()
        if draw.textlength(cand, font=fnt) <= width:
            cur = cand
            continue
        if cur:
            lines.append(cur)
        cur = ''
        for ch in word:
            if draw.textlength(cur + ch, font=fnt) <= width:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
    if cur:
        lines.append(cur)
    return lines


def make(card):
    W = H = 1080
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    x, width = 90, W - 180
    d.text((x, 90), f"ROCOCO 성형 가이드 · {card['keyword']}", font=font(BOLD, 34), fill=GOLD)
    d.rectangle([x, 148, x + 64, 152], fill=GOLD)

    qf = font(BOLD, 62)
    pf = font(REG, 40)
    nf = font(BOLD, 40)
    q_lines = wrap(d, card['q'], qf, width)
    p_lines = [wrap(d, p, pf, width - 60) for p in card['points']]
    # 질문+핵심 묶음을 상단 띠(170)와 하단 서명(H-140) 사이 세로 가운데에 배치
    block = len(q_lines) * 84 + 40 + sum(len(ls) * 58 + 26 for ls in p_lines) - 26
    top, bottom = 190, H - 150
    if block > bottom - top:
        raise SystemExit(f"카드 글이 너무 깁니다: {card['slug']}")
    y = top + (bottom - top - block) // 2

    for line in q_lines:
        d.text((x, y), line, font=qf, fill=WHITE)
        y += 84
    y += 40
    for i, lines in enumerate(p_lines, 1):
        d.text((x, y), str(i), font=nf, fill=GOLD)
        for line in lines:
            d.text((x + 60, y), line, font=pf, fill=SOFT)
            y += 58
        y += 26
    d.text((x, H - 110), '로코코성형외과 김상호 원장', font=font(BOLD, 32), fill=WHITE)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, card['slug'] + '.png')
    img.save(path, optimize=True)
    return os.path.relpath(path, ROOT)


if __name__ == '__main__':
    cards = json.load(open(sys.argv[1], encoding='utf-8'))
    for c in cards:
        print('저장:', make(c))
