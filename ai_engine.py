"""
=========================================
HBL AI TRADER PRO v2.0
AI Decision Engine
=========================================
"""

from config import AI_CONFIDENCE


class AIEngine:

    def evaluate(self, analysis):

        confidence = analysis["confidence"]
        signal = analysis["signal"]

        if signal == "WAIT":
            return {
                "approved": False,
                "signal": "WAIT",
                "confidence": confidence,
                "status": "No Trade",
                "reasons": analysis["reasons"]
            }

        if confidence >= AI_CONFIDENCE:

            return {
                "approved": True,
                "signal": signal,
                "confidence": confidence,
                "status": "APPROVED",
                "reasons": analysis["reasons"]
            }

        return {
            "approved": False,
            "signal": signal,
            "confidence": confidence,
            "status": "LOW CONFIDENCE",
            "reasons": analysis["reasons"]
        }