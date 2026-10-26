// 가이드 키워드 → 대표페이지 연결표를 JSON으로 내보냄 (파이썬 빌드 스크립트가 읽음)
//   node tools/guide_landing_map.mjs
import { LANDING_RULES } from './guide.mjs';
console.log(JSON.stringify(LANDING_RULES.map(([re, path, label]) => ({ pattern: re.source, path, label }))));
