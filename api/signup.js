import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const USERNAME_RE = /^[a-z0-9_]{4,16}$/;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^01[0-9]-?\d{3,4}-?\d{4}$/;

export default async function handler(req, res) {
  const origin = req.headers.origin || '';
  const allowed = ['https://journal.rococops.com', 'https://rococo-journal-api.vercel.app'];
  res.setHeader('Access-Control-Allow-Origin', allowed.includes(origin) ? origin : allowed[0]);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { username, password, name, phone, email, termsAgreed, privacyAgreed } = req.body || {};

  if (!termsAgreed || !privacyAgreed) {
    return res.status(400).json({ error: '이용약관 및 개인정보 수집·이용에 동의해주세요.' });
  }
  if (!username || !USERNAME_RE.test(username)) {
    return res.status(400).json({ error: '아이디는 영문 소문자·숫자·언더스코어 4~16자로 입력해주세요.' });
  }
  if (!password || password.length < 8) {
    return res.status(400).json({ error: '비밀번호는 8자 이상 입력해주세요.' });
  }
  if (!name || !name.trim()) {
    return res.status(400).json({ error: '이름을 입력해주세요.' });
  }
  if (!phone || !PHONE_RE.test(phone)) {
    return res.status(400).json({ error: '연락처 형식이 올바르지 않습니다.' });
  }
  if (!email || !EMAIL_RE.test(email)) {
    return res.status(400).json({ error: '이메일 형식이 올바르지 않습니다.' });
  }

  const normalizedPhone = phone.replace(/-/g, '');
  const normalizedUsername = username.toLowerCase();
  const normalizedEmail = email.toLowerCase();

  const { count: dupCount, error: dupError } = await supabase
    .from('members')
    .select('id', { count: 'exact', head: true })
    .or(`username.eq.${normalizedUsername},email.eq.${normalizedEmail},phone.eq.${normalizedPhone}`);

  if (dupError) return res.status(500).json({ error: dupError.message });
  if (dupCount > 0) {
    return res.status(409).json({ error: '이미 가입된 아이디·이메일·연락처가 있습니다.' });
  }

  const password_hash = await bcrypt.hash(password, 10);

  const { error: insertError } = await supabase.from('members').insert({
    username: normalizedUsername,
    password_hash,
    name: name.trim(),
    phone: normalizedPhone,
    email: normalizedEmail,
    terms_agreed: true,
    privacy_agreed: true
  });

  if (insertError) {
    if (insertError.code === '23505') {
      return res.status(409).json({ error: '이미 가입된 아이디·이메일·연락처가 있습니다.' });
    }
    return res.status(500).json({ error: insertError.message });
  }

  return res.status(200).json({ ok: true });
}
