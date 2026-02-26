import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# ---------------- UI SETUP ----------------
st.set_page_config(page_title="📈 Intraday Trading Dashboard", layout="wide")
st.title("⚡ Live Intraday Stock Tracker")
st.caption(f"📅 {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}")

st.sidebar.header("🔍 Select a Stock")

# ---------------- TICKERS ----------------
popular_tickers = {
    "Apple Inc. (AAPL)": "AAPL",
    "Alphabet Inc. (GOOGL)": "GOOGL",
    "Microsoft Corporation (MSFT)": "MSFT",
    "NVIDIA Corporation (NVDA)": "NVDA",
    "Tesla, Inc. (TSLA)": "TSLA",
    "Infosys Ltd. (INFY)": "INFY.NS",
    "Amazon.com, Inc. (AMZN)": "AMZN",
    "Meta Platforms, Inc. (META)": "META",
    "Intel Corporation (INTC)": "INTC",
    "Advanced Micro Devices, Inc. (AMD)": "AMD",
    "Oracle Corporation (ORCL)": "ORCL",
    "Cisco Systems, Inc. (CSCO)": "CSCO",
    "IBM Corporation (IBM)": "IBM",
    "Reliance Industries Ltd. (RELIANCE)": "RELIANCE.NS",
    "Tata Consultancy Services Ltd. (TCS)": "TCS.NS",
    "HCL Technologies Ltd. (HCLTECH)": "HCLTECH.NS",
    "Wipro Ltd. (WIPRO)": "WIPRO.NS",
    "Bharti Airtel Ltd. (BHARTIARTL)": "BHARTIARTL.NS",
    "ICICI Bank Ltd. (ICICIBANK)": "ICICIBANK.NS",
    "HDFC Bank Ltd. (HDFCBANK)": "HDFCBANK.NS"
}

selected_label = st.sidebar.selectbox("Choose a Ticker", list(popular_tickers.keys()))
ticker = popular_tickers[selected_label]

interval = st.sidebar.selectbox("Interval", ["1m", "5m", "15m", "30m", "60m"])
period = st.sidebar.selectbox("Range", ["1d", "5d", "1wk"])


# ---------------- FETCH FUNCTION (FIXED) ----------------
@st.cache_data(ttl=60)
def fetch_intraday_data(ticker, interval, period):
    session = requests.Session()
    
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    try:
        ticker_obj = yf.Ticker(ticker, session=session)
        df = ticker_obj.history(interval=interval, period=period, prepost=False, actions=False)

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()

        # Normalize datetime column
        if "Datetime" in df.columns:
            df["Datetime"] = pd.to_datetime(df["Datetime"])
        elif "Date" in df.columns:
            df.rename(columns={"Date": "Datetime"}, inplace=True)
            df["Datetime"] = pd.to_datetime(df["Datetime"])
        else:
            df["Datetime"] = pd.to_datetime(df.index)

        return df

    except Exception:
        return pd.DataFrame()


# ---------------- LOAD DATA ----------------
df = fetch_intraday_data(ticker, interval, period)


# ---------------- DISPLAY ----------------
if not df.empty:
    st.subheader(f"📊 Intraday Data for `{ticker}`")
    st.dataframe(df[["Datetime", "Open", "High", "Low", "Close", "Volume"]], use_container_width=True)

    st.subheader("📈 Price Movement")
    st.line_chart(df.set_index("Datetime")[["Open", "Close", "High", "Low"]])

    st.subheader("📦 Volume Trend")
    st.bar_chart(df.set_index("Datetime")["Volume"])

else:
    st.error("⚠️ Failed to fetch data. Yahoo Finance may be blocking your IP. Try again or change interval/period.")


# ---------------- FOOTER ----------------
st.markdown("""
    <hr>
    <div style='text-align:center; color:#888888; font-size:14px;'>
        Made for Intraday Traders ⚡<br>
        Powered by Yahoo Finance & Streamlit
    </div>
""", unsafe_allow_html=True)

# import streamlit as st
# import yfinance as yf
# import pandas as pd
# from datetime import datetime

# st.set_page_config(page_title="📈 Intraday Trading Dashboard", layout="wide")
# st.title("⚡ Live Intraday Stock Tracker")
# st.caption(f"📅 {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}")

# st.sidebar.header("🔍 Select a Stock")

# popular_tickers = {
#     "Apple Inc. (AAPL)": "AAPL",
#     "Alphabet Inc. (GOOGL)": "GOOGL",
#     "Microsoft Corporation (MSFT)": "MSFT",
#     "NVIDIA Corporation (NVDA)": "NVDA",
#     "Tesla, Inc. (TSLA)": "TSLA",
#     "Infosys Ltd. (INFY)": "INFY.NS",
#     "Amazon.com, Inc. (AMZN)": "AMZN",
#     "Meta Platforms, Inc. (META)": "META",
#     "Intel Corporation (INTC)": "INTC",
#     "Advanced Micro Devices, Inc. (AMD)": "AMD",
#     "Oracle Corporation (ORCL)": "ORCL",
#     "Cisco Systems, Inc. (CSCO)": "CSCO",
#     "IBM Corporation (IBM)": "IBM",
#     "Reliance Industries Ltd. (RELIANCE)": "RELIANCE.NS",
#     "Tata Consultancy Services Ltd. (TCS)": "TCS.NS",
#     "HCL Technologies Ltd. (HCLTECH)": "HCLTECH.NS",
#     "Wipro Ltd. (WIPRO)": "WIPRO.NS",
#     "Bharti Airtel Ltd. (BHARTIARTL)": "BHARTIARTL.NS",
#     "ICICI Bank Ltd. (ICICIBANK)": "ICICIBANK.NS",
#     "HDFC Bank Ltd. (HDFCBANK)": "HDFCBANK.NS"
# }

# selected_label = st.sidebar.selectbox("Choose a Ticker", list(popular_tickers.keys()))
# ticker = popular_tickers[selected_label]

# interval = st.sidebar.selectbox("Interval", ["1m", "5m", "15m", "30m", "60m"])
# period = st.sidebar.selectbox("Range", ["1d", "5d", "1wk"])

# @st.cache_data(ttl=60)
# def fetch_intraday_data(ticker, interval, period):
#     try:
#         ticker_obj = yf.Ticker(ticker)
#         df = ticker_obj.history(interval=interval, period=period, prepost=False, actions=False)
#         df = df.reset_index()
#         return df
#     except Exception:
#         return pd.DataFrame()

# df = fetch_intraday_data(ticker, interval, period)

# if not df.empty:
#     st.subheader(f"📊 Intraday Data for `{ticker}`")
#     st.dataframe(df, use_container_width=True)

#     st.subheader("📈 Price Movement")
#     st.line_chart(df.set_index("Datetime")[["Open", "Close", "High", "Low"]])

#     st.subheader("📦 Volume Trend")
#     st.bar_chart(df.set_index("Datetime")["Volume"])
# else:
#     st.error("⚠️ Failed to fetch data. Yahoo Finance may be blocking your IP. Try again or change interval/period.")

# # import streamlit as st
# # import yfinance as yf
# # import pandas as pd
# # from datetime import datetime

# # # --- UI Setup ---
# # st.set_page_config(page_title="📈 Intraday Trading Dashboard", layout="wide")
# # st.title("⚡ Live Intraday Stock Tracker")
# # st.caption(f"📅 {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}")

# # # --- Sidebar Inputs ---
# # st.sidebar.header("🔍 Select a Stock")

# # # Updated tickers with .NS suffix for Indian stocks
# # popular_tickers = {
# #     "Apple Inc. (AAPL)": "AAPL",
# #     "Alphabet Inc. (GOOGL)": "GOOGL",
# #     "Microsoft Corporation (MSFT)": "MSFT",
# #     "NVIDIA Corporation (NVDA)": "NVDA",
# #     "Tesla, Inc. (TSLA)": "TSLA",
# #     "Infosys Ltd. (INFY)": "INFY.NS",
# #     "Amazon.com, Inc. (AMZN)": "AMZN",
# #     "Meta Platforms, Inc. (META)": "META",
# #     "Intel Corporation (INTC)": "INTC",
# #     "Advanced Micro Devices, Inc. (AMD)": "AMD",
# #     "Oracle Corporation (ORCL)": "ORCL",
# #     "Cisco Systems, Inc. (CSCO)": "CSCO",
# #     "IBM Corporation (IBM)": "IBM",
# #     "Reliance Industries Ltd. (RELIANCE)": "RELIANCE.NS",
# #     "Tata Consultancy Services Ltd. (TCS)": "TCS.NS",
# #     "HCL Technologies Ltd. (HCLTECH)": "HCLTECH.NS",
# #     "Wipro Ltd. (WIPRO)": "WIPRO.NS",
# #     "Bharti Airtel Ltd. (BHARTIARTL)": "BHARTIARTL.NS",
# #     "ICICI Bank Ltd. (ICICIBANK)": "ICICIBANK.NS",
# #     "HDFC Bank Ltd. (HDFCBANK)": "HDFCBANK.NS"
# # }

# # selected_label = st.sidebar.selectbox("Choose a Ticker", list(popular_tickers.keys()))
# # ticker = popular_tickers[selected_label]

# # interval = st.sidebar.selectbox("Interval", ["1m", "5m", "15m", "30m", "60m"])
# # period = st.sidebar.selectbox("Range", ["1d", "5d", "1wk"])

# # # --- Fetch Data ---
# # @st.cache_data(ttl=60)
# # def fetch_intraday_data(ticker, interval, period):
# #     df = yf.download(ticker, interval=interval, period=period)

# #     if df.empty:
# #         return df

# #     df = df.reset_index()

# #     # Normalize datetime column
# #     if "Datetime" in df.columns:
# #         df["Datetime"] = pd.to_datetime(df["Datetime"])
# #     elif "Date" in df.columns:
# #         df.rename(columns={"Date": "Datetime"}, inplace=True)
# #         df["Datetime"] = pd.to_datetime(df["Datetime"])
# #     else:
# #         df["Datetime"] = pd.to_datetime(df.index)

# #     return df

# # df = fetch_intraday_data(ticker, interval, period)

# # # --- Display Data ---
# # if not df.empty:
# #     st.subheader(f"📊 Intraday Data for `{ticker}`")
# #     st.dataframe(df[["Datetime", "Open", "High", "Low", "Close", "Volume"]], use_container_width=True)

# #     st.subheader("📈 Price Movement")
# #     st.line_chart(df.set_index("Datetime")[["Open", "Close", "High", "Low"]])

# #     st.subheader("📦 Volume Trend")
# #     st.bar_chart(df.set_index("Datetime")["Volume"])
# # else:
# #     st.warning("No data available. Try a different ticker or time range.")

# # # --- Footer ---
# # st.markdown("""
# #     <hr>
# #     <div style='text-align:center; color:#888888; font-size:14px;'>
# #         Made for Intraday Traders ⚡<br>
# #         Powered by Yahoo Finance & Streamlit
# #     </div>
# # """, unsafe_allow_html=True)
