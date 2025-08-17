import streamlit as st
from philosophy.symbolic_lore import display_lore
from philosophy.indicator_interpretation import interpret_indicators
from philosophy.chart_annotations import annotate_chart
import yfinance as yf
from technical_indicators import calculate_indicators, plot_indicators  # reuse from your existing module

def philosophy_tab():
    st.header("🧘 Philosophy of Market Movements")
    st.markdown("Explore the symbolic essence of price, breath, and duality through technical indicators.")

    ticker = st.selectbox("Choose a Stock", ["AAPL", "GOOGL", "TSLA", "INFY", "RELIANCE", "TCS"])
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
