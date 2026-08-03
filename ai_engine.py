"""
HBL AI Trader Pro
AI Decision Engine
"""

from config import MIN_CONFIDENCE


class AIEngine:

    def evaluate(self, analysis):

        buy = analysis["buy_score"]
        sell = analysis["sell_score"]

        signal = "WAIT"
        confidence = 50
        approved = False
        status = "No Trade"

        total = buy + sell

        if total > 0:
            confidence = int((max(buy, sell) / total) * 100)

        # BUY Decision
        if buy >= 3 and analysis["strong_trend"]:
            signal = "BUY"
            status = "Approved"

        # SELL Decision
        elif sell >= 3 and analysis["strong_trend"]:
            signal = "SELL"
            status = "Approved"

        # Confidence Check
        if confidence >= MIN_CONFIDENCE and signal != "WAIT":
            approved = True
        else:
            approved = False
            if signal != "WAIT":
                status = "Low Confidence"

        return {
            "signal": signal,
            "confidence": confidence,
            "approved": approved,
            "status": status,
            "reasons": analysis["reasons"]
        }