"""sitecontents.contents (HTML) -> 정제된 article-content HTML 블록 생성."""
import re
from bs4 import BeautifulSoup, NavigableString, Tag

ZERO_WIDTH = re.compile(r'[​‌‍﻿]')
URL_RE = re.compile(r'(https?://\S+|www\.\S+)', re.IGNORECASE)
EMOTICON_RE = re.compile(r'\^[\^_\-]*\^[;*]?')
ORIGIN_LINK_RE = re.compile(r'원문\s*(?:링크|보기)\s*:?')
WS_RE = re.compile(r'\s+')


def clean_text(text):
    text = ZERO_WIDTH.sub('', text)
    text = text.replace('\xa0', ' ')
    text = URL_RE.sub('', text)
    text = EMOTICON_RE.sub('', text)
    text = ORIGIN_LINK_RE.sub('', text)
    text = WS_RE.sub(' ', text).strip()
    # 글자만 남거나 의미없는 구두점만 남은 경우 제거
    if not text or re.fullmatch(r'[\s\.\-_·:;,]*', text):
        return ''
    return text


def html_escape(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def fix_img_src(src):
    if not src:
        return None
    src = src.strip()
    if src.startswith('//'):
        return 'https:' + src
    if src.startswith('http://') or src.startswith('https://'):
        return src
    if src.startswith('/'):
        return 'https://rococops.com' + src
    return 'https://rococops.com/' + src


ORIGIN_HOST_RE = re.compile(r'(blog\.naver\.com|blog\.me|rococops\.com)', re.IGNORECASE)
ZW_SUFFIX_RE = re.compile(r'(?:%E2%80%8B|[​‌‍﻿])+$', re.IGNORECASE)


def extract_origin_url(contents_html):
    """본문에서 '원문 링크/보기' 라벨 바로 다음에 나오는 원본 블로그(naver/rococops) 글 링크를 찾아서 반환.
    원문 라벨 뒤에 실제 링크가 아닌 다른 <a>가 오는 경우(이후 본문에서 다른 글로 잘못 연결되는 것)는 None 처리."""
    soup = BeautifulSoup(contents_html or '', 'html.parser')
    nodes = list(soup.descendants)
    for i, node in enumerate(nodes):
        if isinstance(node, NavigableString) and '원문' in str(node):
            for nxt in nodes[i + 1:]:
                if isinstance(nxt, Tag) and nxt.name == 'a':
                    href = ZW_SUFFIX_RE.sub('', (nxt.get('href') or '').strip())
                    if href and ORIGIN_HOST_RE.search(href):
                        return href
                    return None
            return None
    return None


def first_paragraph_text(contents_html):
    """본문 HTML에서 첫 번째 텍스트 블록(설명용)을 추출."""
    soup = BeautifulSoup(contents_html or '', 'html.parser')

    def walk(node):
        if isinstance(node, NavigableString):
            t = clean_text(str(node))
            return t or None
        if not isinstance(node, Tag):
            return None
        if node.name in ('script', 'style', 'img'):
            return None
        if node.name in ('p', 'div', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'blockquote'):
            t = clean_text(node.get_text())
            return t or None
        for child in node.children:
            r = walk(child)
            if r:
                return r
        return None

    for top in soup.contents:
        r = walk(top)
        if r:
            return r
    return ''


def build_article_blocks(contents_html, alt_text):
    """returns (html_string, list_of_image_urls)"""
    soup = BeautifulSoup(contents_html or '', 'html.parser')
    blocks = []
    images = []
    alt = html_escape(alt_text)

    def walk(node):
        if isinstance(node, NavigableString):
            t = clean_text(str(node))
            if t:
                blocks.append(('text', t))
            return
        if not isinstance(node, Tag):
            return
        if node.name == 'img':
            src = fix_img_src(node.get('src'))
            if src:
                blocks.append(('img', src))
                images.append(src)
            return
        if node.name in ('script', 'style'):
            return
        if node.name in ('p', 'div', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'blockquote'):
            # 블록 내부에 이미지가 있으면 텍스트와 분리해서 순서대로 처리
            text_parts = []
            for child in node.children:
                if isinstance(child, Tag) and (child.name == 'img' or child.find('img')):
                    if text_parts:
                        t = clean_text(' '.join(text_parts))
                        if t:
                            blocks.append(('text', t))
                        text_parts = []
                    walk(child)
                else:
                    text_parts.append(child.get_text() if isinstance(child, Tag) else str(child))
            if text_parts:
                t = clean_text(' '.join(text_parts))
                if t:
                    blocks.append(('text', t))
            return
        # 인라인/기타 요소: 자식 순회
        for child in node.children:
            walk(child)

    for top in soup.contents:
        walk(top)

    # 연속된 동일 이미지 중복 제거
    out = []
    seen_consecutive_img = None
    for kind, val in blocks:
        if kind == 'img' and val == seen_consecutive_img:
            continue
        out.append((kind, val))
        seen_consecutive_img = val if kind == 'img' else None

    html_parts = []
    for kind, val in out:
        if kind == 'text':
            html_parts.append(f'<p>{html_escape(val)}</p>')
        else:
            html_parts.append(f'<img src="{val}" alt="{alt}" loading="lazy">')

    return '\n        '.join(html_parts), images
