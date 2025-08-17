import streamlit as st
import yfinance as yf
import pandas as pd # noqa
import plotly.graph_objects as go

def calculate_indicators(df):
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

def plot_indicators(df, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50'))
    fig.update_layout(title=f'{ticker} Price & Moving Averages', xaxis_title='Date', yaxis_title='Price')

    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'))
    fig_rsi.update_layout(title='Relative Strength Index (RSI)', yaxis=dict(range=[0, 100]))

    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD'))
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal'))
    fig_macd.update_layout(title='MACD & Signal Line')

    return fig, fig_rsi, fig_macd

def technical_tab():
    st.header("📈 Technical Indicators")

    # 🔍 Dropdown for Ticker Selection
    popular_tickers = {
        "Apple Inc. (AAPL)": "AAPL",
        "Alphabet Inc. (GOOGL)": "GOOGL",
        "Microsoft Corporation (MSFT)": "MSFT",
        "NVIDIA Corporation (NVDA)": "NVDA",
        "Tesla, Inc. (TSLA)": "TSLA",
        "Amazon.com, Inc. (AMZN)": "AMZN",
        "Meta Platforms, Inc. (META)": "META",
        "Infosys Ltd. (INFY)": "INFY",
        "Reliance Industries Ltd. (RELIANCE)": "RELIANCE",
        "Tata Consultancy Services Ltd. (TCS)": "TCS",
        "HDFC Bank Ltd. (HDFCBANK)": "HDFCBANK"
    }

    selected_label = st.selectbox("Choose a Stock", list(popular_tickers.keys()))
    ticker = popular_tickers[selected_label]

    # 📥 Fetch Data
    data = yf.download(ticker, period="6mo", interval="1d")
    if data.empty:
        st.warning("⚠️ No data available. Try a different ticker or check market status.")
        return

    df = calculate_indicators(data)
    fig_price, fig_rsi, fig_macd = plot_indicators(df, ticker)

    st.plotly_chart(fig_price, use_container_width=True)
    st.plotly_chart(fig_rsi, use_container_width=True)
    st.plotly_chart(fig_macd, use_container_width=True)
