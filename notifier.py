"""
HBL AI Trader Pro
Telegram Notification Module
"""

import requests
from config import BOT_TOKEN, CHAT_ID


class Notifier:

    def send_telegram(self, message):

        if BOT_TOKEN == "YOUR_BOT_TOKEN" or CHAT_ID == "YOUR_CHAT_ID":
            return

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        try:
            requests.post(url, data=data, timeout=10)
        except Exception:
            pass

    def signal_message(
        self,
        pair,
        signal,
        confidence,
        price,
        timeframe,
        reasons
    ):

        reason_text = "\n".join([f"• {r}" for r in reasons])

        return f"""🚨 HBL AI TRADER PRO 🚨

Pair: {pair}

Signal: {signal}

Confidence: {confidence}%

Price: {price}

Timeframe: {timeframe}

Reasons:
{reason_text}

Trade Carefully.
Educational Purposes Only.
"""