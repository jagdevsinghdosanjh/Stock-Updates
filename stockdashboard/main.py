import streamlit as st
from app import show_app_tab
from features import show_features_tab
from intraday import show_intraday_tab
from polygon_app import show_polygon_tab
from technical_indicators import technical_tab

st.set_page_config(page_title="📊 Unified Trading Dashboard", layout="wide")
st.title("🧭 Unified Trading Dashboard")

tabs = st.tabs([
    "🏠 Home",
    "🛠 Features",
    "📈 Intraday Tracker",
    "🌐 Polygon Stock Dashboard",
    "Technical Indicators"
])

with tabs[0]:
    show_app_tab()

with tabs[1]:
    show_features_tab()

with tabs[2]:
    show_intraday_tab()

with tabs[3]:
    show_polygon_tab()
    
with tabs[4]:
    technical_tab()


# import streamlit as st
# from app import show_app_tab
# from features import show_features_tab
# from intraday import show_intraday_tab

# st.set_page_config(page_title="📊 Unified Trading Dashboard", layout="wide")
# st.title("🧭 Unified Trading Dashboard")

# tabs = st.tabs(["🏠 Home", "🛠 Features", "📈 Intraday Tracker", "Past Data"])

# with tabs[0]:
#     show_app_tab()

# with tabs[1]:
#     show_features_tab()

# with tabs[2]:
#     show_intraday_tab()
    
# with tabs[3]:
#     show_intraday_tab()
