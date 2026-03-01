import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== AUTH PROTECTION =====
if not st.session_state.get("authenticated", False):
    st.warning("Please login first.")
    st.stop()

st.set_page_config(layout="wide")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("# 🤖 STRATIQ AI — Strategic Co-Pilot")
st.markdown("Live financial intelligence based on your dashboard.")
st.markdown("---")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

financial_data = st.session_state.get("financial_data", None)

if not financial_data:
    st.warning("Please configure values in the Financial Dashboard first.")
else:

    user_input = st.chat_input("Ask about scalability, pricing, funding, risks...")

    if user_input:

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        system_prompt = f"""
You are STRATIQ AI — a senior financial strategist.

Analyze the business using the real financial data below.

Financial Data:
Price: {financial_data['price']}
Units: {financial_data['units']}
Revenue: {financial_data['revenue']}
Profit: {financial_data['profit']}
IRR: {financial_data['irr']}
NPV: {financial_data['npv']}
Growth Rate: {financial_data['growth_rate']}
Fixed Cost: {financial_data['fixed_cost']}
Variable Cost: {financial_data['variable_cost']}

Respond in structured format:

1. Situation Analysis
2. Financial Interpretation
3. Strategic Insight
4. Risks
5. Recommendation
"""

        with st.spinner("Analyzing business..."):
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.chat_history
                ]
            )

        reply = response.choices[0].message.content

        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply}
        )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])