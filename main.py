import os
from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from src import api_key
import mainfeatures

# ---------------------------------------------------------
# INITIAL SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Stock Analytics V2", layout="wide")
api_key.load_polygon_key()

BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
API_KEY = os.environ.get("POLYGON_API_KEY1")
START_DATE = "2015-01-01"
END_DATE = "2026-07-31"

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
    "HDFC Bank (HDFCBANK)": "HDFCBANK",
}

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div style='padding:10px 0; text-align:center;'>
        <h1 style='margin-bottom:0;'>📊 Stock Analytics Dashboard — Version 2</h1>
        <p style='color:gray; margin-top:4px;'>Multi‑ticker analysis with JSON, Tier‑B, Tier‑C & Pro Mode</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(f"📅 Today: {datetime.now().strftime('%A, %d %B %Y')}")

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.header("⚙️ Controls")

selected_company = st.sidebar.selectbox("Select Company", list(COMPANIES.keys()))
ticker = COMPANIES[selected_company]

st.sidebar.markdown("---")

show_ma = st.sidebar.checkbox("Show Moving Averages", value=True)
show_spikes = st.sidebar.checkbox("Highlight Volume Spikes", value=True)

st.sidebar.markdown("---")

date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.strptime(START_DATE, "%Y-%m-%d").date(), datetime.strptime(END_DATE, "%Y-%m-%d").date()),
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date_sel, end_date_sel = date_range
else:
    start_date_sel = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    end_date_sel = datetime.strptime(END_DATE, "%Y-%m-%d").date()

st.sidebar.markdown("---")
st.sidebar.info("API: Polygon.io\nVersion: V2 UI")

# ---------------------------------------------------------
# FETCH DATA
# ---------------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker: str) -> pd.DataFrame | None:
    if not API_KEY:
        st.error("API key missing. Set POLYGON_API_KEY1 in environment.")
        return None

    url = f"{BASE_URL}/{ticker}/range/1/day/{START_DATE}/{END_DATE}?apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        st.error(f"Failed to fetch data (status {response.status_code}).")
        return None

    data = response.json()
    if "results" not in data:
        st.warning("No results found for this ticker.")
        return None

    df = pd.DataFrame(data["results"])
    df["date"] = pd.to_datetime(df["t"], unit="ms").dt.date

    df = df.rename(
        columns={
            "v": "Volume",
            "vw": "VWAP",
            "o": "Open",
            "c": "Close",
            "h": "High",
            "l": "Low",
            "n": "Trades",
        }
    )

    return df[["date", "Volume", "VWAP", "Open", "Close", "High", "Low", "Trades"]]


df = fetch_stock_data(ticker)
if df is None or df.empty:
    st.stop()

# ---------------------------------------------------------
# PROCESS DATA
# ---------------------------------------------------------
df = mainfeatures.add_moving_averages(df)
filtered_df = mainfeatures.filter_by_date(df, start_date_sel, end_date_sel)

if filtered_df.empty:
    st.warning("No data in selected date range.")
    st.stop()

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📈 Dashboard",
        "🧩 JSON Summary",
        "📘 Tier‑B Lesson",
        "💼 Tier‑C Case Study",
        "🧠 Pro Mode",
    ]
)

# ---------------------------------------------------------
# TAB 1 — DASHBOARD
# ---------------------------------------------------------
with tab1:
    st.subheader(f"📈 Price Trend — {ticker}")
    mainfeatures.show_price_chart(filtered_df, show_ma)

    col_top = st.columns(2)
    with col_top[0]:
        mainfeatures.show_volume_chart(filtered_df, show_spikes)
    with col_top[1]:
        mainfeatures.show_key_statistics(filtered_df)

    st.markdown("---")
    st.subheader("🕯️ Candlestick View")
    mainfeatures.show_candlestick_chart(filtered_df, show_ma)

    st.markdown("---")
    mainfeatures.export_csv(filtered_df, ticker)

# ---------------------------------------------------------
# TAB 2 — JSON SUMMARY
# ---------------------------------------------------------
with tab2:
    st.subheader("🧩 JSON Summary")
    json_output = mainfeatures.generate_json_summary(filtered_df, ticker)
    st.json(json_output)

# ---------------------------------------------------------
# TAB 3 — TIER‑B LESSON
# ---------------------------------------------------------
with tab3:
    st.subheader("📘 Student‑Friendly Lesson (Tier‑B)")
    st.markdown(mainfeatures.generate_tierB_script(filtered_df, ticker))

# ---------------------------------------------------------
# TAB 4 — TIER‑C CASE STUDY
# ---------------------------------------------------------
with tab4:
    st.subheader("💼 Premium Case Study (Tier‑C)")
    st.markdown(mainfeatures.generate_tierC_case_study(filtered_df, ticker))

# ---------------------------------------------------------
# TAB 5 — PRO MODE
# ---------------------------------------------------------
with tab5:
    st.subheader("🧠 Pro Mode — Advanced Analytics")
    mainfeatures.show_pro_mode_panel(filtered_df, ticker)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <hr>
    <div style='text-align:center; color:gray; font-size:13px;'>
        Stock Analytics V2 • Built by Jagdev Singh Dosanjh • Powered by Polygon.io & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
