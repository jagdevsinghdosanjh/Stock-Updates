def load_polygon_key():
    import os
    import streamlit as st
    key1 = st.secrets.get("POLYGON_API_KEY1")
    key2 = st.secrets.get("POLYGON_API_KEY2")
    if key1:
        os.environ["POLYGON_API_KEY1"] = key1
    else:
        st.error("POLYGON_API_KEY1 not found in secrets.")
    if key2:
        os.environ["POLYGON_API_KEY2"] = key2
    else:
        st.error("POLYGON_API_KEY2 not found in secrets.")
        
