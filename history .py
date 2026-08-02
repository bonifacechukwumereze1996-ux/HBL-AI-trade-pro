"""
=========================================
HBL AI TRADER PRO v2.0
Trade History Module
=========================================
"""

import os
import pandas as pd
from datetime import datetime


class TradeHistory:

    def __init__(self):

        self.file_path = "data/trade_history.csv"

        self.columns = [
            "Date",
            "Time",
            "Pair",
            "Signal",
            "Confidence",
            "Price",
            "Timeframe",
            "Status"
        ]

        self.create_file()

    def create_file(self):

        if not os.path.exists(self.file_path):

            df = pd.DataFrame(columns=self.columns)

            df.to_csv(
                self.file_path,
                index=False
            )

    def save(
        self,
        pair,
        signal,
        confidence,
        price,
        timeframe,
        status
    ):

        now = datetime.now()

        row = {
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%H:%M:%S"),
            "Pair": pair,
            "Signal": signal,
            "Confidence": confidence,
            "Price": price,
            "Timeframe": timeframe,
            "Status": status
        }

        df = pd.read_csv(self.file_path)

        df.loc[len(df)] = row

        df.to_csv(
            self.file_path,
            index=False
        )

    def load(self):

        return pd.read_csv(self.file_path)