import streamlit as st

st.set_page_config(
    page_title="STRATIQ AI",
    page_icon="🚀",
    layout="wide"
)

# ===== PREMIUM DARK FINTECH THEME =====

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #0f172a);
}

.block-container {
    padding-top: 2rem;
}

h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg,#00f5d4,#00bbf9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.stButton>button {
    background: linear-gradient(90deg,#00f5d4,#00bbf9);
    color: black;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.6rem 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ===== HERO SECTION =====

st.markdown("# STRATIQ AI")
st.markdown("### Financial Decision Intelligence Engine for Founders & Investors")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
    <h3>AI Strategy</h3>
    Intelligent financial recommendations
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
    <h3>Scenario Intelligence</h3>
    Dynamic modeling & simulations
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
    <h3>Investor Reports</h3>
    Executive-grade output
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
## ⚡ Built for Scale

STRATIQ AI combines advanced financial modeling, AI advisory, 
and investor-ready analytics into one decision intelligence platform.
""")

st.success("Premium Fintech Interface Activated")