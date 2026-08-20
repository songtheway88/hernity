export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { name, phone, prefType, residence, visitDate, message, funnel } = req.body || {};

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

