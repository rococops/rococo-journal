import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const FIELDS = ['username', 'email', 'phone'];

export default async function handler(req, res) {
  const origin = req.headers.origin || '';
  const allowed = ['https://journal.rococops.com', 'https://rococo-journal-api.vercel.app'];
  res.setHeader('Access-Control-Allow-Origin', allowed.includes(origin) ? origin : allowed[0]);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { field, value } = req.body || {};
  if (!FIELDS.includes(field) || !value) {
    return res.status(400).json({ error: '잘못된 요청입니다.' });
  }

  const query = supabase.from('members').select('id', { count: 'exact', head: true });
  const { count, error } = field === 'phone'
    ? await query.eq('phone', value.replace(/-/g, ''))
    : await query.eq(field, value.toLowerCase());

  if (error) return res.status(500).json({ error: error.message });
  return res.status(200).json({ ok: true, available: count === 0 });
}
