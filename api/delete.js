const GITHUB_REPO = 'rococops/rococo-journal';
const GITHUB_API  = 'https://api.github.com';

async function ghFetch(path, token, opts = {}) {
  return fetch(`${GITHUB_API}/repos/${GITHUB_REPO}/contents/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    ...opts,
  });
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://journal.rococops.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { password, catPath, subDir, slug } = req.body || {};

  if (password !== process.env.ADMIN_PASSWORD)
    return res.status(401).json({ error: '비밀번호가 올바르지 않습니다.' });
  if (!catPath || !subDir || !slug)
    return res.status(400).json({ error: '필수 항목 누락' });

  const token = process.env.GITHUB_TOKEN;
  const filePath = `${catPath}/${subDir}/${slug}/index.html`;

  try {
    // SHA 조회
    const check = await ghFetch(filePath, token);
    if (!check.ok) return res.status(404).json({ error: '파일을 찾을 수 없습니다.' });
    const { sha } = await check.json();

    // 삭제
    const del = await ghFetch(filePath, token, {
      method: 'DELETE',
      body: JSON.stringify({ message: `글 삭제: ${catPath}/${subDir}/${slug}`, sha, branch: 'main' }),
    });

    if (!del.ok) return res.status(500).json({ error: 'GitHub 삭제 실패' });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(500).json({ error: String(e.message) });
  }
}
