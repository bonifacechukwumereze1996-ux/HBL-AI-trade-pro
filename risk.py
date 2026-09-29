"""
HBL AI Trader Pro
Risk Management Module
"""

from datetime import datetime

from config import MAX_TRADES_PER_DAY, MAX_DAILY_LOSS


class RiskManager:

    def __init__(self):

        self.current_date = datetime.now().date()

        self.trades_today = 0

        self.daily_loss = 0.0


    def reset_if_new_day(self):

        today = datetime.now().date()

        if today != self.current_date:

            self.current_date = today

            self.trades_today = 0

            self.daily_loss = 0.0


    def register_trade(self):

        self.reset_if_new_day()

        self.trades_today += 1


    def add_loss(self, percent):

        self.reset_if_new_day()

        self.daily_loss += percent


    def can_trade(self):

        self.reset_if_new_day()

        if self.trades_today >= MAX_TRADES_PER_DAY:

            return False

        if self.daily_loss >= MAX_DAILY_LOSS:

            return False

        return True


    def get_status(self):

        self.reset_if_new_day()

        return {

            "trades_today": self.trades_today,

            "daily_loss": round(
                self.daily_loss,
                2
            ),

            "allowed": self.can_trade()

        }