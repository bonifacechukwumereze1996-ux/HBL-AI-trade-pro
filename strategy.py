"""
=========================================
HBL AI TRADER PRO v2.0
Trading Strategy
=========================================
"""


class StrategyEngine:

    def analyze(self, row):

        buy_score = 0
        sell_score = 0

        reasons = []

        # -------------------------
        # EMA TREND
        # -------------------------
        if row["EMA_10"] > row["EMA_20"] > row["EMA_50"]:
            buy_score += 25
            reasons.append("EMA bullish trend")

        elif row["EMA_10"] < row["EMA_20"] < row["EMA_50"]:
            sell_score += 25
            reasons.append("EMA bearish trend")

        # -------------------------
        # RSI
        # -------------------------
        if row["RSI"] > 55:
            buy_score += 20
            reasons.append("RSI bullish")

        elif row["RSI"] < 45:
            sell_score += 20
            reasons.append("RSI bearish")

        # -------------------------
        # MACD
        # -------------------------
        if row["MACD"] > row["MACD_SIGNAL"]:
            buy_score += 25
            reasons.append("MACD bullish")

        else:
            sell_score += 25
            reasons.append("MACD bearish")

        # -------------------------
        # ADX
        # -------------------------
        if row["ADX"] > 25:

            if buy_score > sell_score:
                buy_score += 15

            elif sell_score > buy_score:
                sell_score += 15

            reasons.append("Strong trend")

        # -------------------------
        # PRICE vs EMA50
        # -------------------------
        if row["Close"] > row["EMA_50"]:
            buy_score += 15

        else:
            sell_score += 15

        # -------------------------
        # FINAL SIGNAL
        # -------------------------
        if buy_score > sell_score:
            signal = "BUY"
            confidence = buy_score

        elif sell_score > buy_score:
            signal = "SELL"
            confidence = sell_score

        else:
            signal = "WAIT"
            confidence = 50

        confidence = min(confidence, 100)

        return {
            "signal": signal,
            "confidence": confidence,
            "buy_score": buy_score,
            "sell_score": sell_score,
            "reasons": reasons
        }