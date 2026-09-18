// 회원가입/로그인/중복확인을 한 파일로 묶음 — Vercel Hobby 플랜 서버리스 함수 12개 제한 때문에
// signup.js/login.js/check-duplicate.js 3개를 따로 두면 함수 개수 초과로 배포가 실패함.
// ?action=signup | login | check-duplicate 쿼리로 라우팅.
import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const USERNAME_RE = /^[a-z0-9_]{4,16}$/;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^01[0-9]-?\d{3,4}-?\d{4}$/;
const DUP_FIELDS = ['username', 'email', 'phone'];

async function handleCheckDuplicate(req, res) {
  const { field, value } = req.body || {};
  if (!DUP_FIELDS.includes(field) || !value) {
    return res.status(400).json({ error: '잘못된 요청입니다.' });
  }
  const query = supabase.from('members').select('id', { count: 'exact', head: true });
  const { count, error } = field === 'phone'
    ? await query.eq('phone', value.replace(/-/g, ''))
    : await query.eq(field, value.toLowerCase());

  if (error) return res.status(500).json({ error: error.message });
  return res.status(200).json({ ok: true, available: count === 0 });
}

async function handleSignup(req, res) {
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

async function handleLogin(req, res) {
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

function requireMember(req, res) {
  const authHeader = req.headers.authorization || '';
  const token = authHeader.replace(/^Bearer\s+/i, '');
  if (!token) { res.status(401).json({ error: '로그인이 필요합니다.' }); return null; }
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (e) {
    res.status(401).json({ error: '로그인이 만료되었습니다. 다시 로그인해주세요.' });
    return null;
  }
}

async function handleMe(req, res) {
  const payload = requireMember(req, res);
  if (!payload) return;

  const { data: member, error } = await supabase
    .from('members')
    .select('username, name, phone, email, created_at')
    .eq('id', payload.sub)
    .maybeSingle();

  if (error) return res.status(500).json({ error: error.message });
  if (!member) return res.status(404).json({ error: '회원 정보를 찾을 수 없습니다.' });
  return res.status(200).json({ ok: true, member });
}

async function handleUpdateProfile(req, res) {
  const payload = requireMember(req, res);
  if (!payload) return;

  const { name, phone, email } = req.body || {};
  if (!name || !name.trim()) return res.status(400).json({ error: '이름을 입력해주세요.' });
  if (!phone || !PHONE_RE.test(phone)) return res.status(400).json({ error: '연락처 형식이 올바르지 않습니다.' });
  if (!email || !EMAIL_RE.test(email)) return res.status(400).json({ error: '이메일 형식이 올바르지 않습니다.' });

  const normalizedPhone = phone.replace(/-/g, '');
  const normalizedEmail = email.toLowerCase();

  // 본인 것을 제외하고 다른 회원이 같은 연락처/이메일을 쓰고 있는지 확인
  const { count: dupCount, error: dupError } = await supabase
    .from('members')
    .select('id', { count: 'exact', head: true })
    .or(`email.eq.${normalizedEmail},phone.eq.${normalizedPhone}`)
    .neq('id', payload.sub);

  if (dupError) return res.status(500).json({ error: dupError.message });
  if (dupCount > 0) return res.status(409).json({ error: '이미 사용 중인 이메일 또는 연락처입니다.' });

  const { error } = await supabase
    .from('members')
    .update({ name: name.trim(), phone: normalizedPhone, email: normalizedEmail })
    .eq('id', payload.sub);

  if (error) {
    if (error.code === '23505') return res.status(409).json({ error: '이미 사용 중인 이메일 또는 연락처입니다.' });
    return res.status(500).json({ error: error.message });
  }
  return res.status(200).json({ ok: true, name: name.trim() });
}

async function handleChangePassword(req, res) {
  const payload = requireMember(req, res);
  if (!payload) return;

  const { currentPassword, newPassword } = req.body || {};
  if (!currentPassword || !newPassword) {
    return res.status(400).json({ error: '현재 비밀번호와 새 비밀번호를 입력해주세요.' });
  }
  if (newPassword.length < 8) {
    return res.status(400).json({ error: '새 비밀번호는 8자 이상 입력해주세요.' });
  }

  const { data: member, error } = await supabase
    .from('members')
    .select('password_hash')
    .eq('id', payload.sub)
    .maybeSingle();

  if (error) return res.status(500).json({ error: error.message });
  if (!member) return res.status(404).json({ error: '회원 정보를 찾을 수 없습니다.' });

  const valid = await bcrypt.compare(currentPassword, member.password_hash);
  if (!valid) return res.status(401).json({ error: '현재 비밀번호가 올바르지 않습니다.' });

  const password_hash = await bcrypt.hash(newPassword, 10);
  const { error: updateError } = await supabase
    .from('members')
    .update({ password_hash })
    .eq('id', payload.sub);

  if (updateError) return res.status(500).json({ error: updateError.message });
  return res.status(200).json({ ok: true });
}

async function handleDeleteAccount(req, res) {
  const payload = requireMember(req, res);
  if (!payload) return;

  const { error } = await supabase.from('members').delete().eq('id', payload.sub);
  if (error) return res.status(500).json({ error: error.message });
  return res.status(200).json({ ok: true });
}

// 관리자(병원)용 — 다른 admin API들과 동일하게 ADMIN_PASSWORD로 인증.
// 비밀번호를 잊은 환자는 로그인이 안 돼 스스로 탈퇴할 수 없으므로,
// 문의를 받으면 병원이 해당 계정을 삭제해 재가입할 수 있게 해주는 용도.
function requireAdmin(req, res) {
  const pw = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!pw || pw !== process.env.ADMIN_PASSWORD) {
    res.status(401).json({ error: '인증 실패' });
    return false;
  }
  return true;
}

async function handleAdminList(req, res) {
  if (!requireAdmin(req, res)) return;
  const { data, error } = await supabase
    .from('members')
    .select('id, username, name, phone, email, created_at')
    .order('created_at', { ascending: false })
    .limit(500);
  if (error) return res.status(500).json({ error: error.message });
  return res.status(200).json({ ok: true, members: data });
}

async function handleAdminDelete(req, res) {
  if (!requireAdmin(req, res)) return;
  const { id } = req.body || {};
  if (!id) return res.status(400).json({ error: 'id 필요' });
  const { error } = await supabase.from('members').delete().eq('id', id);
  if (error) return res.status(500).json({ error: error.message });
  return res.status(200).json({ ok: true });
}

export default async function handler(req, res) {
  const origin = req.headers.origin || '';
  const allowed = ['https://journal.rococops.com', 'https://rococo-journal-api.vercel.app'];
  res.setHeader('Access-Control-Allow-Origin', allowed.includes(origin) ? origin : allowed[0]);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const action = req.query?.action;
  if (action === 'signup') return handleSignup(req, res);
  if (action === 'login') return handleLogin(req, res);
  if (action === 'check-duplicate') return handleCheckDuplicate(req, res);
  if (action === 'me') return handleMe(req, res);
  if (action === 'update-profile') return handleUpdateProfile(req, res);
  if (action === 'change-password') return handleChangePassword(req, res);
  if (action === 'delete-account') return handleDeleteAccount(req, res);
  if (action === 'admin-list') return handleAdminList(req, res);
  if (action === 'admin-delete') return handleAdminDelete(req, res);
  return res.status(400).json({ error: '잘못된 요청입니다.' });
}
