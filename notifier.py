"""
=========================================
HBL AI TRADER PRO v2.0
Notification Module
=========================================
"""

import requests

from config import BOT_TOKEN, CHAT_ID


class Notifier:

    def send_telegram(self, message):

        if BOT_TOKEN == "" or CHAT_ID == "":
            return False

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }

        try:

            response = requests.post(
                url,
                data=data,
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:

            print("Telegram Error:", e)

            return False

    def signal_message(
        self,
        pair,
        signal,
        confidence,
        price,
        timeframe,
        reasons
    ):

        reason_text = "\n".join(
            [f"• {r}" for r in reasons]
        )

        return f"""
🤖 HBL AI TRADER PRO

📈 Pair: {pair}

🎯 Signal: {signal}

🧠 Confidence: {confidence}%

💰 Price: {price}

⏰ Timeframe: {timeframe}

📊 Reasons:
{reason_text}

⚠️ Educational use only.
Trade responsibly.
"""