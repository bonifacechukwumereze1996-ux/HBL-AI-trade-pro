"""
HBL AI Trader Pro
Configuration File
"""

APP_NAME = "HBL AI Trader Pro"

VERSION = "3.0"

AUTO_REFRESH = 30

DEFAULT_TIMEFRAME = "5m"

DEFAULT_PAIRS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X",

    "BOOM500",
    "BOOM1000",
    "CRASH500",
    "CRASH1000"
]

# -----------------------------
# TELEGRAM SETTINGS
# -----------------------------

BOT_TOKEN = "YOUR_BOT_TOKEN"

CHAT_ID = "YOUR_CHAT_ID"

# -----------------------------
# RISK SETTINGS
# -----------------------------

MAX_TRADES_PER_DAY = 20

MAX_DAILY_LOSS = 5

MIN_CONFIDENCE = 80