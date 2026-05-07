import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------
# MOVING AVERAGES
# ---------------------------------------------------------
def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA_Short"] = df["Close"].rolling(window=20).mean()
    df["MA_Long"] = df["Close"].rolling(window=50).mean()
    return df


# ---------------------------------------------------------
# DATE FILTERING
# ---------------------------------------------------------
def filter_by_date(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    df = df.copy()
    mask = (df["date"] >= start_date) & (df["date"] <= end_date)
    return df.loc[mask]


# ---------------------------------------------------------
# PRICE CHART
# ---------------------------------------------------------
def show_price_chart(df: pd.DataFrame, show_ma: bool = True) -> None:
    data = df.set_index("date")[["Open", "Close", "High", "Low"]]
    st.line_chart(data)

    if show_ma and "MA_Short" in df.columns and "MA_Long" in df.columns:
        st.line_chart(df.set_index("date")[["MA_Short", "MA_Long"]])


# ---------------------------------------------------------
# VOLUME CHART
# ---------------------------------------------------------
def show_volume_chart(df: pd.DataFrame, show_spikes: bool = True) -> None:
    st.subheader("📊 Volume Trend")

    if show_spikes:
        threshold = df["Volume"].mean() * 2
        colors = ["#ff4b4b" if v > threshold else "#1f77b4" for v in df["Volume"]]
        fig = go.Figure(
            data=[
                go.Bar(
                    x=df["date"],
                    y=df["Volume"],
                    marker_color=colors,
                    name="Volume",
                )
            ]
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(df.set_index("date")["Volume"])


# ---------------------------------------------------------
# KEY STATISTICS
# ---------------------------------------------------------
def show_key_statistics(df: pd.DataFrame) -> None:
    st.subheader("📌 Key Statistics")

    latest_close = float(df["Close"].iloc[-1])
    avg_volume = float(df["Volume"].mean())
    volatility = float(df["Close"].std())
    trend_dir = detect_trend_direction(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Close", f"{latest_close:.2f}")
    col2.metric("Average Volume", f"{avg_volume:,.0f}")
    col3.metric("Volatility (σ)", f"{volatility:.2f}")
    col4.metric("Trend", trend_dir)


# ---------------------------------------------------------
# CANDLESTICK CHART
# ---------------------------------------------------------
def show_candlestick_chart(df: pd.DataFrame, show_ma: bool = True) -> None:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["date"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price",
            )
        ]
    )

    if show_ma and "MA_Short" in df.columns and "MA_Long" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["MA_Short"],
                mode="lines",
                line=dict(color="orange", width=1.5),
                name="MA Short (20)",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["MA_Long"],
                mode="lines",
                line=dict(color="purple", width=1.5),
                name="MA Long (50)",
            )
        )

    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# EXPORT CSV
# ---------------------------------------------------------
def export_csv(df: pd.DataFrame, ticker: str) -> None:
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{ticker}_data.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------
# JSON SUMMARY
# ---------------------------------------------------------
def generate_json_summary(df: pd.DataFrame, ticker: str) -> dict:
    return {
        "ticker": ticker,
        "latest_close": float(df["Close"].iloc[-1]),
        "avg_volume": float(df["Volume"].mean()),
        "volatility": float(df["Close"].std()),
        "trend_direction": detect_trend_direction(df),
        "trend_class": classify_trend(df),
        "volatility_regime": detect_volatility_regime(df),
        "spike_days": detect_spike_days(df),
    }


# ---------------------------------------------------------
# TIER‑B LESSON
# ---------------------------------------------------------
def generate_tierB_script(df: pd.DataFrame, ticker: str) -> str:
    trend = detect_trend_direction(df)
    vol_regime = detect_volatility_regime(df)
    spike_days = len(detect_spike_days(df))

    return f"""
### Understanding {ticker}

This chart shows how the price of **{ticker}** moves over time.

- **Open, High, Low, Close** describe the daily price movement.
- The overall trend currently appears **{trend.lower()}**.
- The volatility regime is **{vol_regime.lower()}**, which tells us how wild the price swings are.
- There are **{spike_days} days** with unusually high trading volume, which often signal strong buying or selling interest.
- **Moving averages** help smooth out noise and reveal the underlying direction.

This explanation is designed so that a Class 11–12 student can connect real market data with basic concepts of trends, volatility, and demand–supply.
"""


# ---------------------------------------------------------
# TIER‑C CASE STUDY
# ---------------------------------------------------------
def generate_tierC_case_study(df: pd.DataFrame, ticker: str) -> str:
    trend_class = classify_trend(df)
    vol_regime = detect_volatility_regime(df)
    momentum = compute_momentum_score(df)
    risk = compute_risk_score(df)
    spike_days = detect_spike_days(df)

    return f"""
## Premium Case Study: {ticker}

### 1. Market Cycle & Trend Structure
The price action of **{ticker}** currently falls into a **{trend_class.lower()}** regime.
This classification is based on the slope of the closing prices and the relationship between short and long moving averages.

### 2. Volatility & Risk Profile
- Volatility regime: **{vol_regime}**
- Momentum score (0–100): **{momentum:.1f}**
- Risk score (0–100): **{risk:.1f}**

Higher momentum suggests stronger directional conviction, while a higher risk score indicates larger drawdowns and more unstable price swings.

### 3. Volume Anomalies & Institutional Activity
We detect **{len(spike_days)} volume spike days**, where trading volume was significantly above normal.
These days often correspond to institutional participation, news events, or strong sentiment shifts.

### 4. Analytical Q&A Prompts
- On which dates did volume spike, and how did price react afterwards?
- Does the current trend regime support a continuation or a possible reversal?
- How does the volatility regime affect position sizing and risk management?
- Are moving averages flattening, steepening, or crossing over?

### 5. Analyst Mindset
A serious learner should look at **trend, volatility, volume, and momentum together** rather than in isolation.
This case study encourages thinking like an analyst, not just a chart reader.
"""


# ---------------------------------------------------------
# PRO MODE PANEL
# ---------------------------------------------------------
def show_pro_mode_panel(df: pd.DataFrame, ticker: str) -> None:
    trend_class = classify_trend(df)
    vol_regime = detect_volatility_regime(df)
    momentum = compute_momentum_score(df)
    risk = compute_risk_score(df)
    spike_days = detect_spike_days(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Trend Class", trend_class)
    col2.metric("Volatility Regime", vol_regime)
    col3.metric("Momentum Score (0–100)", f"{momentum:.1f}")

    col4, col5 = st.columns(2)
    col4.metric("Risk Score (0–100)", f"{risk:.1f}")
    col5.metric("Volume Spike Days", len(spike_days))

    st.markdown("---")
    st.subheader("🧾 Pro Insights")
    st.markdown(generate_pro_insights(df, ticker, trend_class, vol_regime, momentum, risk, spike_days))


# ---------------------------------------------------------
# ANALYTICS HELPERS
# ---------------------------------------------------------
def detect_trend_direction(df: pd.DataFrame) -> str:
    if df["Close"].iloc[-1] > df["Close"].iloc[0]:
        return "Uptrend"
    elif df["Close"].iloc[-1] < df["Close"].iloc[0]:
        return "Downtrend"
    else:
        return "Sideways"


def classify_trend(df: pd.DataFrame) -> str:
    df = df.copy()
    closes = df["Close"].values
    x = np.arange(len(closes))
    if len(closes) < 2:
        return "Sideways"

    slope, _ = np.polyfit(x, closes, 1)
    if slope > 0.05:
        return "Strong Uptrend"
    elif slope > 0.0:
        return "Mild Uptrend"
    elif slope < -0.05:
        return "Strong Downtrend"
    elif slope < 0.0:
        return "Mild Downtrend"
    else:
        return "Sideways"


def detect_spike_days(df: pd.DataFrame) -> list[str]:
    threshold = df["Volume"].mean() * 2
    spikes = df[df["Volume"] > threshold]["date"].astype(str).tolist()
    return spikes


def detect_volatility_regime(df: pd.DataFrame) -> str:
    vol = df["Close"].pct_change().std()
    if vol < 0.01:
        return "Low"
    elif vol < 0.03:
        return "Medium"
    else:
        return "High"


def compute_momentum_score(df: pd.DataFrame) -> float:
    if len(df) < 10:
        return 50.0
    recent = df["Close"].iloc[-10:]
    change = (recent.iloc[-1] - recent.iloc[0]) / recent.iloc[0]
    score = (change * 100) + 50
    return float(np.clip(score, 0, 100))


def compute_risk_score(df: pd.DataFrame) -> float:
    returns = df["Close"].pct_change().dropna()
    if returns.empty:
        return 50.0
    drawdown = (df["Close"].cummax() - df["Close"]) / df["Close"].cummax()
    max_dd = drawdown.max()
    vol = returns.std()
    raw = (max_dd * 100) + (vol * 100)
    return float(np.clip(raw, 0, 100))


def generate_pro_insights(
    df: pd.DataFrame,
    ticker: str,
    trend_class: str,
    vol_regime: str,
    momentum: float,
    risk: float,
    spike_days: list[str],
) -> str:
    insight_lines = []

    insight_lines.append(f"- **{ticker}** is currently in a **{trend_class.lower()}** regime.")
    insight_lines.append(f"- Volatility is classified as **{vol_regime.lower()}**.")

    if momentum > 60:
        insight_lines.append("- Momentum is strong, indicating buyers are in control recently.")
    elif momentum < 40:
        insight_lines.append("- Momentum is weak, suggesting sellers or lack of conviction.")
    else:
        insight_lines.append("- Momentum is neutral, with no clear dominance of buyers or sellers.")

    if risk > 70:
        insight_lines.append("- Risk score is high — price swings and drawdowns are significant.")
    elif risk < 30:
        insight_lines.append("- Risk score is low — price behaviour is relatively stable.")
    else:
        insight_lines.append("- Risk score is moderate — some volatility, but not extreme.")

    if spike_days:
        insight_lines.append(
            f"- There are **{len(spike_days)} volume spike days**, which may correspond to news or institutional activity."
        )
    else:
        insight_lines.append("- No major volume spikes detected in the selected period.")

    return "\n".join(insight_lines)
