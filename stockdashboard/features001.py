import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_features_tab():
    st.header("🛠 Trading Features")
    st.markdown("""
    Here are some features you can explore:
    - 🔔 Price Alerts
    - 📊 Technical Indicators (RSI, MACD, Moving Averages)
    - 📦 Volume Spike Detection
    - 🧠 AI-based Trade Suggestions (coming soon!)
    """)
    st.info("Want a new feature? Just ask!")

# 📉 Add Moving Averages
def add_moving_averages(df, windows=[20, 50, 100]):
    for window in windows:
        df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()
    return df

# 📦 Volume Chart
def show_volume_chart(df):
    st.subheader("📦 Volume Over Time")
    st.bar_chart(df.set_index("date")["Volume"])

# 📌 Key Statistics
def show_key_statistics(df):
    st.subheader("📌 Key Statistics")
    stats = {
        "Highest Close": df["Close"].max(),
        "Lowest Close": df["Close"].min(),
        "Average Volume": int(df["Volume"].mean()),
        "Total Trades": int(df["Trades"].sum())
    }
    st.write(pd.DataFrame(stats.items(), columns=["Metric", "Value"]))

# 📅 Date Range Filter
def filter_by_date(df):
    st.subheader("📅 Filter by Date Range")
    start = st.date_input("Start Date", df["date"].min())
    end = st.date_input("End Date", df["date"].max())
    filtered_df = df[(df["date"] >= start) & (df["date"] <= end)]
    return filtered_df

# 🕯️ Candlestick Chart
def show_candlestick_chart(df):
    st.subheader("🕯️ Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(
        x=df["date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])
    st.plotly_chart(fig, use_container_width=True)

# 📥 Export CSV
def export_csv(df, ticker):
    st.download_button(
        label="📥 Download Data as CSV",
        data=df.to_csv(index=False),
        file_name=f"{ticker}_stock_data.csv",
        mime="text/csv"
    )

# import streamlit as st
# import pandas as pd # noqa

# def show_features_tab():
#     st.header("🛠 Trading Features")
#     st.markdown("""
#     Here are some features you can explore:
#     - 🔔 Price Alerts
#     - 📊 Technical Indicators (RSI, MACD, Moving Averages)
#     - 📦 Volume Spike Detection
#     - 🧠 AI-based Trade Suggestions (coming soon!)
#     """)
#     st.info("Want a new feature? Just ask!")

# def add_moving_averages(df, windows=[20, 50, 100]):
#     """
#     Adds simple moving averages to the DataFrame.
#     """
#     for window in windows:
#         df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()
#     return df

# def filter_by_date(df, start=None, end=None):
#     """
#     Filters the DataFrame between start and end dates.
#     """
#     if start:
#         df = df[df["date"] >= pd.to_datetime(start).date()]
#     if end:
#         df = df[df["date"] <= pd.to_datetime(end).date()]
#     return df
