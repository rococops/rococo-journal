import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

function authCheck(req, res) {
  const password = (req.headers.authorization||'').replace('Bearer ','') || req.query.password || req.body?.password;
  if (password !== process.env.ADMIN_PASSWORD) {
    res.status(401).json({ error: '인증 실패' });
    return false;
  }
  return true;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'GET') {
    if (!authCheck(req, res)) return;
    const { data, error } = await supabase
      .from('inquiries')
      .select('id, name, phone, email, contact_method, message, source, status, note, created_at, photos, reply, replied_at, message_ko, source_lang')
      .order('created_at', { ascending: false })
      .limit(200);
    if (error) return res.status(500).json({ error: error.message });

    // 사진은 비공개 버킷이라 관리자에게만 임시 열람 URL(1시간)을 만들어 전달
    for (const row of data || []) {
      const paths = Array.isArray(row.photos) ? row.photos : [];
      row.photo_urls = [];
      for (const p of paths) {
        const { data: signed } = await supabase.storage.from('consult-photos').createSignedUrl(p, 3600);
        if (signed?.signedUrl) row.photo_urls.push(signed.signedUrl);
      }
    }

    return res.status(200).json({ ok: true, inquiries: data });
  }

  if (req.method === 'PATCH') {
    if (!authCheck(req, res)) return;
    const { id, status, note, reply } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id 필요' });
    const update = {};
    if (status !== undefined) {
      if (!['new', 'in_progress', 'done'].includes(status)) {
        return res.status(400).json({ error: '잘못된 status' });
      }
      update.status = status;
    }
    if (note !== undefined) update.note = note;
    if (reply !== undefined) {
      update.reply = reply;
      update.replied_at = reply ? new Date().toISOString() : null;
    }
    if (!Object.keys(update).length) return res.status(400).json({ error: '변경할 필드 없음' });
    const { error } = await supabase.from('inquiries').update(update).eq('id', id);
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
