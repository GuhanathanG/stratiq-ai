import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(layout="wide")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("# 🤖 STRATIQ AI Co-Pilot")
st.markdown("Ask strategic questions about your business.")
st.markdown("---")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask STRATIQ anything...")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Analyzing..."):
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.chat_history
        )

    reply = response.choices[0].message.content
    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])