import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

def show_intraday_tab():
    st.header("📈 Intraday Stock Tracker")
    st.caption(f"📅 {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}")

    st.sidebar.header("🔍 Select a Stock")
    popular_tickers = {
         "Apple Inc. (AAPL)": "AAPL",
    "Alphabet Inc. (GOOGL)": "GOOGL",
    "Microsoft Corporation (MSFT)": "MSFT",
    "NVIDIA Corporation (NVDA)": "NVDA",
    "Tesla, Inc. (TSLA)": "TSLA",
    "Infosys Ltd. (INFY)": "INFY",
    "Amazon.com, Inc. (AMZN)": "AMZN",
    "Meta Platforms, Inc. (META)": "META",
    "Intel Corporation (INTC)": "INTC",
    "Advanced Micro Devices, Inc. (AMD)": "AMD",
    "Oracle Corporation (ORCL)": "ORCL",
    "Cisco Systems, Inc. (CSCO)": "CSCO",
    "IBM Corporation (IBM)": "IBM",
    "Reliance Industries Ltd. (RELIANCE)": "RELIANCE",
    "Tata Consultancy Services Ltd. (TCS)": "TCS",
    "HCL Technologies Ltd. (HCLTECH)": "HCLTECH",
    "Wipro Ltd. (WIPRO)": "WIPRO",
    "Bharti Airtel Ltd. (BHARTIARTL)": "BHARTIARTL",
    "ICICI Bank Ltd. (ICICIBANK)": "ICICIBANK",
    "HDFC Bank Ltd. (HDFCBANK)": "HDFCBANK"
    }

    selected_label = st.sidebar.selectbox("Choose a Ticker", list(popular_tickers.keys()))
    ticker = popular_tickers[selected_label]
    interval = st.sidebar.selectbox("Interval", ["1m", "5m", "15m", "30m", "60m"])
    range = st.sidebar.selectbox("Range", ["1d", "5d", "1wk"])

    @st.cache_data(ttl=60)
    def fetch_intraday_data(ticker, interval, range):
        stock = yf.Ticker(ticker)
        df = stock.history(interval=interval, period=range)
        df = df.reset_index()

        if "Datetime" in df.columns:
            df["Datetime"] = pd.to_datetime(df["Datetime"])
        elif "Date" in df.columns:
            df.rename(columns={"Date": "Datetime"}, inplace=True)
            df["Datetime"] = pd.to_datetime(df["Datetime"])
        else:
            df["Datetime"] = pd.to_datetime(df.index)

        return df

    df = fetch_intraday_data(ticker, interval, range)

    if not df.empty:
        st.subheader(f"📊 Intraday Data for `{ticker}`")
        st.dataframe(df[["Datetime", "Open", "High", "Low", "Close", "Volume"]], use_container_width=True)
        st.subheader("📈 Price Movement")
        st.line_chart(df.set_index("Datetime")[["Open", "Close", "High", "Low"]])
        st.subheader("📦 Volume Trend")
        st.bar_chart(df.set_index("Datetime")["Volume"])
    else:
        st.warning("No data available. Try a different ticker or time range.")
