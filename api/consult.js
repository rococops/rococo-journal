// 온라인 상담 — 접수(기본), 사진 업로드(?action=upload), 본인 글 조회(?action=lookup)
// Vercel Hobby 서버리스 함수 12개 제한 때문에 파일을 늘리지 않고 action 쿼리로 분기
import { Resend } from 'resend';
import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const resend = new Resend(process.env.RESEND_API_KEY);
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const ALLOWED_CONTACT_METHODS = ['전화', '카카오톡', '이메일'];
const BUCKET = 'consult-photos';
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// 사진 업로드 — 클라이언트에서 리사이즈한 dataURL을 받아 비공개 버킷에 저장하고 경로만 반환.
// (버킷이 없으면 만들어 두어 최초 1회 수동 설정이 필요 없게 함)
async function handleUpload(req, res) {
  const { dataUrl } = req.body || {};
  if (!dataUrl || typeof dataUrl !== 'string' || !dataUrl.startsWith('data:image/')) {
    return res.status(400).json({ error: '이미지 형식이 올바르지 않습니다.' });
  }

  const match = dataUrl.match(/^data:(image\/(jpeg|png|webp));base64,(.+)$/);
  if (!match) return res.status(400).json({ error: '지원하지 않는 이미지 형식입니다.' });

  const contentType = match[1];
  const buffer = Buffer.from(match[3], 'base64');
  if (buffer.length > 4 * 1024 * 1024) {
    return res.status(413).json({ error: '이미지 용량이 너무 큽니다.' });
  }

  const ext = contentType === 'image/png' ? 'png' : contentType === 'image/webp' ? 'webp' : 'jpg';
  const path = `${new Date().toISOString().slice(0, 10)}/${Date.now()}-${Math.random().toString(36).slice(2, 8)}.${ext}`;

  let { error } = await supabase.storage.from(BUCKET).upload(path, buffer, { contentType });
  if (error && /bucket/i.test(error.message || '')) {
    await supabase.storage.createBucket(BUCKET, { public: false });
    ({ error } = await supabase.storage.from(BUCKET).upload(path, buffer, { contentType }));
  }
  if (error) return res.status(500).json({ error: error.message });

  return res.status(200).json({ ok: true, path });
}

// 로그인 회원이면 토큰에서 회원 id를 꺼냄(비로그인이면 null) — 본인 글은 비밀번호 없이 열람
function optionalMember(req) {
  const token = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!token) return null;
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (e) {
    return null;
  }
}

// 이름 마스킹 — 홍길동 → 홍*동, 홍길 → 홍*, 영문/닉네임은 가운데를 *로
function maskName(name) {
  const n = String(name || '').trim();
  if (n.length <= 1) return n || '-';
  if (n.length === 2) return n[0] + '*';
  return n[0] + '*'.repeat(n.length - 2) + n[n.length - 1];
}

// 게시판 목록 — 제목·작성자(마스킹)·날짜·답변여부만 공개. 내용/사진/연락처는 노출하지 않음
async function handleList(req, res) {
  const page = Math.max(1, parseInt(req.body?.page, 10) || 1);
  const size = 15;
  const from = (page - 1) * size;

  const member = optionalMember(req);

  const { data, error, count } = await supabase
    .from('inquiries')
    .select('id, name, title, created_at, reply, member_id', { count: 'exact' })
    .order('created_at', { ascending: false })
    .range(from, from + size - 1);

  if (error) return res.status(500).json({ error: error.message });

  const list = (data || []).map(r => ({
    id: r.id,
    title: r.title || '상담 문의',
    name: maskName(r.name),
    created_at: r.created_at,
    answered: !!r.reply,
    mine: !!(member && r.member_id && r.member_id === member.sub)
  }));

  return res.status(200).json({ ok: true, inquiries: list, total: count || 0, page, size });
}

// 글 열람 — 목록에서 글을 선택한 뒤 해당 글의 비밀번호를 입력받아 확인
async function handleView(req, res) {
  const { id, password } = req.body || {};
  if (!id) return res.status(400).json({ error: '잘못된 요청입니다.' });

  const { data: row, error } = await supabase
    .from('inquiries')
    .select('id, name, title, message, reply, replied_at, created_at, photos, post_password_hash, member_id')
    .eq('id', id)
    .maybeSingle();

  if (error) return res.status(500).json({ error: error.message });
  if (!row) return res.status(404).json({ error: '글을 찾을 수 없습니다.' });

  // 로그인한 본인 글이면 비밀번호 없이 열람
  const member = optionalMember(req);
  const isOwner = !!(member && row.member_id && row.member_id === member.sub);

  if (!isOwner) {
    if (!password) return res.status(400).json({ error: '비밀번호를 입력해주세요.' });
    if (!row.post_password_hash) {
      return res.status(403).json({ error: '비밀번호가 설정되지 않은 글입니다. 병원으로 문의해주세요.' });
    }
    const ok = await bcrypt.compare(String(password), row.post_password_hash);
    if (!ok) return res.status(401).json({ error: '비밀번호가 올바르지 않습니다.' });
  }

  delete row.post_password_hash;
  delete row.member_id;
  row.name = maskName(row.name);
  row.photo_count = Array.isArray(row.photos) ? row.photos.length : 0;
  delete row.photos;

  return res.status(200).json({ ok: true, inquiry: row });
}

// 상담 접수
async function handleSubmit(req, res) {
  const { name, phone, email, contact_method, message, source, photos, password, title } = req.body || {};
  const member = optionalMember(req);

  if (!name || !message || !ALLOWED_CONTACT_METHODS.includes(contact_method)) {
    return res.status(400).json({ error: '필수 항목이 누락되었거나 값이 올바르지 않습니다.' });
  }
  // 해외 환자는 한국 휴대폰이 없을 수 있어 연락처·이메일 중 하나만 있으면 접수 가능
  if (!phone && !email) {
    return res.status(400).json({ error: '연락처 또는 이메일 중 하나는 입력해주세요.' });
  }
  if (email && !EMAIL_RE.test(email)) {
    return res.status(400).json({ error: '이메일 형식이 올바르지 않습니다.' });
  }
  if (contact_method === '이메일' && !email) {
    return res.status(400).json({ error: '이메일로 답변받으시려면 이메일을 입력해주세요.' });
  }
  if (contact_method !== '이메일' && !phone) {
    return res.status(400).json({ error: '전화·카카오톡으로 답변받으시려면 연락처를 입력해주세요.' });
  }
  // 로그인 회원은 본인 계정으로 글을 열람할 수 있어 비밀번호가 필수가 아님
  if (!member && (!password || String(password).length < 4)) {
    return res.status(400).json({ error: '답변 조회용 비밀번호를 4자 이상 입력해주세요.' });
  }

  const photoPaths = Array.isArray(photos) ? photos.filter(p => typeof p === 'string').slice(0, 5) : [];
  const post_password_hash = password ? await bcrypt.hash(String(password), 10) : null;

  const { error: dbError } = await supabase
    .from('inquiries')
    .insert({
      name, phone: phone || null, email: email || null, contact_method, message, source,
      title: (title && String(title).trim()) || '상담 문의',
      photos: photoPaths, post_password_hash,
      member_id: member ? member.sub : null
    });

  if (dbError) {
    console.error('Supabase insert error:', dbError);
    return res.status(500).json({ error: '접수 중 오류가 발생했습니다.' });
  }

  // 병원 알림 메일 — 실패해도 접수 자체는 성공 처리(환자 입장에서 접수는 끝난 것)
  try {
    await resend.emails.send({
      from: 'Rococo Journal <onboarding@resend.dev>',
      to: process.env.NOTIFY_EMAIL,
      subject: `[${source || '온라인 상담'}] ${name}님 문의${photoPaths.length ? ` (사진 ${photoPaths.length}장)` : ''}`,
      html: `
        <h2>새 상담 신청이 도착했습니다</h2>
        <p><strong>이름:</strong> ${name}</p>
        <p><strong>연락처:</strong> ${phone || '-'}</p>
        <p><strong>이메일:</strong> ${email || '-'}</p>
        <p><strong>희망 연락 방법:</strong> ${contact_method}</p>
        <p><strong>첨부 사진:</strong> ${photoPaths.length}장</p>
        <p><strong>문의 내용:</strong></p>
        <p>${String(message).replace(/\n/g, '<br>')}</p>
        <p>관리자 페이지에서 사진 확인 및 답변 등록이 가능합니다.</p>
      `
    });
  } catch (mailError) {
    console.error('Resend send error:', mailError);
  }

  return res.status(200).json({ ok: true });
}

export default async function handler(req, res) {
  // GitHub Pages(다른 도메인)에서 호출하므로 CORS 허용
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const action = req.query?.action;
  if (action === 'upload') return handleUpload(req, res);
  if (action === 'list') return handleList(req, res);
  if (action === 'view') return handleView(req, res);
  return handleSubmit(req, res);
}
