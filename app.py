"""
=========================================
HBL AI Trader Pro v3.0
Main Application
=========================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

from config import (
    APP_NAME,
    VERSION,
    DEFAULT_PAIRS,
    DEFAULT_TIMEFRAME,
    AUTO_REFRESH,
)

from data import MarketData
from indicators import IndicatorEngine
from strategy import StrategyEngine
from ai_engine import AIEngine
from notifier import Notifier
from history import TradeHistory
from risk import RiskManager

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------
# AUTO REFRESH
# ---------------------------------------

st_autorefresh(
    interval=AUTO_REFRESH * 1000,
    key="refresh"
)

# ---------------------------------------
# SESSION STATE
# ---------------------------------------

if "last_signal" not in st.session_state:
    st.session_state.last_signal = {}

# ---------------------------------------
# INITIALIZE MODULES
# ---------------------------------------

market = MarketData()
indicator = IndicatorEngine()
strategy = StrategyEngine()
ai = AIEngine()
notify = Notifier()
history = TradeHistory()
risk = RiskManager()

# ---------------------------------------
# HEADER
# ---------------------------------------

st.title("🤖 HBL AI Trader Pro")
st.caption(f"Version {VERSION}")

st.info(
    "AI Powered Trading Dashboard | "
    "Educational Use Only | "
    "Trade Responsibly"
)

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

st.sidebar.title("⚙ Settings")

pairs = st.sidebar.multiselect(
    "Trading Pairs",
    [
        "EURUSD=X",
        "GBPUSD=X",
        "USDJPY=X",
        "AUDUSD=X",
        "USDCAD=X",
        "USDCHF=X",
        "NZDUSD=X",
        "EURJPY=X",
        "GBPJPY=X",
        "AUDJPY=X",
    ],
    default=DEFAULT_PAIRS
)

timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["1m", "5m", "15m", "1h"],
    index=["1m", "5m", "15m", "1h"].index(DEFAULT_TIMEFRAME)
)

st.sidebar.markdown("---")

status = risk.get_status()

st.sidebar.success("✅ AI Engine Ready")
st.sidebar.success("✅ Market Data Ready")
st.sidebar.success("✅ Strategy Ready")
st.sidebar.success("✅ Telegram Ready")

# ---------------------------------------
# DASHBOARD METRICS
# ---------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Pairs", len(pairs))
col2.metric("Timeframe", timeframe)
col3.metric("Trades Today", status["trades_today"])
col4.metric("Daily Loss %", status["daily_loss"])

st.divider()

# ---------------------------------------
# PREPARE RESULTS
# ---------------------------------------

results = []
