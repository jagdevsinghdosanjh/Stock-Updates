import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np # noqa

def validate_ticker(ticker):
    import yfinance as yf
    df = yf.Ticker(ticker).history(period="5d")
    if df.empty:
        st.error(f"❌ No data found for ticker '{ticker}'. Please check the symbol.")
        return None
    return df

def show_features_tab():
    st.header("🛠 Trading Features")
    st.markdown("""
    Here are some features you can explore:
    - 🔔 Price Alerts
    - 📊 Technical Indicators (RSI, MACD, Moving Averages)
    - 📦 Volume Spike Detection
    - 🧠 AI-based Trade Suggestions (coming soon!)
    """)
    st.info("Want a new feature? Just ask!")
    

# 📉 Add Moving Averages
def add_moving_averages(df, windows=[20, 50, 100]):
    for window in windows:
        df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()
    return df

# 📊 RSI Indicator
def calculate_rsi(df, period=14):
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

# 📊 MACD Indicator
def calculate_macd(df):
    short_ema = df["Close"].ewm(span=12, adjust=False).mean()
    long_ema = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = short_ema - long_ema
    df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()
    return df

# 📦 Volume Spike Detection
def detect_volume_spikes(df, threshold=2.0):
    avg_volume = df["Volume"].mean()
    df["Volume_Spike"] = df["Volume"] > (threshold * avg_volume)
    spikes = df[df["Volume_Spike"]]
    st.subheader("📦 Volume Spikes")
    st.write(spikes[["date", "Volume"]])
    return df

# 🔔 Price Alerts
def show_price_alert(df):
    st.subheader("🔔 Price Alert")
    latest_price = df["Close"].iloc[-1]
    alert_price = st.number_input("Set Alert Price", value=float(latest_price))
    if latest_price >= alert_price:
        st.success(f"✅ Alert! Latest price ({latest_price}) has crossed your threshold.")
    else:
        st.info(f"ℹ️ Latest price is {latest_price}. Waiting to cross {alert_price}.")

# 🧠 AI-based Trade Suggestions (Placeholder)
def show_trade_suggestions(df):
    st.subheader("🧠 AI Trade Suggestions")
    st.info("🚧 This feature is coming soon! Stay tuned for intelligent trade ideas based on market patterns.")

# 📦 Volume Chart
def show_volume_chart(df):
    st.subheader("📦 Volume Over Time")
    st.bar_chart(df.set_index("date")["Volume"])

# 📌 Key Statistics
def show_key_statistics(df):
    st.subheader("📌 Key Statistics")
    stats = {
        "Highest Close": df["Close"].max(),
        "Lowest Close": df["Close"].min(),
        "Average Volume": int(df["Volume"].mean()),
        "Total Trades": int(df["Trades"].sum())
    }
    st.write(pd.DataFrame(stats.items(), columns=["Metric", "Value"]))

# 📅 Date Range Filter
def filter_by_date(df):
    st.subheader("📅 Filter by Date Range")
    start = st.date_input("Start Date", df["date"].min())
    end = st.date_input("End Date", df["date"].max())
    filtered_df = df[(df["date"] >= start) & (df["date"] <= end)]
    return filtered_df

# 🕯️ Candlestick Chart
def show_candlestick_chart(df):
    st.subheader("🕯️ Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(
        x=df["date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])
    st.plotly_chart(fig, use_container_width=True)

# 📥 Export CSV
def export_csv(df, ticker):
    st.download_button(
        label="📥 Download Data as CSV",
        data=df.to_csv(index=False),
        file_name=f"{ticker}_stock_data.csv",
        mime="text/csv"
    )

# if __name__ == "__main__":
#     import yfinance as yf

#     st.title("📈 Stock Feature Demo")

#     ticker = st.text_input("Enter Ticker Symbol", "AAPL")
#     if ticker:
#         df = yf.Ticker(ticker).history(period="3mo")
#         if df.empty:
#             st.error("No data found. Please check the ticker.")
#         else:
#             df.reset_index(inplace=True)
#             df.rename(columns={"Date": "date"}, inplace=True)

#             # Apply features
#             df = add_moving_averages(df)
#             df = calculate_rsi(df)
#             df = calculate_macd(df)
#             df = detect_volume_spikes(df)

#             # Show outputs
#             show_candlestick_chart(df)
#             show_volume_chart(df)
#             show_key_statistics(df)
#             show_price_alert(df)
#             show_trade_suggestions(df)

#             # Export
#             export_csv(df, ticker)
