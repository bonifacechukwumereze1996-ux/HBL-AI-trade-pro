"""
HBL AI Trader Pro
Trade History Module
"""

import pandas as pd
import os
from datetime import datetime


class TradeHistory:

    def __init__(self):

        self.file = "trade_history.csv"

        if not os.path.exists(self.file):

            pd.DataFrame(
                columns=[
                    "Date",
                    "Pair",
                    "Signal",
                    "Confidence",
                    "Price",
                    "Timeframe",
                    "Status"
                ]
            ).to_csv(self.file, index=False)

    def save(
        self,
        pair,
        signal,
        confidence,
        price,
        timeframe,
        status
    ):

        row = pd.DataFrame([
            {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Pair": pair,
                "Signal": signal,
                "Confidence": confidence,
                "Price": price,
                "Timeframe": timeframe,
                "Status": status
            }
        ])

        row.to_csv(
            self.file,
            mode="a",
            header=False,
            index=False
        )

    def load(self):

        try:
            return pd.read_csv(self.file)

        except Exception:

            return pd.DataFrame()