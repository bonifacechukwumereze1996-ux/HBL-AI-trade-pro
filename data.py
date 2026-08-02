"""
=========================================
HBL AI TRADER PRO v2.0
Market Data Module
=========================================
"""

import yfinance as yf
import pandas as pd


class MarketData:

    def __init__(self):
        self.period_map = {
            "1m": "1d",
            "5m": "5d",
            "15m": "7d",
            "1h": "30d"
        }

        self.interval_map = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "1h": "60m"
        }

    def get_data(self, pair, timeframe):

        symbol = pair.replace(" OTC", "=X")

        try:

            df = yf.download(
                symbol,
                interval=self.interval_map[timeframe],
                period=self.period_map[timeframe],
                progress=False,
                auto_adjust=False
            )

            if df.empty:
                return None

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            required = ["Open", "High", "Low", "Close", "Volume"]

            for col in required:
                if col not in df.columns:
                    return None

            df = df.dropna()

            return df

        except Exception as e:

            print("Market Data Error:", e)

            return None