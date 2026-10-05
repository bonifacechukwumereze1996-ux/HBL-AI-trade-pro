
"""
=========================================
HBL AI TRADER PRO v3.0
Persistent Demo Trade Engine
=========================================
"""

import json
import os
from datetime import datetime


class DemoTradeEngine:

    def __init__(self, file_path="demo_state.json"):

        self.file_path = file_path

        self.pending_trades = {}
self.open_trades = {}
self.completed_trades = []
self.last_signal_candles = {}

self.load_state()
    # ---------------------------------------
    # CONVERT DATETIME FOR JSON
    # ---------------------------------------

    def serialize_trade(self, trade):

        saved = trade.copy()

        for key, value in saved.items():
            if isinstance(value, datetime):
                saved[key] = value.isoformat()

        return saved

    # ---------------------------------------
    # RESTORE DATETIME VALUES
    # ---------------------------------------

    def restore_trade(self, trade):

        restored = trade.copy()

        datetime_fields = [
            "created_time",
            "entry_time",
            "exit_time"
        ]

        for key in datetime_fields:
            value = restored.get(key)

            if isinstance(value, str):
                restored[key] = datetime.fromisoformat(value)

        return restored

    # ---------------------------------------
    # SAVE CURRENT STATE
    # ---------------------------------------

    def save_state(self):

        data = {
    "pending_trades": {
        pair: self.serialize_trade(trade)
        for pair, trade in self.pending_trades.items()
    },
    "open_trades": {
        pair: self.serialize_trade(trade)
        for pair, trade in self.open_trades.items()
    },
    "completed_trades": [
        self.serialize_trade(trade)
        for trade in self.completed_trades
    ],
    "last_signal_candles": self.last_signal_candles
} 

        temp_path = self.file_path + ".tmp"

        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        os.replace(temp_path, self.file_path)

    # ---------------------------------------
    # LOAD SAVED STATE
    # ---------------------------------------

    def load_state(self):

        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
self.last_signal_candles = data.get(
    "last_signal_candles", {}
)

            self.pending_trades = {
                pair: self.restore_trade(trade)
                for pair, trade in data.get(
                    "pending_trades", {}
                ).items()
            }

            self.open_trades = {
                pair: self.restore_trade(trade)
                for pair, trade in data.get(
                    "open_trades", {}
                ).items()
            }

            self.completed_trades = [
                self.restore_trade(trade)
                for trade in data.get(
                    "completed_trades", []
                )
            ]

        except (OSError, ValueError, TypeError, KeyError) as error:
            print("Could not load demo state:", error)

    # ---------------------------------------
    # CHECK PENDING TRADE
    # ---------------------------------------

    def has_pending_trade(self, pair):
        return pair in self.pending_trades

    # ---------------------------------------
    # CREATE PENDING DEMO TRADE
    # ---------------------------------------

    def create_pending_trade(
        self,
        pair,
        signal,
        confidence,
        signal_candle,
        timeframe,
        indicators=None
    ):

        if self.has_pending_trade(pair):
            return False

        if self.has_open_trade(pair):
            return False

        if signal not in ["BUY", "SELL"]:
            return False

        trade = {
            "pair": pair,
            "signal": signal,
            "confidence": confidence,
            "signal_candle": signal_candle,
            "created_time": datetime.now(),
            "timeframe": timeframe,
            "indicators": indicators.copy() if indicators else {}
        }

        self.pending_trades[pair] = trade
        self.save_state()

        return True

    # ---------------------------------------
    # CHECK OPEN TRADE
    # ---------------------------------------

    def has_open_trade(self, pair):
        return pair in self.open_trades

    # ---------------------------------------
    # OPEN PENDING TRADE
    # ---------------------------------------

    def open_pending_trade(
        self,
        pair,
        entry_price,
        entry_candle
    ):

        if not self.has_pending_trade(pair):
            return False

        if self.has_open_trade(pair):
            return False

        trade = self.pending_trades[pair]

        if str(entry_candle) == str(trade["signal_candle"]):
            return False

        open_trade = {
            "pair": pair,
            "signal": trade["signal"],
            "confidence": trade["confidence"],
            "entry_price": entry_price,
            "entry_time": datetime.now(),
            "entry_candle": entry_candle,
            "signal_candle": trade["signal_candle"],
            "timeframe": trade["timeframe"],
            "indicators": trade.get("indicators", {})
        }

        self.open_trades[pair] = open_trade
        del self.pending_trades[pair]

        self.save_state()

        return True

    # ---------------------------------------
    # CLOSE DEMO TRADE
    # ---------------------------------------

    def close_trade(self, pair, exit_price):

        if not self.has_open_trade(pair):
            return None

        trade = self.open_trades[pair]

        entry_price = trade["entry_price"]
        signal = trade["signal"]

        if signal == "BUY":

            if exit_price > entry_price:
                result = "WIN"
            elif exit_price < entry_price:
                result = "LOSS"
            else:
                result = "DRAW"

        else:

            if exit_price < entry_price:
                result = "WIN"
            elif exit_price > entry_price:
                result = "LOSS"
            else:
                result = "DRAW"

        if signal == "BUY":
            price_change = exit_price - entry_price
        else:
            price_change = entry_price - exit_price

        completed_trade = {
            "pair": pair,
            "signal": signal,
            "confidence": trade["confidence"],
            "entry_price": entry_price,
            "exit_price": exit_price,
            "entry_time": trade["entry_time"],
            "exit_time": datetime.now(),
            "entry_candle": trade["entry_candle"],
            "signal_candle": trade["signal_candle"],
            "timeframe": trade["timeframe"],
            "result": result,
            "price_change": round(price_change, 5),
            "indicators": trade.get("indicators", {})
        }

        self.completed_trades.append(completed_trade)
        del self.open_trades[pair]

        self.save_state()

        return completed_trade

    # ---------------------------------------
    # GET PENDING TRADES
    # ---------------------------------------

    def get_pending_trades(self):
        return list(self.pending_trades.values())

    # ---------------------------------------
    # GET OPEN TRADES
    # ---------------------------------------

    def get_open_trades(self):
        return list(self.open_trades.values())

    # ---------------------------------------
    # GET COMPLETED TRADES
    # ---------------------------------------

    def get_completed_trades(self):
        return self.completed_trades
    # ---------------------------------------
    # CHECK SIGNAL FOR COMPLETED CANDLE
    # ---------------------------------------

    def has_signal_for_candle(self, pair, candle_id):

        return (
            self.last_signal_candles.get(pair)
            == str(candle_id)
        )

    # ---------------------------------------
    # RECORD SIGNAL CANDLE
    # ---------------------------------------

    def record_signal_candle(self, pair, candle_id):

        self.last_signal_candles[pair] = str(candle_id)

        self.save_state()
