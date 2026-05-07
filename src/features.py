import pandas as pd #noqa
import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------
# MOVING AVERAGES
# ---------------------------------------------------------
def add_moving_averages(df):
    df["MA_Short"] = df["Close"].rolling(window=20).mean()
    df["MA_Long"] = df["Close"].rolling(window=50).mean()
    return df

# ---------------------------------------------------------
# DATE FILTERING
# ---------------------------------------------------------
def filter_by_date(df):
    return df  # placeholder for future date filters

# ---------------------------------------------------------
# VOLUME CHART
# ---------------------------------------------------------
def show_volume_chart(df):
    st.subheader("📊 Volume Trend")
    st.bar_chart(df.set_index("date")["Volume"])

# ---------------------------------------------------------
# KEY STATISTICS
# ---------------------------------------------------------
def show_key_statistics(df):
    st.subheader("📌 Key Statistics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Latest Close", round(df["Close"].iloc[-1], 2))
    col2.metric("Average Volume", round(df["Volume"].mean(), 2))
    col3.metric("Volatility", round(df["Close"].std(), 2))

# ---------------------------------------------------------
# CANDLESTICK CHART
# ---------------------------------------------------------
def show_candlestick_chart(df):
    st.subheader("🕯️ Candlestick Chart")

    fig = go.Figure(data=[
        go.Candlestick(
            x=df["date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )
    ])

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# EXPORT CSV
# ---------------------------------------------------------
def export_csv(df, ticker):
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{ticker}_data.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# JSON SUMMARY
# ---------------------------------------------------------
def generate_json_summary(df, ticker):
    return {
        "ticker": ticker,
        "latest_close": float(df["Close"].iloc[-1]),
        "avg_volume": float(df["Volume"].mean()),
        "volatility": float(df["Close"].std()),
        "trend_direction": detect_trend(df),
        "spike_days": detect_spikes(df),
    }

# ---------------------------------------------------------
# TIER‑B LESSON
# ---------------------------------------------------------
def generate_tierB_script(df, ticker):
    return f"""
### Understanding {ticker}

This chart shows how the price of {ticker} moves over time.

- **Open, High, Low, Close** show daily price movement.
- **Volume spikes** indicate strong buying or selling.
- **Moving averages** help identify long-term trends.
- **Uptrends** mean buyers dominate.
- **Downtrends** mean sellers dominate.

This helps students understand real market behaviour.
"""

# ---------------------------------------------------------
# TIER‑C CASE STUDY
# ---------------------------------------------------------
def generate_tierC_case_study(df, ticker):
    return f"""
## Premium Case Study: {ticker}

### 1. Market Cycle Analysis
We identify phases like accumulation, uptrend, distribution, correction, and base formation.

### 2. Statistical Interpretation
- Trend slope: {round(df['Close'].iloc[-1] - df['Close'].iloc[0], 2)}
- Volatility: {round(df['Close'].std(), 2)}
- Volume anomalies: {len(detect_spikes(df))} spike days

### 3. Economic Interpretation
We connect price behaviour with macro factors, sector cycles, and company fundamentals.

### 4. Q&A Prompts
- Why did volume spike on certain dates?
- What does a flattening moving average indicate?
- How do we identify a distribution zone?
- What signals a capitulation bottom?
"""

# ---------------------------------------------------------
# TREND DETECTION
# ---------------------------------------------------------
def detect_trend(df):
    if df["Close"].iloc[-1] > df["Close"].iloc[0]:
        return "Uptrend"
    return "Downtrend"

# ---------------------------------------------------------
# SPIKE DETECTION
# ---------------------------------------------------------
def detect_spikes(df):
    threshold = df["Volume"].mean() * 2
    spikes = df[df["Volume"] > threshold]["date"].astype(str).tolist()
    return spikes

# ---------------------------------------------------------
# VOLATILITY DETECTION
# ---------------------------------------------------------
def detect_volatility(df):
    return df["Close"].std()
