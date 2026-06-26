import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { password } = req.query || {};
  if (password !== process.env.ADMIN_PASSWORD) {
    return res.status(401).json({ error: '비밀번호가 올바르지 않습니다.' });
  }

  const todayStart = new Date();
  todayStart.setHours(0, 0, 0, 0);
  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

  const [todayRes, weekRes, totalRes] = await Promise.all([
    supabase.from('pageviews').select('*', { count: 'exact', head: true }).gte('created_at', todayStart.toISOString()),
    supabase.from('pageviews').select('path, referrer, created_at').gte('created_at', sevenDaysAgo.toISOString()),
    supabase.from('pageviews').select('*', { count: 'exact', head: true }),
  ]);

  if (weekRes.error) {
    console.error('Supabase select error:', weekRes.error);
    return res.status(500).json({ error: '통계 조회 실패' });
  }

  const rows = weekRes.data || [];

  // 인기 페이지 TOP 10 (최근 7일)
  const pathCounts = {};
  const referrerCounts = {};
  for (const row of rows) {
    pathCounts[row.path] = (pathCounts[row.path] || 0) + 1;
    const ref = row.referrer || '(직접 입력)';
    referrerCounts[ref] = (referrerCounts[ref] || 0) + 1;
  }
  const topPages = Object.entries(pathCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([path, count]) => ({ path, count }));
  const topReferrers = Object.entries(referrerCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([referrer, count]) => ({ referrer, count }));

  return res.status(200).json({
    ok: true,
    today: todayRes.count || 0,
    last7days: rows.length,
    total: totalRes.count || 0,
    topPages,
    topReferrers,
  });
}
