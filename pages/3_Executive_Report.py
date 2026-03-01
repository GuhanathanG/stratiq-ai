import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from fpdf import FPDF

st.set_page_config(layout="wide")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("# 📄 Executive Strategy Report")
st.markdown("Generate an investor-ready strategic analysis.")
st.markdown("---")

if st.button("Generate Investor Report"):

    with st.spinner("Generating executive analysis..."):

        prompt = """
You are a senior investment analyst.

Generate a structured investor-grade business evaluation report with:

1. Executive Summary
2. Financial Health Analysis
3. Revenue & Profitability Assessment
4. Scalability Potential
5. Risk Assessment
6. Strategic Recommendations
7. Investment Decision (Invest / Caution / Avoid) with justification

Keep it professional, analytical, and concise.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        report = response.choices[0].message.content

    st.markdown("## 🧠 AI Executive Report")
    st.write(report)

    # -------- PDF EXPORT --------

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    for line in report.split("\n"):
        pdf.multi_cell(0, 6, line)

    pdf.output("STRATIQ_Investor_Report.pdf")

    with open("STRATIQ_Investor_Report.pdf", "rb") as f:
        st.download_button(
            "Download PDF Version",
            f,
            file_name="STRATIQ_Investor_Report.pdf",
            mime="application/pdf"
        )