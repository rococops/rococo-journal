import { Resend } from 'resend';
import { createClient } from '@supabase/supabase-js';

const resend = new Resend(process.env.RESEND_API_KEY);
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const ALLOWED_CONTACT_METHODS = ['전화', '카카오톡'];

export default async function handler(req, res) {
  // GitHub Pages(다른 도메인)에서 호출하므로 CORS 허용
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { name, phone, contact_method, message, source } = req.body || {};

  if (!name || !phone || !message || !ALLOWED_CONTACT_METHODS.includes(contact_method)) {
    return res.status(400).json({ error: '필수 항목이 누락되었거나 값이 올바르지 않습니다.' });
  }

  // Supabase에 상담 내역 저장 (실패해도 이메일 발송은 계속 진행)
  const { error: dbError } = await supabase
    .from('inquiries')
    .insert({ name, phone, contact_method, message, source });

  if (dbError) console.error('Supabase insert error:', dbError);

  let sendResult;
  try {
    sendResult = await resend.emails.send({
      from: 'Rococo Journal <onboarding@resend.dev>',
      to: process.env.NOTIFY_EMAIL,
      subject: `[${source || '온라인 상담 페이지'} 상담 문의] - ${name}`,
      html: `
        <h2>새 상담 신청이 도착했습니다</h2>
        <p><strong>이름:</strong> ${name}</p>
        <p><strong>전화번호:</strong> ${phone}</p>
        <p><strong>희망 연락 방법:</strong> ${contact_method}</p>
        <p><strong>문의 내용:</strong></p>
        <p>${String(message).replace(/\n/g, '<br>')}</p>
      `
    });
  } catch (mailError) {
    console.error('Resend send error:', mailError);
    return res.status(500).json({ error: '이메일 전송 실패' });
  }

  if (sendResult?.error) {
    console.error('Resend API error:', sendResult.error);
    return res.status(500).json({ error: '이메일 전송 실패', detail: sendResult.error });
  }

  return res.status(200).json({ ok: true });
}
