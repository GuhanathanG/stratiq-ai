import streamlit as st
import sqlite3
import pandas as pd

# ===== AUTH PROTECTION =====
if not st.session_state.get("authenticated", False):
    st.warning("Please login first.")
    st.stop()

st.set_page_config(layout="wide")

st.markdown("# 📊 Scenario Comparison Dashboard")
st.markdown("Compare your saved financial scenarios.")
st.markdown("---")

# ===== CONNECT TO DATABASE =====

conn = sqlite3.connect("stratiq.db")
cursor = conn.cursor()

# Ensure table exists (with username column)
cursor.execute("""
CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    price REAL,
    units REAL,
    profit REAL,
    irr REAL,
    ltv_cac REAL
)
""")

conn.commit()

# ===== LOAD ONLY CURRENT USER DATA =====

try:
    df = pd.read_sql(
        "SELECT * FROM scenarios WHERE username = ?",
        conn,
        params=(st.session_state.username,)
    )
except:
    df = pd.DataFrame()

conn.close()

# ===== DISPLAY DATA =====

if df.empty:
    st.warning("You have no saved scenarios yet.")
else:

    st.markdown("## 📋 Your Saved Scenarios")
    st.dataframe(df.drop(columns=["id", "username"]))

    st.markdown("---")
    st.markdown("## 📈 Profit Comparison")

    profit_chart = df[["profit"]].copy()
    profit_chart.index = [f"Scenario {i+1}" for i in range(len(df))]
    st.bar_chart(profit_chart)

    if "irr" in df.columns:
        st.markdown("## 📊 IRR Comparison")
        irr_chart = df[["irr"]].copy()
        irr_chart.index = [f"Scenario {i+1}" for i in range(len(df))]
        st.bar_chart(irr_chart)

    # ===== BEST SCENARIO =====

    best_profit_index = df["profit"].idxmax()
    best_scenario = df.loc[best_profit_index]

    st.markdown("---")
    st.success(f"""
🏆 Your Best Performing Scenario:

Profit: ₹{best_scenario['profit']:,.0f}  
IRR: {best_scenario['irr']:.2%}
""")