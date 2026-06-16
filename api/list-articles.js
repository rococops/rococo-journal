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
    return res.status(401).json({ error: '인증 실패' });

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
        const isPureNum = s => /^\d+$/.test(s);
        const cNum = s => parseInt(s.replace(/^c/, ''));
        // 순수 숫자(어드민 발행글)는 항상 위
        if (isPureNum(a) && !isPureNum(b)) return -1;
        if (!isPureNum(a) && isPureNum(b)) return 1;
        // 둘 다 순수 숫자거나 둘 다 c-prefix: 숫자 내림차순
        return cNum(b) - cNum(a);
      });
    return res.status(200).json({ ok: true, slugs });
  } catch (e) {
    return res.status(500).json({ error: String(e.message) });
  }
}
