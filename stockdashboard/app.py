import streamlit as st

def show_app_tab():
    st.header("🏠 Welcome to Your Trading Dashboard")
    st.markdown("""
    This dashboard helps you:
    - Track live intraday stock data 📈
    - Explore trading features 🛠
    - Stay informed and make smart decisions 💡
    """)
    st.image("https://images.unsplash.com/photo-1611974789857-9c2a0a6f1d1c", caption="Market Pulse", use_container_width=True)
