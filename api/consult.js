// 온라인 상담 — 접수(기본), 사진 업로드(?action=upload), 본인 글 조회(?action=lookup)
// Vercel Hobby 서버리스 함수 12개 제한 때문에 파일을 늘리지 않고 action 쿼리로 분기
import { Resend } from 'resend';
import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';

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

// 본인 상담 글 조회 — 이름 + 글 비밀번호
async function handleLookup(req, res) {
  const { name, password } = req.body || {};
  if (!name || !password) return res.status(400).json({ error: '이름과 비밀번호를 입력해주세요.' });

  const { data, error } = await supabase
    .from('inquiries')
    .select('id, name, message, reply, replied_at, created_at, status, photos, post_password_hash')
    .eq('name', name.trim())
    .order('created_at', { ascending: false })
    .limit(20);

  if (error) return res.status(500).json({ error: error.message });

  const mine = [];
  for (const row of data || []) {
    if (!row.post_password_hash) continue;
    if (await bcrypt.compare(password, row.post_password_hash)) {
      delete row.post_password_hash;
      mine.push(row);
    }
  }

  if (!mine.length) return res.status(404).json({ error: '일치하는 상담 내역이 없습니다. 이름과 비밀번호를 확인해주세요.' });
  return res.status(200).json({ ok: true, inquiries: mine });
}

// 상담 접수
async function handleSubmit(req, res) {
  const { name, phone, email, contact_method, message, source, photos, password } = req.body || {};

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
  if (!password || String(password).length < 4) {
    return res.status(400).json({ error: '답변 조회용 비밀번호를 4자 이상 입력해주세요.' });
  }

  const photoPaths = Array.isArray(photos) ? photos.filter(p => typeof p === 'string').slice(0, 5) : [];
  const post_password_hash = await bcrypt.hash(String(password), 10);

  const { error: dbError } = await supabase
    .from('inquiries')
    .insert({
      name, phone: phone || null, email: email || null, contact_method, message, source,
      photos: photoPaths, post_password_hash
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
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const action = req.query?.action;
  if (action === 'upload') return handleUpload(req, res);
  if (action === 'lookup') return handleLookup(req, res);
  return handleSubmit(req, res);
}
