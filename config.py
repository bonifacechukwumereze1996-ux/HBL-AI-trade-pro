"""
=========================================
HBL AI TRADER PRO v2.0
Configuration File
=========================================
"""

# -----------------------------
# APP SETTINGS
# -----------------------------
APP_NAME = "HBL AI Trader Pro"
VERSION = "2.0.0"

# -----------------------------
# DEFAULT TRADING SETTINGS
# -----------------------------
DEFAULT_TIMEFRAME = "5m"

DEFAULT_PAIRS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X"
]

AUTO_REFRESH = 30  # seconds

# -----------------------------
# AI SETTINGS
# -----------------------------
AI_CONFIDENCE = 80  # Minimum confidence before a signal

# -----------------------------
# RISK MANAGEMENT
# -----------------------------
MAX_TRADES_PER_DAY = 10

MAX_DAILY_LOSS = 5      # Percent

RISK_PER_TRADE = 1      # Percent

# -----------------------------
# TELEGRAM
# -----------------------------
BOT_TOKEN = ""

CHAT_ID = ""

# -----------------------------
# WHATSAPP
# -----------------------------
WHATSAPP_ENABLED = False

# -----------------------------
# COLORS
# -----------------------------
BUY_COLOR = "#00C853"

SELL_COLOR = "#D50000"

WAIT_COLOR = "#FFD600"