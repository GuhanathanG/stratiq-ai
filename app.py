import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from database import save_scenario, load_scenarios

# ================= CONFIG =================

st.set_page_config(
    page_title="STRATIQ AI",
    page_icon="📊",
    layout="wide"
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ================= SESSION STATE =================

defaults = {
    "price": 1000.0,
    "units": 100.0,
    "variable_cost": 400.0,
    "fixed_cost": 50000.0,
    "growth_rate": 0.10,
    "chat_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ================= HEADER =================

st.markdown("# 📊 STRATIQ AI")
st.markdown("### Financial Decision Intelligence Platform")
st.markdown("---")

# ================= AI CHAT / CONTROL =================

st.markdown("## 🤖 STRATIQ AI Co-Pilot")

user_input = st.chat_input("Ask strategy questions or modify variables...")

if user_input:

    st.session_state.chat_history.append({"role": "user", "content": user_input})

    system_prompt = f"""
You are STRATIQ AI, an advanced financial strategy co-pilot.

You have two modes:

1) If user wants to modify variables, respond ONLY with valid JSON:
{{
  "price": number_or_null,
  "units": number_or_null,
  "variable_cost": number_or_null,
  "fixed_cost": number_or_null,
  "growth_rate": decimal_between_0_and_1_or_null
}}

2) If user asks strategic/business questions, respond normally in professional consulting tone.

Current Business State:
Price: {st.session_state.price}
Units: {st.session_state.units}
Variable Cost: {st.session_state.variable_cost}
Fixed Cost: {st.session_state.fixed_cost}
Growth Rate: {st.session_state.growth_rate}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.chat_history
        ]
    )

    ai_reply = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(ai_reply)

        updated = False

        for key in ["price", "units", "variable_cost", "fixed_cost", "growth_rate"]:
            if key in parsed and parsed[key] is not None:
                st.session_state[key] = float(parsed[key])
                updated = True

        if updated:
            st.success("Business parameters updated.")
        else:
            st.info("No changes detected.")

    except:
        st.session_state.chat_history.append(
            {"role": "assistant", "content": ai_reply}
        )

# Display Chat History
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

st.markdown("---")

# ================= SIDEBAR =================

st.sidebar.markdown("## ⚙️ Business Configuration")
st.sidebar.markdown("---")

price = st.sidebar.number_input("Selling Price per Unit", key="price")
units = st.sidebar.number_input("Units Sold per Month", key="units")
variable_cost = st.sidebar.number_input("Variable Cost per Unit", key="variable_cost")
fixed_cost = st.sidebar.number_input("Fixed Cost per Month", key="fixed_cost")

growth_slider = st.sidebar.slider(
    "Monthly Growth Rate (%)",
    0, 50,
    int(st.session_state.growth_rate * 100)
)

st.session_state.growth_rate = growth_slider / 100
growth_rate = st.session_state.growth_rate

marketing_spend = st.sidebar.number_input("Marketing Spend", value=20000.0)
new_customers = st.sidebar.number_input("New Customers Acquired", value=50.0)
initial_investment = st.sidebar.number_input("Initial Investment", value=300000.0)
discount_rate = st.sidebar.slider("Discount Rate (%)", 0, 30, 10) / 100

# ================= CALCULATIONS =================

revenue = price * units
total_variable_cost = variable_cost * units
contribution_margin = price - variable_cost
profit = revenue - (total_variable_cost + fixed_cost)
break_even = fixed_cost / contribution_margin if contribution_margin != 0 else 0

months = np.arange(1, 13)
projected_revenue = [revenue * (1 + growth_rate) ** m for m in months]

cash_flows = [-initial_investment] + projected_revenue
irr = npf.irr(cash_flows)
npv = npf.npv(discount_rate, cash_flows)

cac = marketing_spend / new_customers if new_customers != 0 else 0
ltv = (price * 3 * 2) - cac
ltv_cac_ratio = ltv / cac if cac != 0 else 0

# ================= KPI SECTION =================

st.markdown("## 📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{revenue:,.0f}")
col2.metric("Profit", f"₹{profit:,.0f}")
col3.metric("IRR", f"{irr:.2%}" if irr else "N/A")
col4.metric("LTV/CAC Ratio", f"{ltv_cac_ratio:.2f}")

st.write("NPV:", f"₹{npv:,.0f}")
st.write("Break-even Units:", f"{break_even:,.0f}")

st.markdown("---")

# ================= EXECUTIVE REPORT =================

st.markdown("## 📄 Executive Strategy Report")

if st.button("Generate Executive AI Report"):

    financial_snapshot = f"""
Revenue: {revenue}
Profit: {profit}
IRR: {irr}
NPV: {npv}
LTV/CAC Ratio: {ltv_cac_ratio}
Break-even Units: {break_even}
Price: {price}
Units: {units}
Variable Cost: {variable_cost}
Fixed Cost: {fixed_cost}
Growth Rate: {growth_rate}
"""

    report_prompt = f"""
You are a senior strategy consultant.

Generate a professional executive report with:

1. Business Performance Overview
2. Financial Health Analysis
3. Unit Economics Evaluation
4. Scalability Assessment
5. Key Risks
6. Strategic Recommendations
7. Investment Recommendation

Data:
{financial_snapshot}
"""

    report_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "system", "content": report_prompt}]
    )

    executive_report = report_response.choices[0].message.content

    st.markdown("### 🧠 AI Executive Report")
    st.write(executive_report)

st.markdown("---")

# ================= CHART =================

st.markdown("## 📊 12-Month Revenue Projection")

df = pd.DataFrame({
    "Month": months,
    "Projected Revenue": projected_revenue
})

st.line_chart(df.set_index("Month"))

st.markdown("---")

# ================= SCENARIO MANAGEMENT =================

st.markdown("## 📂 Scenario Management")

if st.button("Save Current Scenario"):
    save_scenario({
        "price": price,
        "units": units,
        "profit": profit,
        "irr": irr,
        "ltv_cac": ltv_cac_ratio
    })
    st.success("Scenario saved successfully!")

past = load_scenarios()
st.dataframe(past)

if not past.empty:
    st.subheader("📊 Scenario Comparison (Profit)")
    comparison_df = past[["profit"]]
    comparison_df.index = range(1, len(comparison_df) + 1)
    st.bar_chart(comparison_df)