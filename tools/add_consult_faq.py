import re

CONTENT = {
    'en': {
        'consult': {
            'title': 'Book a Consultation',
            'sub': 'All consultations are conducted by Dr. Kim Sang-ho personally — no coordinators',
            'form_title': 'Online Consultation Form',
            'form_desc': 'Send your questions and photos. We reply by email within 1–2 business days.',
            'form_lang': '✓ English available &nbsp;·&nbsp; Japanese &amp; Chinese (translation-assisted)',
            'kakao_title': 'KakaoTalk',
            'kakao_desc': 'Instant messaging via KakaoTalk. Download the free app to start a chat.',
            'kakao_lang': '✓ Korean preferred &nbsp;·&nbsp; English available',
            'phone_label': 'Phone',
        },
        'faq': {
            'title': 'FAQ for International Patients',
            'sub': 'Common questions from patients traveling from abroad',
            'items': [
                (
                    'Is English consultation available?',
                    'Dr. Kim Sang-ho consults in English directly. Written inquiries in Japanese and Chinese are also accepted — we use translation to ensure clear communication.'
                ),
                (
                    'How do I book a consultation?',
                    'Submit the online consultation form or message us on KakaoTalk. We will confirm your appointment date by email or message, usually within 1–2 business days.'
                ),
                (
                    'Can I come alone without a Korean companion?',
                    'Yes. Dr. Kim handles English consultations directly. Most of our international patients visit independently. Our staff will assist you from the moment you arrive.'
                ),
                (
                    'How long is the recovery period?',
                    'It varies by procedure. As a general guide: cheekbone reduction 2–3 weeks for most swelling to subside, rhinoplasty 2–3 weeks, eye surgery 1–2 weeks. Full results take 3–6 months. We will provide a detailed recovery timeline at your consultation.'
                ),
                (
                    'How much does surgery cost?',
                    'Pricing depends on the specific procedure and your individual case. Please use the consultation form to describe your goals — we will provide a full cost estimate after reviewing your case.'
                ),
            ],
        },
        'maps_label': 'Open in Google Maps →',
        'maps_url': 'https://maps.google.com/maps?q=로코코성형외과+서울+강남구+논현로+842',
    },
    'ja': {
        'consult': {
            'title': 'カウンセリングのご予約',
            'sub': 'すべてのカウンセリングはキム・サンホ院長が直接担当します',
            'form_title': 'オンライン相談フォーム',
            'form_desc': 'ご質問や写真をお送りください。1〜2営業日以内にメールでご返信します。',
            'form_lang': '✓ 日本語対応（翻訳補助）&nbsp;·&nbsp; 英語・中国語も受付可',
            'kakao_title': 'カカオトーク',
            'kakao_desc': 'カカオトークでのリアルタイム相談。アプリをダウンロードしてメッセージをお送りください。',
            'kakao_lang': '✓ 韓国語推奨 &nbsp;·&nbsp; 英語対応可',
            'phone_label': '電話',
        },
        'faq': {
            'title': '海外からいらっしゃる患者様へ よくある質問',
            'sub': '韓国での美容整形を検討されている方へ',
            'items': [
                (
                    '日本語でのカウンセリングはできますか？',
                    '日本語での直接会話は難しいですが、オンライン相談フォームから日本語でお問い合わせいただければ、翻訳を通じて丁寧にご対応いたします。英語でのカウンセリングはキム院長が直接対応します。'
                ),
                (
                    '予約はどのようにするのですか？',
                    'オンライン相談フォームからご希望の日程をお送りいただくか、カカオトークでご連絡ください。通常1〜2営業日以内にご確認のご連絡を差し上げます。'
                ),
                (
                    '一人で来院しても大丈夫ですか？',
                    'はい、大丈夫です。英語でのコミュニケーションが可能ですので、韓国語ができなくても安心してご来院いただけます。多くの海外の患者様が一人で来院されています。'
                ),
                (
                    'ダウンタイム（回復期間）はどのくらいですか？',
                    '術式によって異なります。目安として：頬骨縮小術 2〜3週間、鼻整形 2〜3週間、目の整形 1〜2週間で大きな腫れが引きます。最終的な仕上がりは3〜6ヶ月後です。カウンセリング時に詳しくご説明します。'
                ),
                (
                    '手術費用はどのくらいですか？',
                    '術式や個々の状態によって異なるため、一概にはお伝えできません。オンライン相談フォームにてご希望やお悩みをお送りいただければ、詳細なお見積りをお出しいたします。'
                ),
            ],
        },
        'maps_label': 'Google マップで開く →',
        'maps_url': 'https://maps.google.com/maps?q=로코코성형외과+서울+강남구+논현로+842',
    },
    'zh': {
        'consult': {
            'title': '预约咨询',
            'sub': '所有咨询均由金相镐院长亲自主持，不设中间人',
            'form_title': '在线咨询表格',
            'form_desc': '请发送您的问题和照片，我们将在1-2个工作日内通过邮件回复。',
            'form_lang': '✓ 支持中文（翻译辅助）&nbsp;·&nbsp; 英语·日语均可',
            'kakao_title': 'KakaoTalk',
            'kakao_desc': '通过KakaoTalk即时咨询。请下载应用程序后发送消息。',
            'kakao_lang': '✓ 韩语优先 &nbsp;·&nbsp; 支持英语',
            'phone_label': '电话',
        },
        'faq': {
            'title': '海外患者常见问题',
            'sub': '专为考虑赴韩整形的国际患者整理',
            'items': [
                (
                    '可以用中文咨询吗？',
                    '目前不提供直接的中文对话服务，但可通过在线咨询表格以中文提问，我们会借助翻译为您详细解答。金院长可以用英语直接沟通。'
                ),
                (
                    '如何预约？',
                    '请通过在线咨询表格告知希望预约的日期，或通过KakaoTalk联系我们。通常在1-2个工作日内确认预约。'
                ),
                (
                    '一个人来也可以吗？',
                    '完全可以。金院长可以用英语沟通，许多海外患者都是独自前来。到院后工作人员会全程协助您。'
                ),
                (
                    '恢复期大概需要多长时间？',
                    '因手术项目而异。一般参考：颧骨缩小2-3周主要肿胀消退，鼻整形2-3周，眼部整形1-2周。最终效果需3-6个月后完全显现。咨询时会提供详细的恢复时间表。'
                ),
                (
                    '手术费用大概是多少？',
                    '费用因手术项目和个人情况而有所不同。请通过在线咨询表格告知您的需求，我们将在了解您的情况后提供详细报价。'
                ),
            ],
        },
        'maps_label': '在 Google 地图中打开 →',
        'maps_url': 'https://maps.google.com/maps?q=로코코성형외과+서울+강남구+논현로+842',
    },
}

CONSULT_CSS = """
.consult-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
@media(max-width:640px){ .consult-grid { grid-template-columns: 1fr; } }
.consult-card { display: flex; flex-direction: column; gap: 0.75rem; background: #fafafa; border: 1px solid #e8e8e8; border-radius: 10px; padding: 1.5rem 1.75rem; text-decoration: none; transition: box-shadow 0.15s; }
.consult-card:hover { box-shadow: 0 4px 18px rgba(0,0,0,0.09); }
.consult-icon { font-size: 2rem; line-height: 1; }
.consult-card h3 { font-size: 1.05rem; font-weight: 700; color: #111; margin: 0; }
.consult-card p { font-size: 0.88rem; color: #555; line-height: 1.7; margin: 0; }
.consult-card .lang-note { font-size: 12px; color: #b8956a; font-weight: 600; border-top: 1px solid #eee; padding-top: 0.65rem; margin-top: auto; }
.consult-phone { font-size: 0.9rem; color: #555; text-align: center; margin-top: 0.5rem; }
.consult-phone a { color: #111; font-weight: 700; }
.faq-list { display: flex; flex-direction: column; gap: 0.75rem; }
.faq-item { border: 1px solid #ebebeb; border-radius: 8px; overflow: hidden; }
.faq-item summary { cursor: pointer; padding: 1rem 1.25rem; font-size: 0.95rem; font-weight: 600; color: #111; list-style: none; display: flex; justify-content: space-between; align-items: center; user-select: none; }
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after { content: '+'; font-size: 1.2rem; color: #b8956a; font-weight: 400; transition: transform 0.2s; flex-shrink: 0; margin-left: 1rem; }
.faq-item[open] summary::after { content: '−'; }
.faq-item p { padding: 0 1.25rem 1rem; font-size: 0.88rem; color: #555; line-height: 1.8; margin: 0; }
"""

def make_consult_section(lang):
    c = CONTENT[lang]['consult']
    return f"""<section class="section" id="consult">
  <p class="section-title">{c['title']}</p>
  <p class="section-sub">{c['sub']}</p>
  <div class="consult-grid">
    <a href="https://journal.rococops.com/counsel/" class="consult-card">
      <div class="consult-icon">✉️</div>
      <h3>{c['form_title']}</h3>
      <p>{c['form_desc']}</p>
      <span class="lang-note">{c['form_lang']}</span>
    </a>
    <a href="https://pf.kakao.com/_xdBpRl" class="consult-card" target="_blank" rel="noopener">
      <div class="consult-icon">💬</div>
      <h3>{c['kakao_title']}</h3>
      <p>{c['kakao_desc']}</p>
      <span class="lang-note">{c['kakao_lang']}</span>
    </a>
  </div>
  <p class="consult-phone">{c['phone_label']}: <a href="tel:+82221352702">+82-2-2135-2702</a></p>
</section>

<hr class="divider">"""

def make_faq_section(lang):
    f = CONTENT[lang]['faq']
    items_html = '\n    '.join(
        f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in f['items']
    )
    return f"""<section class="section" id="faq">
  <p class="section-title">{f['title']}</p>
  <p class="section-sub">{f['sub']}</p>
  <div class="faq-list">
    {items_html}
  </div>
</section>

<hr class="divider">"""

def add_maps_link(html, lang):
    maps_label = CONTENT[lang]['maps_label']
    maps_url = CONTENT[lang]['maps_url']
    maps_link = f'\n      <p style="margin-top:1.2rem;"><a href="{maps_url}" target="_blank" rel="noopener" style="color:#b8956a;font-weight:700;font-size:0.9rem;">{maps_label}</a></p>'
    # 위치 섹션 내 tel 링크 다음에 추가
    pattern = r'(<p[^>]*><strong>Tel:<\/strong>.*?<\/p>)'
    if re.search(pattern, html):
        html = re.sub(pattern, r'\1' + maps_link, html, count=1)
    return html

for lang in ['en', 'ja', 'zh']:
    fpath = f'{lang}/index.html'
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    # CSS 추가
    if '.consult-grid' not in html:
        html = html.replace('</style>', CONSULT_CSS + '\n</style>', 1)
        print(f'{lang}: CSS 추가')

    # 상담 섹션: doctor 섹션 뒤 divider 다음에 삽입
    consult_block = make_consult_section(lang)
    faq_block = make_faq_section(lang)

    # cases-banner 앞에 상담 섹션 삽입 (없으면 location 앞)
    if '<!-- 케이스 리뷰 배너 -->' in html and 'id="consult"' not in html:
        html = html.replace('<!-- 케이스 리뷰 배너 -->', consult_block + '\n\n<!-- 케이스 리뷰 배너 -->')
        print(f'{lang}: 상담 섹션 삽입')
    elif 'id="consult"' in html:
        print(f'{lang}: 상담 섹션 이미 있음')
    else:
        print(f'{lang}: WARNING - 상담 섹션 삽입 위치 못 찾음')

    # FAQ: location 섹션 앞에 삽입
    if 'id="location"' in html and 'id="faq"' not in html:
        html = html.replace('<!-- 위치 & 시간 -->', faq_block + '\n\n<!-- 위치 & 시간 -->')
        if 'id="faq"' not in html:
            # 주석 없는 경우
            loc_pattern = r'(<section class="section" id="location">)'
            html = re.sub(loc_pattern, faq_block + '\n\n' + r'\1', html, count=1)
        print(f'{lang}: FAQ 섹션 삽입')
    elif 'id="faq"' in html:
        print(f'{lang}: FAQ 이미 있음')

    # 구글맵 링크
    html = add_maps_link(html, lang)
    print(f'{lang}: 구글맵 링크 처리')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

print('\n완료')
