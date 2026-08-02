"""
=========================================
HBL AI TRADER PRO v2.0
Risk Management Module
=========================================
"""

from config import (
    MAX_TRADES_PER_DAY,
    MAX_DAILY_LOSS,
    RISK_PER_TRADE
)


class RiskManager:

    def __init__(self):

        self.trades_today = 0

        self.daily_loss = 0.0

    def can_trade(self):

        if self.trades_today >= MAX_TRADES_PER_DAY:

            return False, "Maximum daily trades reached."

        if self.daily_loss >= MAX_DAILY_LOSS:

            return False, "Daily loss limit reached."

        return True, "Trading allowed."

    def register_trade(self):

        self.trades_today += 1

    def register_loss(self, loss_percent):

        self.daily_loss += loss_percent

    def get_status(self):

        return {
            "trades_today": self.trades_today,
            "max_trades": MAX_TRADES_PER_DAY,
            "daily_loss": round(self.daily_loss, 2),
            "max_daily_loss": MAX_DAILY_LOSS,
            "risk_per_trade": RISK_PER_TRADE
        }

    def reset_day(self):

        self.trades_today = 0

        self.daily_loss = 0.0