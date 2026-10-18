
"""
=========================================
HBL AI TRADER PRO v3.0
Trade History Module
=========================================
"""

import os
import pandas as pd
from datetime import datetime


class TradeHistory:

    def __init__(self):
        self.file_path = "trade_history.csv"
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
            pd.DataFrame(columns=self.columns).to_csv(
                self.file_path,
                index=False
            )

    def _read_history(self):
        """Read history safely, including an empty CSV."""
        try:
            df = pd.read_csv(self.file_path)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df = pd.DataFrame(columns=self.columns)

        # Ensure all required columns exist.
        for column in self.columns:
            if column not in df.columns:
                df[column] = pd.NA

        return df[self.columns]

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

        df = self._read_history()
        df.loc[len(df)] = row

        # Write to a temporary file before replacing history.
        temp_path = self.file_path + ".tmp"
        df.to_csv(temp_path, index=False)
        os.replace(temp_path, self.file_path)

    def load(self):
        return self._read_history()
