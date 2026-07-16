import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

function toMin(t) { const [h,m] = t.split(':').map(Number); return h*60+m; }
function toTime(m) { return `${String(Math.floor(m/60)).padStart(2,'0')}:${String(m%60).padStart(2,'0')}`; }

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'GET') {
    const { date } = req.query;
    if (!date) return res.status(400).json({ error: 'date 필요' });

    const { data: row } = await supabase.from('settings').select('value').eq('key','schedule').single();
    const sch = row?.value || {};

    if ((sch.blocked_dates||[]).includes(date)) {
      return res.status(200).json({ ok:true, slots:[], closed:true, reason:'휴진일' });
    }

    const dow = new Date(date + 'T12:00:00Z').getDay();
    const dayCfg = (sch.custom_dates||{})[date] || sch.weekdays?.[String(dow)];
    if (!dayCfg?.enabled) {
      return res.status(200).json({ ok:true, slots:[], closed:true, reason:'휴진' });
    }

    const dur = sch.slot_duration || 30;
    const slots = [];
    for (let m = toMin(dayCfg.open); m < toMin(dayCfg.close); m += dur) slots.push(toTime(m));

    const { data: booked } = await supabase
      .from('reservations').select('time').eq('date', date).neq('status','cancelled');
    const bookedSet = new Set((booked||[]).map(r => r.time));

    return res.status(200).json({ ok:true, slots: slots.filter(s => !bookedSet.has(s)) });
  }

  if (req.method === 'POST') {
    const { name, phone, contact_method, visit_type, category, date, time } = req.body || {};
    if (!name||!phone||!contact_method||!visit_type||!category||!date||!time) {
      return res.status(400).json({ error: '필수 항목이 누락되었습니다.' });
    }

    const { data: dup } = await supabase
      .from('reservations').select('id').eq('date',date).eq('time',time).neq('status','cancelled');
    if (dup?.length) return res.status(409).json({ error: '이미 예약된 시간입니다. 다른 시간을 선택해주세요.' });

    const { error } = await supabase.from('reservations').insert({ name, phone, contact_method, visit_type, category, date, time });
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok:true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
