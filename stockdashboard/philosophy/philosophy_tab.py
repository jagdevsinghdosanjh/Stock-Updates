import streamlit as st
from philosophy.symbolic_lore import display_lore
from philosophy.indicator_interpretation import interpret_indicators
from philosophy.chart_annotations import annotate_chart
import yfinance as yf
from technical_indicators import calculate_indicators, plot_indicators  # reuse from your existing module

def philosophy_tab():
    st.header("🧘 Philosophy of Market Movements")
    st.markdown("Explore the symbolic essence of price, breath, and duality through technical indicators.")

    #ticker = st.selectbox("Choose a Stock", ["AAPL", "GOOGL", "TSLA", "INFY", "RELIANCE", "TCS"])
    ticker = st.selectbox("Choose a Stock", [
    # 🇺🇸 US Tech & Innovation
    "AAPL",  # Apple Inc.
    "GOOGL", # Alphabet Inc.
    "MSFT",  # Microsoft Corp.
    "AMZN",  # Amazon.com Inc.
    "META",  # Meta Platforms Inc.
    "TSLA",  # Tesla Inc.
    "NVDA",  # NVIDIA Corp.
    "AMD",   # Advanced Micro Devices
    "INTC",  # Intel Corp.
    "CRM",   # Salesforce

    # 🇺🇸 US Finance & Energy
    "JPM",   # JPMorgan Chase
    "GS",    # Goldman Sachs
    "BAC",   # Bank of America
    "XOM",   # Exxon Mobil
    "CVX",   # Chevron Corp.
    "KO",    # Coca-Cola
    "PEP",   # PepsiCo
    "WMT",   # Walmart
    "DIS",   # Walt Disney

    # 🇮🇳 India Majors
    "INFY",      # Infosys
    "RELIANCE",  # Reliance Industries
    "TCS",       # Tata Consultancy Services
    "HDFCBANK",  # HDFC Bank
    "ICICIBANK", # ICICI Bank
    "LT",        # Larsen & Toubro
    "BHARTIARTL",# Bharti Airtel
    "ITC",       # ITC Ltd.
    "SBIN",      # State Bank of India

    # 🇯🇵 Japan
    "TM",    # Toyota Motor Corp.
    "SONY",  # Sony Group Corp.
    "NTTYY", # Nippon Telegraph & Telephone

    # 🇰🇷 South Korea
    "SSNLF", # Samsung Electronics
    "HYMTF", # Hyundai Motor

    # 🇨🇳 China
    "BABA",  # Alibaba Group
    "JD",    # JD.com
    "TCEHY", # Tencent Holdings
    "BIDU",  # Baidu Inc.

    # 🇪🇺 Europe
    "ASML",  # ASML Holding (Netherlands)
    "SIEGY", # Siemens AG (Germany)
    "NSRGY", # Nestlé (Switzerland)
    "LVMUY", # LVMH (France)
    "SAP",   # SAP SE (Germany)

    # 🇨🇦 Canada
    "SHOP",  # Shopify Inc.
    "RY",    # Royal Bank of Canada

    # 🇦🇷 Latin America
    "MELI",  # MercadoLibre (Argentina)

    # 🧪 Symbolic Disruptors
    "PLTR",  # Palantir Technologies
    "SNOW",  # Snowflake Inc.
    "ARKK",  # ARK Innovation ETF
])

    data = yf.download(ticker, period="6mo", interval="1d")

    if data.empty:
        st.error("Market appears closed. 🕉️ Use this pause to reflect on breath, rhythm, and readiness.")
        return

    df = calculate_indicators(data)
    fig_price, fig_rsi, fig_macd = plot_indicators(df, ticker)

    annotate_chart(fig_price, df)
    st.plotly_chart(fig_price, use_container_width=True)
    st.plotly_chart(fig_rsi, use_container_width=True)
    st.plotly_chart(fig_macd, use_container_width=True)

    interpret_indicators(df)
    display_lore()
