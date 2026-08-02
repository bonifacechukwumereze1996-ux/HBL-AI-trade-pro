"""
=========================================
HBL AI TRADER PRO v2.0
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
    AUTO_REFRESH
)

from data import MarketData
from indicators import IndicatorEngine
from strategy import StrategyEngine
from ai_engine import AIEngine
from notifier import Notifier
from history import TradeHistory
from risk import RiskManager

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# AUTO REFRESH
# ---------------------------------------------------

st_autorefresh(
    interval=AUTO_REFRESH * 1000,
    key="refresh"
)

# ---------------------------------------------------
# INITIALIZE CLASSES
# ---------------------------------------------------

market = MarketData()

indicator = IndicatorEngine()

strategy = StrategyEngine()

ai = AIEngine()

notify = Notifier()

history = TradeHistory()

risk = RiskManager()

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🤖 HBL AI Trader Pro")

st.caption(f"Version {VERSION}")

st.info(
    "Educational Use Only | "
    "AI Signal Dashboard | "
    "Trade Responsibly"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

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
        "AUDJPY=X"
    ],

    default=DEFAULT_PAIRS
)

timeframe = st.sidebar.selectbox(

    "Timeframe",

    ["1m", "5m", "15m", "1h"],

    index=["1m", "5m", "15m", "1h"].index(DEFAULT_TIMEFRAME)

)

st.sidebar.markdown("---")

st.sidebar.success("✅ AI Engine Ready")

st.sidebar.success("✅ Strategy Ready")

st.sidebar.success("✅ Market Data Ready")

st.sidebar.success("✅ Notification Ready")

st.sidebar.success("✅ Risk Manager Ready")

# ---------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Pairs",
    len(pairs)
)

col2.metric(
    "Timeframe",
    timeframe
)

status = risk.get_status()

col3.metric(
    "Trades Today",
    status["trades_today"]
)

col4.metric(
    "Daily Loss %",
    status["daily_loss"]
)

st.divider()

# ---------------------------------------------------
# MAIN CONTAINER
# ---------------------------------------------------

results = []

history_df = history.load()
# ---------------------------------------------------
# ANALYZE EACH PAIR
# ---------------------------------------------------

for pair in pairs:

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
        continue

    # Latest Candle
    last = df.iloc[-1]

    # Strategy Analysis
    analysis = strategy.analyze(last)

    # AI Evaluation
    decision = ai.evaluate(analysis)

    # Current Price
    price = round(float(last["Close"]), 5)

    # Save Result
    results.append({

        "Pair": pair,

        "Signal": decision["signal"],

        "Confidence": decision["confidence"],

        "Status": decision["status"],

        "Price": price

    })
      if "last_signal" not in st.session_state:
        st.session_state.last_signal = {}

    # ---------------------------------------
    # TELEGRAM ALERT
    # ---------------------------------------

    if decision["approved"]:

        previous_signal = st.session_state.last_signal.get(pair)

        if previous_signal != decision["signal"]:

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

            st.session_state.last_signal[pair] = decision["signal"] ---------------------------------------------------
# RESULTS DATAFRAME
# ---------------------------------------------------

results_df = pd.DataFrame(results)
# ---------------------------------------------------
# DISPLAY SIGNAL TABLE
# ---------------------------------------------------

st.subheader("📊 Live AI Trading Signals")

if len(results_df) == 0:

    st.warning("No market data available.")

else:

    def highlight_signal(row):

        signal = row["Signal"]

        if signal == "BUY":
            return ["background-color:#00C853;color:white"] * len(row)

        elif signal == "SELL":
            return ["background-color:#D50000;color:white"] * len(row)

        elif signal == "WAIT":
            return ["background-color:#FFD600;color:black"] * len(row)

        return [""] * len(row)

    st.dataframe(
        results_df.style.apply(highlight_signal, axis=1),
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

st.divider()

st.subheader("📈 Live Market Charts")

for pair in pairs:

    df = market.get_data(pair, timeframe)

    if df is None:
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
            name="Candles"
        )

        fig.add_scatter(
            x=df.index,
            y=df["EMA_10"],
            name="EMA 10"
        )

        fig.add_scatter(
            x=df.index,
            y=df["EMA_20"],
            name="EMA 20"
        )

        fig.add_scatter(
            x=df.index,
            y=df["EMA_50"],
            name="EMA 50"
        )

        fig.update_layout(

            height=500,

            xaxis_rangeslider_visible=False,

            template="plotly_dark"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        # ---------------------------------------------------
# TRADE HISTORY
# ---------------------------------------------------

st.divider()

st.subheader("📜 Trade History")

try:

    history_data = history.load()

    if history_data.empty:

        st.info("No trade history available yet.")

    else:

        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:

    st.warning(f"History Error: {e}")

# ---------------------------------------------------
# RISK MANAGEMENT
# ---------------------------------------------------

st.divider()

st.subheader("🛡 Risk Management")

risk_status = risk.get_status()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Trades Today",
    risk_status["trades_today"]
)

col2.metric(
    "Daily Loss %",
    risk_status["daily_loss"]
)

col3.metric(
    "Risk / Trade",
    f'{risk_status["risk_per_trade"]}%'
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "🤖 HBL AI Trader Pro v2.0 | "
    "Built with Streamlit | "
    "Educational Use Only"
)