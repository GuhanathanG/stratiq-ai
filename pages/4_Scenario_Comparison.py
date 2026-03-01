import streamlit as st
import sqlite3
import pandas as pd

# ===== AUTH PROTECTION =====
if not st.session_state.get("authenticated", False):
    st.warning("Please login first.")
    st.stop()

st.set_page_config(layout="wide")

st.markdown("# 📊 Scenario Comparison Dashboard")
st.markdown("Compare saved financial scenarios and identify the strongest performer.")
st.markdown("---")

# ===== CONNECT TO DATABASE =====

conn = sqlite3.connect("stratiq.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price REAL,
    units REAL,
    profit REAL,
    irr REAL,
    ltv_cac REAL
)
""")

conn.commit()

# Read data safely
try:
    df = pd.read_sql("SELECT * FROM scenarios", conn)
except:
    df = pd.DataFrame()

conn.close()

# ===== DISPLAY DATA =====

if df.empty:
    st.warning("No saved scenarios found. Save scenarios from the Dashboard first.")
else:

    st.markdown("## 📋 Saved Scenarios")
    st.dataframe(df)

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

    best_profit_index = df["profit"].idxmax()
    best_scenario = df.loc[best_profit_index]

    st.markdown("---")
    st.success(f"""
🏆 Best Performing Scenario:

Profit: ₹{best_scenario['profit']:,.0f}
IRR: {best_scenario['irr']:.2%}
LTV/CAC: {best_scenario['ltv_cac'] if 'ltv_cac' in df.columns else 'N/A'}
""")