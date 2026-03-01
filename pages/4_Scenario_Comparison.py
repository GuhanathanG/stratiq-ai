import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout="wide")

st.markdown("# 📊 Scenario Comparison Dashboard")
st.markdown("Compare saved financial scenarios and identify the strongest performer.")
st.markdown("---")

# ===== CONNECT TO DATABASE =====

conn = sqlite3.connect("stratiq.db")
df = pd.read_sql("SELECT * FROM scenarios", conn)
conn.close()

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

    st.markdown("## 📊 IRR Comparison")

    if "irr" in df.columns:
        irr_chart = df[["irr"]].copy()
        irr_chart.index = [f"Scenario {i+1}" for i in range(len(df))]
        st.bar_chart(irr_chart)

    # ===== IDENTIFY BEST SCENARIO =====

    if "profit" in df.columns:
        best_profit_index = df["profit"].idxmax()
        best_scenario = df.loc[best_profit_index]

        st.markdown("---")
        st.success(f"""
        🏆 Best Performing Scenario:

        Profit: ₹{best_scenario['profit']:,.0f}
        IRR: {best_scenario['irr']:.2%} (if available)
        LTV/CAC: {best_scenario['ltv_cac'] if 'ltv_cac' in df.columns else 'N/A'}
        """)