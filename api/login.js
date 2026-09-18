import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

export default async function handler(req, res) {
  const origin = req.headers.origin || '';
  const allowed = ['https://journal.rococops.com', 'https://rococo-journal-api.vercel.app'];
  res.setHeader('Access-Control-Allow-Origin', allowed.includes(origin) ? origin : allowed[0]);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { username, password } = req.body || {};
  if (!username || !password) {
    return res.status(400).json({ error: '아이디와 비밀번호를 입력해주세요.' });
  }

  const { data: member, error } = await supabase
    .from('members')
    .select('id, username, password_hash, name')
    .eq('username', username.trim().toLowerCase())
    .maybeSingle();

  if (error) return res.status(500).json({ error: error.message });
  if (!member) return res.status(401).json({ error: '아이디 또는 비밀번호가 올바르지 않습니다.' });

  const valid = await bcrypt.compare(password, member.password_hash);
  if (!valid) return res.status(401).json({ error: '아이디 또는 비밀번호가 올바르지 않습니다.' });

  const token = jwt.sign(
    { sub: member.id, username: member.username, name: member.name },
    process.env.JWT_SECRET,
    { expiresIn: '30d' }
  );

  return res.status(200).json({ ok: true, token, name: member.name });
}
