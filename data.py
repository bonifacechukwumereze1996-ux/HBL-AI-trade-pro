"""
HBL AI Trader Pro
Market Data Module
"""

import yfinance as yf


class MarketData:

    def get_data(self, pair, timeframe):

        interval_map = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "1h": "60m"
        }

        period_map = {
            "1m": "1d",
            "5m": "5d",
            "15m": "5d",
            "1h": "1mo"
        }

        try:

            df = yf.download(
                pair,
                interval=interval_map[timeframe],
                period=period_map[timeframe],
                progress=False,
                auto_adjust=False
            )

            if df.empty:
                return None

            # Flatten multi-level columns if needed
            if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(0)

            return df

        except Exception:
            return None