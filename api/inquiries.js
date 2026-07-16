import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

function authCheck(req, res) {
  const password = req.query.password || req.body?.password;
  if (password !== process.env.ADMIN_PASSWORD) {
    res.status(401).json({ error: '인증 실패' });
    return false;
  }
  return true;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'GET') {
    if (!authCheck(req, res)) return;
    const { data, error } = await supabase
      .from('inquiries')
      .select('id, name, phone, contact_method, message, source, status, created_at')
      .order('created_at', { ascending: false })
      .limit(200);
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok: true, inquiries: data });
  }

  if (req.method === 'PATCH') {
    if (!authCheck(req, res)) return;
    const { id, status } = req.body || {};
    if (!id || !['pending', 'done'].includes(status)) {
      return res.status(400).json({ error: '잘못된 요청' });
    }
    const { error } = await supabase.from('inquiries').update({ status }).eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok: true });
  }

  if (req.method === 'DELETE') {
    if (!authCheck(req, res)) return;
    const { id, ids, status_filter } = req.body || {};
    let query = supabase.from('inquiries').delete();
    if (status_filter) {
      query = query.eq('status', status_filter);
    } else if (ids && Array.isArray(ids)) {
      query = query.in('id', ids);
    } else if (id) {
      query = query.eq('id', id);
    } else {
      return res.status(400).json({ error: 'id / ids / status_filter 중 하나 필요' });
    }
    const { error } = await query;
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok: true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
