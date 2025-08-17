import streamlit as st

def show_app_tab():
    st.header("🏠 Welcome to Your Trading Dashboard")
    st.markdown("""
    This dashboard helps you:
    - Track live intraday stock data 📈
    - Explore trading features 🛠
    - Stay informed and make smart decisions 💡
    """)
    st.image("https://cdn.prod.website-files.com/6705f4b15aee7ca914fff083/685e47a2b2ab5e3998c98aac_Table%20Usage%20Template%20Image-p-1600.png", caption="Market Pulse", use_container_width=True)
