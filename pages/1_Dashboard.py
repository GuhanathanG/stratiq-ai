import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf

st.set_page_config(layout="wide")

st.markdown("# 📊 Financial Dashboard")
st.markdown("---")

# Sidebar Inputs
price = st.sidebar.number_input("Selling Price", value=1000.0)
units = st.sidebar.number_input("Units Sold", value=100.0)
variable_cost = st.sidebar.number_input("Variable Cost", value=400.0)
fixed_cost = st.sidebar.number_input("Fixed Cost", value=50000.0)
growth_rate = st.sidebar.slider("Growth Rate (%)", 0, 50, 10) / 100
initial_investment = st.sidebar.number_input("Initial Investment", value=300000.0)
discount_rate = st.sidebar.slider("Discount Rate (%)", 0, 30, 10) / 100

# Calculations
revenue = price * units
profit = revenue - (variable_cost * units + fixed_cost)

cash_flows = [-initial_investment] + [profit] * 12
irr = npf.irr(cash_flows)
npv = npf.npv(discount_rate, cash_flows)

months = np.arange(1, 13)
projection = [revenue * (1 + growth_rate) ** m for m in months]

# Metrics
st.markdown("## Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"₹{revenue:,.0f}")
col2.metric("Profit", f"₹{profit:,.0f}")
col3.metric("IRR", f"{irr:.2%}" if irr else "N/A")

st.markdown("NPV:", f"₹{npv:,.0f}")

st.markdown("---")

# Chart
st.markdown("## Revenue Projection")
df = pd.DataFrame({"Month": months, "Revenue": projection})
st.line_chart(df.set_index("Month"))