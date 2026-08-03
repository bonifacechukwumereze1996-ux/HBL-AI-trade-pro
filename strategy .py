"""
HBL AI Trader Pro
Trading Strategy Engine
"""


class StrategyEngine:

    def analyze(self, row):

        buy_score = 0
        sell_score = 0
        reasons = []

        # EMA Trend
        if row["EMA10"] > row["EMA25"]:
            buy_score += 1
            reasons.append("EMA Bullish")
        else:
            sell_score += 1
            reasons.append("EMA Bearish")

        # RSI
        if row["RSI"] > 55:
            buy_score += 1
            reasons.append("RSI Bullish")
        elif row["RSI"] < 45:
            sell_score += 1
            reasons.append("RSI Bearish")
        else:
            reasons.append("RSI Neutral")

        # MACD
        if row["MACD"] > row["MACD_SIGNAL"]:
            buy_score += 1
            reasons.append("MACD Bullish")
        else:
            sell_score += 1
            reasons.append("MACD Bearish")

        # ADX Trend Strength
        strong_trend = row["ADX"] >= 25

        return {
            "buy_score": buy_score,
            "sell_score": sell_score,
            "strong_trend": strong_trend,
            "adx": round(float(row["ADX"]), 2),
            "reasons": reasons
        }