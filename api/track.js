import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { path, referrer } = req.body || {};
  if (!path || typeof path !== 'string') {
    return res.status(400).json({ error: 'path가 필요합니다.' });
  }

  const { error } = await supabase
    .from('pageviews')
    .insert({
      path: path.slice(0, 500),
      referrer: (referrer || '').slice(0, 500),
    });

  if (error) console.error('Supabase insert error:', error);

  return res.status(200).json({ ok: true });
}
