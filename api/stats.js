import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const password = (req.headers.authorization||'').replace('Bearer ','') || req.query.password;
  if (password !== process.env.ADMIN_PASSWORD) {
    return res.status(401).json({ error: '비밀번호가 올바르지 않습니다.' });
  }

  // Vercel 서버는 UTC로 동작해서 그냥 setHours(0,0,0,0)을 쓰면
  // "오늘"이 한국시간 오전 9시에 리셋됨 → 한국시간(UTC+9) 기준으로 직접 계산
  const KST_OFFSET = 9 * 60 * 60 * 1000;
  function kstDateStr(dateLike) {
    return new Date(new Date(dateLike).getTime() + KST_OFFSET).toISOString().slice(0, 10);
  }
  function kstMidnightUtc(dateLike) {
    const k = new Date(new Date(dateLike).getTime() + KST_OFFSET);
    return new Date(Date.UTC(k.getUTCFullYear(), k.getUTCMonth(), k.getUTCDate()) - KST_OFFSET);
  }

  const todayStart = kstMidnightUtc(Date.now());
  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);

  // Supabase는 한 번에 최대 1000행만 돌려준다. 그대로 쓰면 방문이 1000건을 넘는 순간
  // 뒤쪽 날짜가 통째로 잘려서 그래프가 0으로 붙는다 → 1000행씩 나눠 끝까지 가져온다
  async function fetchAll(buildQuery) {
    const PAGE = 1000;
    const all = [];
    for (let from = 0; from < 200000; from += PAGE) {
      const { data, error } = await buildQuery().order('created_at', { ascending: true }).range(from, from + PAGE - 1);
      if (error) return { data: null, error };
      all.push(...data);
      if (data.length < PAGE) break;
    }
    return { data: all, error: null };
  }

  const [todayRes, weekRes, totalRes, monthRes, consultRes] = await Promise.all([
    supabase.from('pageviews').select('*', { count: 'exact', head: true }).gte('created_at', todayStart.toISOString()),
    fetchAll(() => supabase.from('pageviews').select('path, referrer, created_at').gte('created_at', sevenDaysAgo.toISOString())),
    supabase.from('pageviews').select('*', { count: 'exact', head: true }),
    fetchAll(() => supabase.from('pageviews').select('created_at').gte('created_at', thirtyDaysAgo.toISOString())),
    supabase.from('inquiries').select('*', { count: 'exact', head: true }).gte('created_at', thirtyDaysAgo.toISOString()),
  ]);

  if (weekRes.error) {
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

  // 최근 30일 일별 방문수
  const dailyCounts = {};
  for (let i = 29; i >= 0; i--) {
    dailyCounts[kstDateStr(Date.now() - i * 24 * 60 * 60 * 1000)] = 0;
  }
  for (const row of (monthRes.data || [])) {
    const day = kstDateStr(row.created_at);
    if (day in dailyCounts) dailyCounts[day]++;
  }
  const dailyViews = Object.entries(dailyCounts).map(([date, count]) => ({ date, count }));

  return res.status(200).json({
    ok: true,
    today: todayRes.count || 0,
    last7days: rows.length,
    total: totalRes.count || 0,
    consultCount30: consultRes.count || 0,
    dailyViews,
    topPages,
    topReferrers,
  });
}
