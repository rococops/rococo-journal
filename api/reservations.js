import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

function auth(req, res) {
  const pw = req.query.password || req.body?.password;
  if (pw !== process.env.ADMIN_PASSWORD) { res.status(401).json({ error: '인증 실패' }); return false; }
  return true;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'GET') {
    if (!auth(req, res)) return;
    const { month } = req.query; // e.g. "2025-07"
    let query = supabase.from('reservations')
      .select('id, name, phone, contact_method, visit_type, category, date, time, status, note, created_at')
      .order('date', { ascending: true }).order('time', { ascending: true });
    if (month) {
      query = query.gte('date', `${month}-01`).lte('date', `${month}-31`);
    }
    const { data, error } = await query.limit(500);
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok: true, reservations: data });
  }

  if (req.method === 'PATCH') {
    if (!auth(req, res)) return;
    const { id, status, note } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id 필요' });
    const update = {};
    if (status !== undefined) {
      if (!['new','confirmed','cancelled'].includes(status)) return res.status(400).json({ error: '잘못된 status' });
      update.status = status;
    }
    if (note !== undefined) update.note = note;
    const { error } = await supabase.from('reservations').update(update).eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok: true });
  }

  if (req.method === 'DELETE') {
    if (!auth(req, res)) return;
    const { id } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id 필요' });
    const { error } = await supabase.from('reservations').delete().eq('id', id);
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok: true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
