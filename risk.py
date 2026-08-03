"""
HBL AI Trader Pro
Risk Management Module
"""

from config import MAX_TRADES_PER_DAY, MAX_DAILY_LOSS


class RiskManager:

    def __init__(self):

        self.trades_today = 0
        self.daily_loss = 0.0

    def register_trade(self):

        self.trades_today += 1

    def add_loss(self, percent):

        self.daily_loss += percent

    def can_trade(self):

        if self.trades_today >= MAX_TRADES_PER_DAY:
            return False

        if self.daily_loss >= MAX_DAILY_LOSS:
            return False

        return True

    def get_status(self):

        return {
            "trades_today": self.trades_today,
            "daily_loss": round(self.daily_loss, 2),
            "allowed": self.can_trade()
        }