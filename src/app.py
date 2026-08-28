import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import features
import api_key
import os

# ---------------------------------------------------------
# INITIAL SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Stock Analytics V2", layout="wide")
api_key.load_polygon_key()

BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
API_KEY = os.environ.get("POLYGON_API_KEY1")
START_DATE = "2015-01-01"
END_DATE = "2026-09-30"

COMPANIES = {
    "Apple (AAPL)": "AAPL",
    "Alphabet (GOOGL)": "GOOGL",
    "Microsoft (MSFT)": "MSFT",
    "NVIDIA (NVDA)": "NVDA",
    "Tesla (TSLA)": "TSLA",
    "Infosys (INFY)": "INFY",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META",
    "Intel (INTC)": "INTC",
    "AMD (AMD)": "AMD",
    "Oracle (ORCL)": "ORCL",
    "Cisco (CSCO)": "CSCO",
    "IBM (IBM)": "IBM",
    "Reliance (RELIANCE)": "RELIANCE",
    "TCS (TCS)": "TCS",
    "HCLTech (HCLTECH)": "HCLTECH",
    "Wipro (WIPRO)": "WIPRO",
    "Airtel (BHARTIARTL)": "BHARTIARTL",
    "ICICI Bank (ICICIBANK)": "ICICIBANK",
    "HDFC Bank (HDFCBANK)": "HDFCBANK"
}

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
    <h1 style='text-align:center;'>📊 Stock Analytics Dashboard — Version 2</h1>
    <p style='text-align:center; color:gray;'>Advanced multi‑ticker analysis with JSON, Tier‑B, Tier‑C insights</p>
""", unsafe_allow_html=True)

st.caption(f"📅 Today: {datetime.now().strftime('%A, %d %B %Y')}")

# ---------------------------------------------------------
# TICKER SELECTION
# ---------------------------------------------------------
selected_company = st.selectbox("Select a Company", list(COMPANIES.keys()))
ticker = COMPANIES[selected_company]

# ---------------------------------------------------------
# FETCH DATA
# ---------------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    if not API_KEY:
        st.error("API key missing.")
        return None

    url = f"{BASE_URL}/{ticker}/range/1/day/{START_DATE}/{END_DATE}?apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Failed to fetch data.")
        return None

    data = response.json()
    if "results" not in data:
        st.warning("No results found.")
        return None

    df = pd.DataFrame(data["results"])
    df["date"] = pd.to_datetime(df["t"], unit="ms").dt.date

    df = df.rename(columns={
        "v": "Volume",
        "vw": "VWAP",
        "o": "Open",
        "c": "Close",
        "h": "High",
        "l": "Low",
        "n": "Trades"
    })

    return df[["date", "Volume", "VWAP", "Open", "Close", "High", "Low", "Trades"]]

df = fetch_stock_data(ticker)
if df is None:
    st.stop()

# ---------------------------------------------------------
# PROCESS DATA
# ---------------------------------------------------------
df = features.add_moving_averages(df)
filtered_df = features.filter_by_date(df)

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Dashboard",
    "🧩 JSON Summary",
    "📘 Tier‑B Lesson",
    "💼 Tier‑C Case Study"
])

# ---------------------------------------------------------
# TAB 1 — DASHBOARD
# ---------------------------------------------------------
with tab1:
    st.subheader(f"📈 Price Trend — {ticker}")
    st.line_chart(filtered_df.set_index("date")[["Open", "Close", "High", "Low"]])

    features.show_volume_chart(filtered_df)
    features.show_key_statistics(filtered_df)
    features.show_candlestick_chart(filtered_df)
    features.export_csv(filtered_df, ticker)

# ---------------------------------------------------------
# TAB 2 — JSON SUMMARY
# ---------------------------------------------------------
with tab2:
    st.subheader("🧩 JSON Summary")
    json_output = features.generate_json_summary(filtered_df, ticker)
    st.json(json_output)

# ---------------------------------------------------------
# TAB 3 — TIER‑B LESSON
# ---------------------------------------------------------
with tab3:
    st.subheader("📘 Student‑Friendly Lesson (Tier‑B)")
    st.markdown(features.generate_tierB_script(filtered_df, ticker))

# ---------------------------------------------------------
# TAB 4 — TIER‑C CASE STUDY
# ---------------------------------------------------------
with tab4:
    st.subheader("💼 Premium Case Study (Tier‑C)")
    st.markdown(features.generate_tierC_case_study(filtered_df, ticker))
