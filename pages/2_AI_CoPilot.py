import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(layout="wide")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("# 🤖 STRATIQ AI — Strategic Co-Pilot")
st.markdown("Investor-grade financial & strategy intelligence.")
st.markdown("---")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask about scalability, pricing, funding, risks...")

if user_input:

    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    system_prompt = """
You are STRATIQ AI — a senior financial strategist and investment analyst.

Respond in a structured professional format:

1. Situation Analysis
2. Financial Implications
3. Strategic Insight
4. Risks (if any)
5. Recommendation

Be concise, analytical, and executive-level.
"""

    with st.spinner("Analyzing business scenario..."):
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

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])