import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Debug: Check what secrets are loaded
st.write("Available secrets:", st.secrets)

# Access your API key
api_key = st.secrets["POLYGON_API_KEY"]

# --- Configuration ---
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
API_KEY = os.environ.get("POLYGON_API_KEY")  # ✅ Refactored here
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# --- Company Options ---
COMPANIES = {
    "Apple Inc. (AAPL)": "AAPL",
    "Alphabet Inc. (GOOGL)": "GOOGL",
    "Microsoft Corporation (MSFT)": "MSFT",
    "NVIDIA (NVDA)": "NVDA",
    "Tesla, Inc. (TSLA)": "TSLA",
    "Infosys Ltd. (INFY)": "INFY"
}
# ✅ Display current date using datetime
st.caption(f"📅 Today's Date: {datetime.now().strftime('%A, %d %B %Y')}")
# --- Streamlit UI ---
st.set_page_config(page_title="Multi-Company Stock App", layout="wide")
st.title("📈 Multi-Company Stock Data Viewer")

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

# import streamlit as st
# import requests
# import pandas as pd
# from datetime import datetime

# # --- Configuration ---
# BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
# API_KEY = st.secrets["POLYGON_API_KEY"]
# START_DATE = "2025-01-01"
# END_DATE = "2025-05-11"

# # --- Company Options ---
# COMPANIES = {
#     "Apple Inc. (AAPL)": "AAPL",
#     "Alphabet Inc. (GOOGL)": "GOOGL",
#     "Microsoft Corporation (MSFT)": "MSFT",
#     "NVIDIA (NVDA)": "NVDA",
#     "Tesla, Inc. (TSLA)": "TSLA",
#     "Infosys Ltd. (INFY)": "INFY"
# }

# # --- Streamlit UI ---
# st.set_page_config(page_title="Multi-Company Stock App", layout="wide")
# st.title("📈 Multi-Company Stock Data Viewer")

# selected_company = st.selectbox("Select a Company", list(COMPANIES.keys()))
# ticker = COMPANIES[selected_company]

# # --- Fetch Data ---
# @st.cache_data(ttl=3600)
# def fetch_stock_data(ticker):
#     url = f"{BASE_URL}/{ticker}/range/1/day/{START_DATE}/{END_DATE}?apiKey={API_KEY}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         st.error("Failed to fetch data.")
#         return None
#     data = response.json()
#     if "results" not in data:
#         st.warning("No results found.")
#         return None
#     df = pd.DataFrame(data["results"])
#     df["date"] = pd.to_datetime(df["t"], unit="ms").dt.date
#     df = df.rename(columns={
#         "v": "Volume",
#         "vw": "VWAP",
#         "o": "Open",
#         "c": "Close",
#         "h": "High",
#         "l": "Low",
#         "n": "Trades"
#     })
#     return df[["date", "Volume", "VWAP", "Open", "Close", "High", "Low", "Trades"]]

# df = fetch_stock_data(ticker)

# # --- Display Data ---
# if df is not None:
#     st.subheader(f"Stock Data for {selected_company}")
#     st.dataframe(df, use_container_width=True)

#     # --- Chart ---
#     st.subheader("📊 Price Trend")
#     st.line_chart(df.set_index("date")[["Open", "Close", "High", "Low"]])
# else:
#     st.stop()
