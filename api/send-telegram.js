// 폼의 인입경로(한글) → 분양천국 대시보드가 이해하는 utm_source로 매핑
const SOURCE_TO_UTM_SOURCE = {
  '네이버 검색': 'naver',
  '네이버 블로그': 'naver',
  '네이버 배너광고': 'naver',
  '유튜브': 'youtube',
  '인스타그램': 'instagram',
  '페이스북': 'facebook',
};

function resolveUtmSource(funnel) {
  if (!funnel) return 'other';
  const values = funnel.split(',').map((v) => v.trim());
  for (const v of values) {
    if (SOURCE_TO_UTM_SOURCE[v]) return SOURCE_TO_UTM_SOURCE[v];
  }
  return 'other';
}

// 분양천국 대시보드로 리드 전송 (고객DB 적재 + 담당자 문자 알림).
// 텔레그램 발송과 무관하게 별도로 동작하며, 실패해도 상담 신청 흐름에는 영향 없음.
async function sendToDashboard({ name, phone, prefType, residence, visitDate, message, funnel }) {
  const dashboardUrl = process.env.DASHBOARD_INTAKE_URL; // 예: https://bunyang-dashboard.vercel.app/api/leads/intake
  const apiKey = process.env.DASHBOARD_API_KEY; // 현장(헤르니티) 전용 API 키

  if (!dashboardUrl || !apiKey) {
    throw new Error('DASHBOARD_INTAKE_URL 또는 DASHBOARD_API_KEY 환경변수가 없습니다.');
  }

  const combinedMessage = visitDate
    ? `[방문희망: ${visitDate}] ${message || ''}`.trim()
    : (message || '');

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);

  try {
    const response = await fetch(dashboardUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
      },
      body: JSON.stringify({
        name,
        phone,
        pyeong_type: prefType,
        region: residence,
        message: combinedMessage,
        utm_source: resolveUtmSource(funnel),
        utm_medium: 'landing_form',
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const body = await response.text().catch(() => '');
      throw new Error(`Dashboard intake failed: ${response.status} ${body}`);
    }
  } finally {
    clearTimeout(timeout);
  }
}

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { name, phone, prefType, residence, visitDate, message, funnel } = req.body || {};

    // 대시보드 전송이 성공하면 대시보드가 자체적으로 텔레그램까지 보내주므로(project.telegram_bot_token
    // 기준), 중복 발송을 피하기 위해 대시보드 실패시에만 아래 직접 발송으로 폴백한다.
    try {
      await sendToDashboard({ name, phone, prefType, residence, visitDate, message, funnel });
      return res.status(200).json({ success: true, via: 'dashboard' });
    } catch (dashboardErr) {
      console.error('Dashboard intake error, falling back to direct Telegram send:', dashboardErr);
    }

    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const rawChatIds = process.env.TELEGRAM_CHAT_ID || process.env.TELEGRAM_CHAT_IDS || '';

    if (!botToken || !rawChatIds) {
      console.error('Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in Vercel environment variables');
      return res.status(500).json({ error: 'Server configuration error: missing Telegram environment variables.' });
    }

    // Support multiple Chat IDs split by comma
    const chatIds = rawChatIds.split(',').map(id => id.trim()).filter(Boolean);

    const messageText = `✨ [남성역 헤르니티 관심고객 등록] ✨
--------------------------------
👤 이름: ${name || '미입력'}
📞 연락처: ${phone || '미입력'}
🏠 관심 평형: ${prefType || '미선택'}
📍 현재 거주지: ${residence || '미입력'}
📅 방문희망일시: ${visitDate || '미입력'}
💬 문의사항: ${message || '없음'}
🔍 인입 경로: ${funnel || '직접'}
--------------------------------
📅 신청일시: ${new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' })}`;

    // Send messages in parallel to all chat IDs
    const results = await Promise.allSettled(
      chatIds.map(async (chatId) => {
        const response = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            chat_id: chatId,
            text: messageText
          })
        });
        const data = await response.json();
        if (!response.ok || !data.ok) {
          throw new Error(`ChatID ${chatId} send failed: ${data.description || 'Unknown error'}`);
        }
        return data;
      })
    );

    const fulfilledCount = results.filter(r => r.status === 'fulfilled').length;
    const rejectedResults = results.filter(r => r.status === 'rejected');

    if (rejectedResults.length > 0) {
      console.warn('Some Telegram messages failed to send:', rejectedResults.map(r => r.reason?.message || r.reason));
    }

    // As long as at least one message was delivered, consider it successful
    if (fulfilledCount > 0) {
      return res.status(200).json({ success: true, deliveredCount: fulfilledCount });
    } else {
      return res.status(500).json({ error: 'Failed to send Telegram message to all recipients.' });
    }
  } catch (error) {
    console.error('Internal Server Error in Telegram API:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

