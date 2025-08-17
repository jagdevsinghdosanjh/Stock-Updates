import streamlit as st
import yfinance as yf
import pandas as pd # noqa
import plotly.graph_objects as go

def calculate_indicators(df):
    # Moving Averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

def plot_indicators(df, ticker):
    fig = go.Figure()

    # Price + Moving Averages
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50'))

    fig.update_layout(title=f'{ticker} Price & Moving Averages', xaxis_title='Date', yaxis_title='Price')

    # RSI
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'))
    fig_rsi.update_layout(title='Relative Strength Index (RSI)', yaxis=dict(range=[0, 100]))

    # MACD
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD'))
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal'))
    fig_macd.update_layout(title='MACD & Signal Line')

    return fig, fig_rsi, fig_macd

# Streamlit Tab
def technical_tab():
    st.header("📈 Technical Indicators")
    ticker = st.text_input("Enter Stock Ticker", value="AAPL")
    data = yf.download(ticker, period="6mo", interval="1d")
    df = calculate_indicators(data)

    fig_price, fig_rsi, fig_macd = plot_indicators(df, ticker)

    st.plotly_chart(fig_price, use_container_width=True)
    st.plotly_chart(fig_rsi, use_container_width=True)
    st.plotly_chart(fig_macd, use_container_width=True)

# In your main app:
# with st.tabs(["Overview", "Symbolic Dashboard", "Technical Indicators"]) as tabs:
#     with tabs[2]:
#         technical_tab()
