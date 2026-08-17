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
from deriv_data import DerivMarketData
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
deriv = DerivMarketData()
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
        "BOOM500",
        "BOOM1000",
        "CRASH500",
        "CRASH1000",
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
# ---------------------------------------
# ANALYZE EACH PAIR
# ---------------------------------------

for pair in pairs:

    if pair.startswith("BOOM") or pair.startswith("CRASH"):
        df = deriv.get_data(pair, timeframe)
    else:
        df = market.get_data(pair, timeframe)
    if df is None:

        results.append({
            "Pair": pair,
            "Signal": "NO DATA",
            "Confidence": 0,
            "Status": "Unavailable",
            "Price": "-"
        })

        continue

    # Calculate Indicators
    df = indicator.calculate(df)

    if df.empty:

        results.append({
            "Pair": pair,
            "Signal": "NO DATA",
            "Confidence": 0,
            "Status": "Indicator Error",
            "Price": "-"
        })

        continue

    # Latest candle
    last = df.iloc[-1]

    # Strategy Analysis
    analysis = strategy.analyze(last)

    # AI Decision
    decision = ai.evaluate(analysis)

    # Current Price
    price = round(float(last["Close"]), 5)

    # Save Result
    results.append({
        "Pair": pair,
        "Signal": decision["signal"],
        "Confidence": f'{decision["confidence"]}%',
        "Status": decision["status"],
        "Price": price
    })

    # Telegram Alert
    if decision["approved"]:

        previous = st.session_state.last_signal.get(pair)

        if previous != decision["signal"]:

            message = notify.signal_message(
                pair=pair,
                signal=decision["signal"],
                confidence=decision["confidence"],
                price=price,
                timeframe=timeframe,
                reasons=decision["reasons"]
            )

            notify.send_telegram(message)

            history.save(
                pair=pair,
                signal=decision["signal"],
                confidence=decision["confidence"],
                price=price,
                timeframe=timeframe,
                status=decision["status"]
            )

            risk.register_trade()

            st.session_state.last_signal[pair] = decision["signal"]
# ---------------------------------------
# RESULTS DATAFRAME
# ---------------------------------------

results_df = pd.DataFrame(results)

# ---------------------------------------
# SIGNAL TABLE
# ---------------------------------------

st.subheader("📊 Live AI Trading Signals")

if results_df.empty:

    st.warning("No market data available.")

else:

    def highlight_signal(row):

        if row["Signal"] == "BUY":
            return ["background-color:#00C853;color:white"] * len(row)

        elif row["Signal"] == "SELL":
            return ["background-color:#D50000;color:white"] * len(row)

        elif row["Signal"] == "WAIT":
            return ["background-color:#FFD600;color:black"] * len(row)

        return [""] * len(row)

    st.dataframe(
        results_df.style.apply(highlight_signal, axis=1),
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------
# TRADE HISTORY
# ---------------------------------------

st.subheader("📜 Trade History")

history_df = history.load()

if history_df.empty:

    st.info("No trades recorded yet.")

else:

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )
# ---------------------------------------
# LIVE CHARTS
# ---------------------------------------

st.subheader("📈 Live Market Charts")

for pair in pairs:

    df = market.get_data(pair, timeframe)

    if df is None or df.empty:
        continue

    df = indicator.calculate(df)

    if df.empty:
        continue

    with st.expander(f"📊 {pair}"):

        fig = go.Figure()

        fig.add_candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=pair
        )

        fig.add_scatter(
            x=df.index,
            y=df["EMA10"],
            name="EMA 10"
        )

        fig.add_scatter(
            x=df.index,
            y=df["EMA25"],
            name="EMA 25"
        )

        fig.update_layout(
            height=500,
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ---------------------------------------
# FOOTER
# ---------------------------------------

st.divider()

st.caption(
    f"{APP_NAME} v{VERSION} | "
    "Educational Purposes Only | "
    "Powered by Python, Streamlit & Yahoo Finance"
)

