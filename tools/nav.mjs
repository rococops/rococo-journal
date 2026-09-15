// 사이트 공통 GNB — 모든 페이지 생성 스크립트가 여기서 가져다 씀 (api/publish.js, tools/build_reviews.mjs, tools/update_gnb.mjs)
export const CAT_NAMES = { cheekbone: '광대성형', nose: '코성형', nostril: '콧구멍성형', forehead: '이마성형', eye: '눈성형', 'anti-aging': '동안성형', etc: '기타' };

export function navHtml(root, activeCat) {
  const a = (cat) => cat === activeCat ? 'active' : '';
  return `<nav class="gnb" id="gnb">
      <div class="gnb-header">
        <span class="gnb-title">Menu</span>
        <button class="gnb-close" id="gnbClose" aria-label="메뉴 닫기">&#x2715;</button>
      </div>
      <ul>
        <li class="has-sub ${a('cheekbone')}"><a href="${root}cheekbone/">광대성형</a>
          <ul class="sub-menu">
            <li><a href="${root}cheekbone/quick/">15분 광대축소술</a></li>
            <li><a href="${root}cheekbone/fat-graft/">심부볼·관자 지방이식</a></li>
            <li><a href="${root}cheekbone/liposuction/">광대라인 지방흡입</a></li>
            <li><a href="${root}cheekbone/rear/">뒷광대축소술</a></li>
            <li><a href="${root}cheekbone/revision/">광대 재수술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('nose')}"><a href="${root}nose/">코성형</a>
          <ul class="sub-menu">
            <li><a href="${root}nose/column/">진료단상</a></li>
            <li><a href="${root}nose/revision/">코재수술</a></li>
            <li><a href="${root}nose/rib-cartilage/">늑연골 명품코성형</a></li>
            <li><a href="${root}nose/septal/">비중격연골 코성형</a></li>
            <li><a href="${root}nose/scarless/">흉터없는 코성형</a></li>
            <li><a href="${root}nose/hump/">매부리코</a></li>
            <li><a href="${root}nose/bulbous/">복코</a></li>
            <li><a href="${root}nose/osteotomy/">절골술</a></li>
            <li><a href="${root}nose/long/">긴코</a></li>
            <li><a href="${root}nose/columella/">비주성형</a></li>
            <li><a href="${root}nose/cat/">비순각 고양이 입매교정</a></li>
            <li><a href="${root}nose/male/">남자의 코성형</a></li>
            <li><a href="${root}nose/rhinitis/">비염수술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('nostril')}"><a href="${root}nostril/">콧구멍성형</a>
          <ul class="sub-menu">
            <li><a href="${root}nostril/alar-lowering/">비공내리기</a></li>
            <li><a href="${root}nostril/alar-raising/">콧날개올리기</a></li>
            <li><a href="${root}nostril/v-shape/">V형 콧구멍교정</a></li>
            <li><a href="${root}nostril/reduction/">콧구멍축소술</a></li>
            <li><a href="${root}nostril/alar-base/">콧볼축소술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('forehead')}"><a href="${root}forehead/">이마성형</a>
          <ul class="sub-menu">
            <li><a href="${root}forehead/endoscopic/">내시경 이마거상술</a></li>
            <li><a href="${root}forehead/reduction/">이마축소술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('eye')}"><a href="${root}eye/">눈성형</a>
          <ul class="sub-menu">
            <li><a href="${root}eye/correction/">눈매교정술</a></li>
            <li><a href="${root}eye/incision/">트임성형</a></li>
            <li><a href="${root}eye/double/">쌍커풀 자연유착법</a></li>
            <li><a href="${root}eye/lower-fat/">눈밑지방 재배치</a></li>
            <li><a href="${root}eye/fat-graft/">꺼진눈 지방이식</a></li>
            <li><a href="${root}eye/brow-lift/">눈썹하거상술</a></li>
          </ul>
        </li>
        <li class="has-sub ${a('anti-aging')}"><a href="${root}anti-aging/">동안성형</a>
          <ul class="sub-menu">
            <li><a href="${root}anti-aging/chin/">무턱성형</a></li>
            <li><a href="${root}anti-aging/fat-graft/">미세지방이식</a></li>
            <li><a href="${root}anti-aging/blepharoplasty/">상·하안검성형</a></li>
            <li><a href="${root}anti-aging/lifting/">엘라스티꿈 실리프팅</a></li>
            <li><a href="${root}anti-aging/filler-botox/">필러·보톡스</a></li>
          </ul>
        </li>
        <li class="has-sub"><a href="${root}about/">About</a>
          <ul class="sub-menu">
            <li><a href="${root}about/">로코코 소개</a></li>
            <li><a href="${root}about/philosophy/">철학과 강점</a></li>
            <li><a href="${root}about/location/">오시는 길·진료시간</a></li>
            <li><a href="${root}about/faq/">자주 묻는 질문</a></li>
          </ul>
        </li>
        <li><a href="${root}counsel/" class="btn-consult">상담·예약</a></li>
        <li><a href="${root}reviews/" class="btn-gold-outline">수술후기</a></li>
        <li><a href="${root}cases/" class="btn-gold">전후사진</a></li>
      </ul>
    </nav>`;
}
