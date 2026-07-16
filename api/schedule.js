import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, PATCH, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'GET') {
    const { data, error } = await supabase.from('settings').select('value').eq('key','schedule').single();
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok:true, schedule: data.value });
  }

  if (req.method === 'PATCH') {
    const password = req.body?.password;
    if (password !== process.env.ADMIN_PASSWORD) return res.status(401).json({ error: '인증 실패' });
    const { schedule } = req.body || {};
    if (!schedule) return res.status(400).json({ error: 'schedule 필요' });
    const { error } = await supabase.from('settings')
      .update({ value: schedule, updated_at: new Date().toISOString() }).eq('key','schedule');
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok:true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
