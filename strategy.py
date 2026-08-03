"""
=========================================
HBL AI TRADER PRO v3.0
Trading Strategy
=========================================
"""

class StrategyEngine:

    def analyze(self, row):

        buy_score = 0
        sell_score = 0
        reasons = []

        # EMA Trend
        if row["EMA10"] > row["EMA25"]:
            buy_score += 30
            reasons.append("EMA Bullish")

        elif row["EMA10"] < row["EMA25"]:
            sell_score += 30
            reasons.append("EMA Bearish")

        # RSI
        if row["RSI"] > 55:
            buy_score += 20
            reasons.append("RSI Bullish")

        elif row["RSI"] < 45:
            sell_score += 20
            reasons.append("RSI Bearish")

        # MACD
        if row["MACD"] > row["MACD_SIGNAL"]:
            buy_score += 30
            reasons.append("MACD Bullish")

        else:
            sell_score += 30
            reasons.append("MACD Bearish")

        # ADX
        if row["ADX"] > 25:
            if buy_score > sell_score:
                buy_score += 20
            elif sell_score > buy_score:
                sell_score += 20

            reasons.append("Strong Trend")

        # Final Decision
        if buy_score > sell_score:
            signal = "BUY"
            confidence = min(buy_score, 100)

        elif sell_score > buy_score:
            signal = "SELL"
            confidence = min(sell_score, 100)

        else:
            signal = "WAIT"
            confidence = 50

        return {
            "signal": signal,
            "confidence": confidence,
            "buy_score": buy_score,
            "sell_score": sell_score,
            "reasons": reasons
        }