import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
import api_key
import features
from st_social_media_links import SocialMediaIcons

def show_polygon_tab():
    api_key.load_polygon_key()

    st.markdown("""
        <div style='background-color:#0E1117; padding:15px; border-radius:10px;'>
            <h1 style='color:#F5F5F5; text-align:center;'>📊 Stock Updates Dashboard</h1>
            <p style='color:#CCCCCC; text-align:center;'>Top Global Companies by Sector - Tracker by Jagdev Singh Dosanjh</p>
        </div>
        <br>
    """, unsafe_allow_html=True)

    BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
    API_KEY = os.environ.get("POLYGON_API_KEY1")
    START_DATE = "2023-08-21"
    END_DATE = "2025-08-31"

    COMPANY_SECTORS = [
        ["Technology", [
            ("Apple Inc. (AAPL)", "AAPL"),
            ("Alphabet Inc. (GOOGL)", "GOOGL"),
            ("Microsoft Corporation (MSFT)", "MSFT"),
            ("NVIDIA Corporation (NVDA)", "NVDA"),
            ("Meta Platforms, Inc. (META)", "META"),
            ("Intel Corporation (INTC)", "INTC"),
            ("Advanced Micro Devices, Inc. (AMD)", "AMD"),
            ("Oracle Corporation (ORCL)", "ORCL"),
            ("Cisco Systems, Inc. (CSCO)", "CSCO"),
            ("IBM Corporation (IBM)", "IBM"),
            ("Infosys Ltd. ADR (INFY)", "INFY"),
            ("Broadcom Inc. (AVGO)", "AVGO"),
            ("Qualcomm Inc. (QCOM)", "QCOM"),
            ("Adobe Inc. (ADBE)", "ADBE"),
            ("Snowflake Inc. (SNOW)", "SNOW"),
            ("Palantir Technologies Inc. (PLTR)", "PLTR")
        ]],
        ["Consumer Discretionary", [
            ("Tesla, Inc. (TSLA)", "TSLA"),
            ("Amazon.com, Inc. (AMZN)", "AMZN"),
            ("Netflix, Inc. (NFLX)", "NFLX"),
            ("Airbnb, Inc. (ABNB)", "ABNB"),
            ("Uber Technologies, Inc. (UBER)", "UBER")
        ]],
        ["Fintech", [
            ("PayPal Holdings, Inc. (PYPL)", "PYPL"),
            ("Block, Inc. (SQ)", "SQ")
        ]],
        ["Enterprise Software & Cloud", [
            ("Salesforce, Inc. (CRM)", "CRM"),
            ("Snowflake Inc. (SNOW)", "SNOW"),
            ("Palantir Technologies Inc. (PLTR)", "PLTR")
        ]]
    ]

    st.caption(f"📅 Today's Date: {datetime.now().strftime('%A, %d %B %Y')}")

    sector_names = [sector for sector, _ in COMPANY_SECTORS]
    selected_sector = st.selectbox("Select Sector", sector_names)

    sector_companies = dict(COMPANY_SECTORS)[selected_sector]
    selected_company = st.selectbox("Select Company", [name for name, _ in sector_companies])
    ticker = dict(sector_companies)[selected_company]

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

    if df is not None:
        st.subheader(f"Stock Data for {selected_company}")
        st.dataframe(df, use_container_width=True)
        st.subheader("📊 Price Trend")
        st.line_chart(df.set_index("date")[["Open", "Close", "High", "Low"]])

        df = features.add_moving_averages(df)
        filtered_df = features.filter_by_date(df)
        features.show_volume_chart(filtered_df)
        features.show_key_statistics(filtered_df)
        features.show_candlestick_chart(filtered_df)
        features.export_csv(filtered_df, ticker)
    else:
        st.stop()

    social_media_links = [
        "https://www.facebook.com/jagdevsinghdosanjh",
        "https://www.youtube.com/jagdevsinghdosanjh",
        "https://www.instagram.com/jagdevsinghdosanjh",
        "https://www.github.com/jagdevsinghdosanjh",
        "https://www.linkedin.com/in/jagdevsinghdosanjh",
        "https://x.com/DosanjhJagdev"
    ]

    social_media_icons = SocialMediaIcons(social_media_links)
    social_media_icons.render(sidebar=False)

    st.markdown("""
        <br><hr>
        <div style='text-align:center; color:#888888; font-size:14px;'>
            Made with ❤️ by Jagdev Singh Dosanjh<br>
            Powered by Polygon.io & Streamlit<br>
            <a href="https://dosanjhpubsasr.org">DOSANJHPUBSASR.ORG</a>
        </div>
    """, unsafe_allow_html=True)
