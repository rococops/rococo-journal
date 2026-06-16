const GITHUB_REPO = 'rococops/rococo-journal';
const GITHUB_API  = 'https://api.github.com';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://journal.rococops.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { password, catPath, subDir } = req.body || {};
  if (password !== process.env.ADMIN_PASSWORD)
    return res.status(401).json({ error: `인증 실패 (받은값: ${password ? password.slice(0,2)+'***' : 'undefined'}, 환경변수: ${process.env.ADMIN_PASSWORD ? '설정됨' : '미설정'})` });

  const token = process.env.GITHUB_TOKEN;
  try {
    const r = await fetch(`${GITHUB_API}/repos/${GITHUB_REPO}/contents/${catPath}/${subDir}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
      },
    });
    if (!r.ok) return res.status(404).json({ error: '카테고리를 찾을 수 없습니다.' });
    const items = await r.json();
    const slugs = items
      .filter(i => i.type === 'dir')
      .map(i => i.name)
      .sort((a, b) => {
        // 숫자면 숫자 정렬, 아니면 문자 정렬
        const na = parseInt(a), nb = parseInt(b);
        if (!isNaN(na) && !isNaN(nb)) return nb - na;
        return b.localeCompare(a);
      });
    return res.status(200).json({ ok: true, slugs });
  } catch (e) {
    return res.status(500).json({ error: String(e.message) });
  }
}
