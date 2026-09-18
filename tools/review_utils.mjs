// 후기 관련 생성 스크립트(build_reviews.mjs, build_reviews_hub.mjs) 공용 유틸
export const PHOTO_BASE = 'https://rococops.com/files/postscript/attach';

// 익명화: 흔한 한국 성씨로 시작하는 순한글 3자(성+이름2자)만 실명으로 간주, 가운데 글자만 마스킹.
// 나머지(닉네임/영문/숫자/2·4자 등)는 원본 그대로 사용 — 사용자 확인: "흔한 한국성씨 3자일경우만 간주해 가운데글자만 마스킹"
const SURNAMES = new Set(['김','이','박','최','정','강','조','윤','장','임','한','오','서','신','권','황','안','송','전','홍','유','고','문','양','손','배','백','허','남','심','노','하','곽','성','차','주','우','구','나','민','진','지','엄','채','원','천','방','공','현','함','변','염','여','추','도','소','석','선','설','마','길','위','표','명','기','반','왕','금','옥','육','인','맹','제','계','피','연','국','예','경','봉','사','어','두','감','판','단','갈','좌','편','부','간','매','상','시','목','형']);

function isRealName3(name) {
  return /^[가-힣]{3}$/.test(name) && SURNAMES.has(name[0]);
}

export function maskName(name) {
  if (!name) return '고객';
  name = name.trim();
  if (!name) return '고객';
  if (isRealName3(name)) return name[0] + '0' + name[2];
  return name;
}

export function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// 수술후기 열람 게이트 — 회원 로그인(JWT, localStorage)이 없으면 login 페이지로 즉시 리다이렉트.
// <head> 최상단에 넣어서 콘텐츠가 그려지기 전에 판단되도록 함(깜빡임/노출 방지).
// 토큰 서명 검증은 서버(로그인 시점)에서만 하고, 여기서는 존재 여부 + exp(만료)만 클라이언트에서 가볍게 확인.
export const MEMBER_GATE = (root) => `<script>
(function(){
  try {
    var t = localStorage.getItem('rococo_member_token');
    if (t) {
      var payload = JSON.parse(atob(t.split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));
      if (payload.exp && Date.now() < payload.exp * 1000) return;
      localStorage.removeItem('rococo_member_token');
    }
  } catch(e) {}
  location.replace('${root}member/login/?return=' + encodeURIComponent(location.pathname));
})();
</script>`;

// 로그인 상태 표시줄 — 게이트 통과한 회원 페이지 상단에 삽입.
// 동작 스크립트를 main.js가 아니라 여기에 직접 인라인으로 넣음: main.js는 별도 파일이라
// 브라우저/CDN에 이전 버전으로 캐시되면 표시줄만 안 뜨는 문제가 실제로 발생했음.
export const MEMBER_BAR = (root) => `<div class="member-bar" id="memberBar" hidden>
  <span id="memberBarName"></span>
  <a href="${root}member/account/">내 정보</a>
  <button type="button" id="memberLogoutBtn">로그아웃</button>
</div>
<script>
(function(){
  var bar = document.getElementById('memberBar');
  if (!bar) return;
  try {
    var t = localStorage.getItem('rococo_member_token');
    if (t) {
      var raw = atob(t.split('.')[1].replace(/-/g,'+').replace(/_/g,'/'));
      // atob는 바이트 단위라 한글(멀티바이트 UTF-8)이 깨짐 — %XX로 풀어서 다시 디코딩
      var payload = JSON.parse(decodeURIComponent(raw.split('').map(function(c){
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join('')));
      if (payload.exp && Date.now() < payload.exp * 1000) {
        var name = localStorage.getItem('rococo_member_name') || payload.name || '회원';
        document.getElementById('memberBarName').textContent = name + '님';
        bar.hidden = false;
      }
    }
  } catch(e) {}
  var btn = document.getElementById('memberLogoutBtn');
  if (btn) btn.addEventListener('click', function(){
    localStorage.removeItem('rococo_member_token');
    localStorage.removeItem('rococo_member_name');
    location.reload();
  });
})();
</script>`;

export const FOOTER = (root) => `<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-info">
        <p class="footer-logo">ROCOCO <em>Journal</em></p>
        <p>로코코성형외과의원</p>
        <p>서울특별시 강남구 논현로 842 (신사동 599) 압구정빌딩 3층</p>
        <p>대표원장 김상호 · 02-2135-2702</p>
        <p>사업자등록번호 211-09-48591</p>
      </div>
      <div class="footer-hours">
        <p class="footer-title">진료시간</p>
        <p>월·금 — 09:00 ~ 19:00</p>
        <p>화·수·목 — 09:00 ~ 18:00</p>
        <p>토 — 09:00 ~ 13:00</p>
        <p>일·공휴일 휴진</p>
      </div>
      <div class="footer-links">
        <p class="footer-title">바로가기</p>
        <a href="https://rococops.com" target="_blank">기존 홈페이지</a>
        <a href="${root}counsel/">상담·예약</a>
        <a href="${root}cases/">전후사진</a>
        <a href="${root}about/">About 로코코</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 Rococo Plastic Surgery. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="${root}js/main.js"></script>
<a href="https://pf.kakao.com/_xdBpRl" target="_blank" rel="noopener" class="kakao-float">
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="14" cy="13" rx="12" ry="10" fill="#3C1E1E"/>
    <path d="M10.5 10.5c0-1.1.9-2 2-2h3c1.1 0 2 .9 2 2v2a2 2 0 01-2 2h-.8l-1.7 2.2v-2.2h-.5a2 2 0 01-2-2v-2z" fill="#FEE500"/>
  </svg>
  카카오톡 상담 문의
</a>`;
