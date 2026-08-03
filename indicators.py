"""
HBL AI Trader Pro
Technical Indicators
"""

import ta


class IndicatorEngine:

    def calculate(self, df):

        close = df["Close"]
        high = df["High"]
        low = df["Low"]

        # EMA
        df["EMA10"] = ta.trend.EMAIndicator(
            close=close,
            window=10
        ).ema_indicator()

        df["EMA25"] = ta.trend.EMAIndicator(
            close=close,
            window=25
        ).ema_indicator()

        # RSI
        df["RSI"] = ta.momentum.RSIIndicator(
            close=close,
            window=14
        ).rsi()

        # MACD
        macd = ta.trend.MACD(close)

        df["MACD"] = macd.macd()
        df["MACD_SIGNAL"] = macd.macd_signal()

        # ADX
        df["ADX"] = ta.trend.ADXIndicator(
            high=high,
            low=low,
            close=close,
            window=14
        ).adx()

        df.dropna(inplace=True)

        return df