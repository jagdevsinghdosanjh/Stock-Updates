import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime  # ✅ Now meaningfully used
import api_key
import features
from st_social_media_links import SocialMediaIcons

api_key.load_polygon_key()
# Header
st.markdown("""
    <div style='background-color:#0E1117; padding:15px; border-radius:10px;'>
        <h1 style='color:#F5F5F5; text-align:center;'>📊 Stock Updates Dashboard</h1>
        <p style='color:#CCCCCC; text-align:center;'>Track real-time data for top global and Indian companies</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# --- Configuration ---
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
API_KEY = os.environ.get("POLYGON_API_KEY1")
START_DATE = "2015-01-01"
END_DATE = "2025-08-31"

# --- Company Options ---
COMPANIES = {
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

# --- Streamlit UI ---
st.set_page_config(page_title="Multi-Company Stock App", layout="wide")
st.title("📈 Stock Data Viewer")

# ✅ Display current date using datetime
st.caption(f"📅 Today's Date: {datetime.now().strftime('%A, %d %B %Y')}")

selected_company = st.selectbox("Select a Company", list(COMPANIES.keys()))
ticker = COMPANIES[selected_company]

# --- Fetch Data ---
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    if not API_KEY:
        st.error("API key not found. Please set POLYGON_API_KEY in your environment.")
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

# --- Display Data ---
if df is not None:
    st.subheader(f"Stock Data for {selected_company}")
    st.dataframe(df, use_container_width=True)

    # --- Chart ---
    st.subheader("📊 Price Trend")
    st.line_chart(df.set_index("date")[["Open", "Close", "High", "Low"]])
else:
    st.stop()
    
    # Add moving averages
df = features.add_moving_averages(df)

# Filter by date
filtered_df = features.filter_by_date(df)

# Show enhanced features
features.show_volume_chart(filtered_df)
features.show_key_statistics(filtered_df)
features.show_candlestick_chart(filtered_df)
features.export_csv(filtered_df, ticker)

social_media_links = [
    "https://www.facebook.com/jagdevsinghdosanjh",
    "https://www.youtube.com/jagdevsinghdosanjh",
    "https://www.instagram.com/jagdevsinghdosanjh",
    "https://www.github.com/jagdevsinghdosanjh",
    "https://www.linkedin.com/in/jagdevsinghdosanjh"
    "https://x.com/DosanjhJagdev"
]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render(sidebar=True)  # or sidebar=False for main page

    
# Footer
st.markdown("""
    <br><hr>
    <div style='text-align:center; color:#888888; font-size:14px;'>
        Made with ❤️ by Jagdev Singh Dosanjh<br>
        Powered by Polygon.io & Streamlit<br>
        <a href="https://dosanjhpubsasr.org">DOSANJHPUBSASR.ORG</a>
    </div>
""", unsafe_allow_html=True)
