"""
=========================================
HBL AI TRADER PRO v3.0
Demo Trade Engine
=========================================
"""

from datetime import datetime


class DemoTradeEngine:

    def __init__(self):

        self.pending_trades = {}

        self.open_trades = {}

        self.completed_trades = []

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
        timeframe
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
            "timeframe": timeframe
        }

        self.pending_trades[pair] = trade

        return True

    # ---------------------------------------
    # CHECK OPEN TRADE
    # ---------------------------------------

    def has_open_trade(self, pair):

        return pair in self.open_trades

    # ---------------------------------------
    # OPEN PENDING TRADE
    # ON NEXT CANDLE
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

        if str(entry_candle) == str(
            trade["signal_candle"]
        ):
            return False

        open_trade = {
            "pair": pair,
            "signal": trade["signal"],
            "confidence": trade["confidence"],
            "entry_price": entry_price,
            "entry_time": datetime.now(),
            "entry_candle": entry_candle,
            "signal_candle": trade["signal_candle"],
            "timeframe": trade["timeframe"]
        }

        self.open_trades[pair] = open_trade

        del self.pending_trades[pair]

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

        # ---------------------------------------
        # DETERMINE RESULT
        # ---------------------------------------

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

        # ---------------------------------------
        # CALCULATE PRICE MOVEMENT
        # ---------------------------------------

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
            "price_change": round(
                price_change,
                5
            )
        }

        self.completed_trades.append(
            completed_trade
        )

        del self.open_trades[pair]

        return completed_trade

    # ---------------------------------------
    # GET PENDING TRADES
    # ---------------------------------------

    def get_pending_trades(self):

        return list(
            self.pending_trades.values()
        )

    # ---------------------------------------
    # GET OPEN TRADES
    # ---------------------------------------

    def get_open_trades(self):

        return list(
            self.open_trades.values()
        )

    # ---------------------------------------
    # GET COMPLETED TRADES
    # ---------------------------------------

    def get_completed_trades(self):

        return self.completed_trades