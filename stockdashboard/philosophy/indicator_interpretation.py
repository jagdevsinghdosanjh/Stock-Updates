import streamlit as st

def interpret_indicators(df):
    rsi = df['RSI'].iloc[-1]
    macd = df['MACD'].iloc[-1]
    signal = df['Signal'].iloc[-1]

    st.subheader("🔮 Symbolic Insights")

    if rsi > 70:
        st.markdown("🌬️ **RSI**: Overbought — Shakti ascends, prepare for reversal.")
    elif rsi < 30:
        st.markdown("🌬️ **RSI**: Oversold — Shiva descends, stillness before renewal.")
    else:
        st.markdown("🌬️ **RSI**: Balanced — breath between cycles.")

    if macd > signal:
        st.markdown("🌊 **MACD**: Bullish crossover — inhale of Shakti.")
    elif macd < signal:
        st.markdown("🌊 **MACD**: Bearish crossover — exhale of Shiva.")
    else:
        st.markdown("🌊 **MACD**: Equilibrium — the dance pauses.")
