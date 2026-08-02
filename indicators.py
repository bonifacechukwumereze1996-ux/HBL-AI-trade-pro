"""
=========================================
HBL AI TRADER PRO v2.0
Technical Indicators Module
=========================================
"""

import ta


class IndicatorEngine:

    def calculate(self, df):

        # EMA
        df["EMA_10"] = ta.trend.EMAIndicator(
            close=df["Close"],
            window=10
        ).ema_indicator()

        df["EMA_20"] = ta.trend.EMAIndicator(
            close=df["Close"],
            window=20
        ).ema_indicator()

        df["EMA_50"] = ta.trend.EMAIndicator(
            close=df["Close"],
            window=50
        ).ema_indicator()

        # RSI
        df["RSI"] = ta.momentum.RSIIndicator(
            close=df["Close"],
            window=14
        ).rsi()

        # MACD
        macd = ta.trend.MACD(close=df["Close"])

        df["MACD"] = macd.macd()

        df["MACD_SIGNAL"] = macd.macd_signal()

        # ADX
        adx = ta.trend.ADXIndicator(
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )

        df["ADX"] = adx.adx()

        # ATR
        atr = ta.volatility.AverageTrueRange(
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )

        df["ATR"] = atr.average_true_range()

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(
            close=df["Close"]
        )

        df["BB_UPPER"] = bb.bollinger_hband()

        df["BB_MIDDLE"] = bb.bollinger_mavg()

        df["BB_LOWER"] = bb.bollinger_lband()

        df.dropna(inplace=True)

        return df