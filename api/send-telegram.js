export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { name, phone, prefType, residence, visitDate, message, funnel } = req.body || {};

    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;

    if (!botToken || !chatId) {
      console.error('Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in Vercel environment variables');
      return res.status(500).json({ error: 'Server configuration error: missing Telegram environment variables.' });
    }

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
      console.error('Telegram API error:', data);
      return res.status(500).json({ error: data.description || 'Telegram API request failed' });
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Internal Server Error in Telegram API:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
