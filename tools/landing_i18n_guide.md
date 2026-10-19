# 외국어 대표페이지 번역 원칙 (영어·일본어·중국어)

한국어 대표페이지(`data/landing/{cat}-{sub}.json`)를 번역해 `/{lang}/{cat}/{sub}/` 페이지를 만든다.
번역가는 Claude 한 명(사용자 결정, 2026-10-20). 원어민 검수 없이 올라가므로 **정확성이 최우선**이다.
완성 예시: `data/landing/i18n/en/nose-hump.json` → `/en/nose/hump/`

## 구조
- 번역 파일: `data/landing/i18n/{lang}/{cat}-{sub}.json` — **문장만** 넣는다. 숫자·사진·출처 링크·아이콘은 한국어 데이터에서 자동으로 가져온다.
- 생성: `python tools/build_landing_i18n.py {lang} {cat}-{sub}` → `{lang}/{cat}/{sub}/index.html`
  - 번역 파일의 항목 개수가 한국어 데이터와 다르면 생성기가 멈춘다(구조 대조). 개수를 맞춰라.
- 원장 이야기(story) 인용은 번역문 아래에 한국어 원문이 접힌 채로 함께 나온다.
- 케이스 글·사진 카드는 한국어 페이지로 연결된다(번역하지 않음). 한국어 칼럼 제목은 번역 파일에 넣지 않는다.

## 번역 파일 항목 (예시 파일과 같은 키)
`seo{title, description, h1}`, `hero{eyebrow, question, summary, stats[라벨], units[단위], case_caption, case_alt}`,
`features{type, toc, title, items[], note}`, `story{title, blocks[{heading, paras[]}]}`,
`method{title, steps[], note, pros_cons[]}`, `recovery{title, items[{label, lines[]}], note}`,
`before_after{title, alt, labels[]}`, `logs{title, tags[]}`, `faq[{q, a}]`, `related[이름]`,
그리고 한국어 데이터에 `companions`가 있으면 `companions[{name, lead}]`.
`hero.units`는 숫자 뒤 단위(예: en `hour`/`weeks`, ja `時間`/`週間`, zh `小时`/`周`). `hero.case_caption`은 한국어 히어로 사례 칼럼 제목을 그 언어로 옮긴 짧은 설명.

## 반드시 지킬 것
1. **원장님 문장은 충실하게 번역한다.** 요약·생략·과장·보탬 금지. "대부분", "드물게", "개인적으로는", "(?)" 같은 단서와 1인칭 말투를 그대로 살린다. 숫자·기간·비율은 한국어와 같아야 한다.
2. **의학적 의미가 바뀌지 않게.** 모르는 용어는 추측으로 의역하지 말고, 아래 용어집과 일반적인 의학 용어를 쓴다. 정말 애매하면 보고서에 적는다.
3. **제작 문구**(소제목·질문형 부제·라벨·태그·FAQ 질문)는 자연스럽고 짧게. 의학적 주장을 새로 만들지 않는다.
4. **SEO**: title은 `{시술명} in Seoul | {핵심 2~3개} | Dr. Kim Sang-ho, Rococo Plastic Surgery` 형태(ja/zh는 그 언어 관례대로). 그 나라 사람이 실제로 검색하는 일반 용어를 쓰고, 필요하면 다른 표기를 괄호로. description은 en 160자, ja 120자, zh 80자 안팎.
5. 중국어는 **간체(zh-CN)**. 일본어는 です・ます체. 영어는 미국식 철자.
6. 이름: 김상호 원장 = Dr. Kim Sang-ho / キム・サンホ院長 / 金相浩院长. 로코코성형외과 = Rococo Plastic Surgery / ロココ整形外科 / 洛可可整形外科.

## 용어집 (기본값 — 문맥에 맞으면 그대로, 아니면 더 일반적인 용어로)
| 한국어 | English | 日本語 | 中文 |
|---|---|---|---|
| 매부리코 | hump nose (dorsal hump) | 鷲鼻 | 驼峰鼻 |
| 비공내리기 | alar rim lowering (hiding nostril show) | 鼻孔縁下降術（小鼻下げ） | 鼻翼缘下移（遮挡鼻孔） |
| 콧날개올리기 | alar rim lifting | 小鼻挙上術 | 鼻翼上提 |
| 콧볼축소술 | alar base reduction | 小鼻縮小術 | 鼻翼缩小术 |
| 복코 | bulbous nose (bulbous tip) | 団子鼻 | 蒜头鼻 |
| 코재수술 | revision rhinoplasty | 鼻の再手術 | 鼻修复手术 |
| 자가늑연골 | autologous rib cartilage | 自家肋軟骨 | 自体肋软骨 |
| 비중격연골 | septal cartilage | 鼻中隔軟骨 | 鼻中隔软骨 |
| 귀연골 | ear (conchal) cartilage | 耳介軟骨 | 耳软骨 |
| 절골술 | osteotomy | 骨切り術 | 截骨术 |
| 비개방(흉터없는) 코성형 | closed rhinoplasty | クローズ法鼻整形 | 闭合式隆鼻 |
| 휜코 | crooked (deviated) nose | 斜鼻（曲がった鼻） | 歪鼻 |
| 들창코 | upturned nose | 豚鼻（上向きの鼻） | 朝天鼻 |
| 구축코 | contracted nose | 拘縮鼻 | 挛缩鼻 |
| 비주 | columella | 鼻柱 | 鼻小柱 |
| 퀵광대(15분 광대축소술) | quick cheekbone reduction (15-minute) | 頬骨縮小術（15分） | 颧骨缩小术（15分钟） |
| 뒷광대 | rear zygomatic arch | 頬骨弓（後方） | 颧弓后部 |
| 눈매교정 | ptosis correction | 眼瞼下垂矯正 | 上睑下垂矫正 |
| 앞트임/뒤트임/밑트임 | epicanthoplasty / lateral canthoplasty / lower eyelid lowering | 目頭切開 / 目尻切開 / たれ目形成 | 开内眼角 / 开外眼角 / 下眼睑下至 |
| 쌍커풀 자연유착법(매몰법) | non-incisional double eyelid (natural adhesion, buried suture) | 埋没法二重 | 埋线双眼皮 |
| 내시경 이마거상술 | endoscopic forehead (brow) lift | 内視鏡下額リフト | 内窥镜额部提升 |
| 무턱 | retruded (weak) chin | 小さい顎（下顎後退） | 下巴后缩 |
| 수면마취 | sedation (IV sedation) | 静脈麻酔（睡眠麻酔） | 静脉麻醉（睡眠麻醉） |
| 붓기 / 멍 | swelling / bruising | 腫れ / 内出血 | 肿胀 / 淤青 |

## 순서
1. `data/landing/{cat}-{sub}.json`을 읽고, 필요하면 원문 칼럼(`/카테고리/하위메뉴/번호/`)을 열어 문맥을 확인한다.
2. 번역 파일 작성 → `python tools/build_landing_i18n.py {lang} {key}` → 미리보기(PC·모바일 375px)로 확인.
3. 이 브랜치에 **번역 파일과 생성된 `{lang}/{cat}/{sub}/index.html`만** 커밋.

## 건드리면 안 되는 것
한국어 페이지·데이터, `css/style.css`, `tools/*.py`, `sitemap.xml`, 다른 언어 폴더. push 금지. (hreflang·사이트맵·한국어 페이지 연결은 메인 세션이 합칠 때 한꺼번에 처리)
