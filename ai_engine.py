"""
HBL AI Trader Pro
AI Decision Engine
"""

from config import MIN_CONFIDENCE


class AIEngine:

    def evaluate(self, analysis):

        buy = analysis["buy_score"]
        sell = analysis["sell_score"]

        signal = analysis["signal"]
        confidence = analysis["confidence"]

        approved = False
        status = "No Trade"

        if signal != "WAIT":

            if confidence >= MIN_CONFIDENCE:
                approved = True
                status = "Approved"
            else:
                approved = False
                status = "Low Confidence"

        return {
            "signal": signal,
            "confidence": confidence,
            "approved": approved,
            "status": status,
            "reasons": analysis["reasons"]
        }