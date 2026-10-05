"""
AlgoLens — Look Inside the Algorithm
====================================
Streamlit Web Launcher serving the exact AlgoVision Stitch IDE design system.
Provides pixel-perfect fidelity with zero formatting glitches and 60fps simulation.
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components

favicon_path = os.path.join(os.path.dirname(__file__), "brain.png")
brain_b64 = ""
if os.path.exists(favicon_path):
    with open(favicon_path, "rb") as f:
        brain_b64 = base64.b64encode(f.read()).decode("utf-8")

# Configure full-screen layout with brain.png favicon
st.set_page_config(
    page_title="AlgoVision — AlgoLens IDE v3.12",
    page_icon=favicon_path if os.path.exists(favicon_path) else "🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject favicon links
if brain_b64:
    st.markdown(f'<link rel="icon" type="image/png" href="data:image/png;base64,{brain_b64}"><link rel="shortcut icon" type="image/png" href="data:image/png;base64,{brain_b64}">', unsafe_allow_html=True)

# Eliminate Streamlit padding, header, footer, and sidebar margins
st.markdown("""
<style>
/* Remove all Streamlit chrome, header, toolbar, paddings, and top black space */
header, [data-testid="stHeader"], footer, #MainMenu, [data-testid="stSidebar"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
    margin: 0 !important;
    padding: 0 !important;
}
html, body, .stApp {
    background-color: #070e1d !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}
[data-testid="stAppViewContainer"], section.main, [data-testid="stAppViewBlockContainer"], .block-container, [data-testid="stVerticalBlock"] {
    padding: 0 !important;
    margin: 0 !important;
    top: 0 !important;
    left: 0 !important;
    max-width: 100vw !important;
    height: 100vh !important;
}
iframe {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    display: block !important;
    z-index: 999999 !important;
}
</style>
""", unsafe_allow_html=True)

# Load the exact unified Stitch HTML application
static_html_path = os.path.join(os.path.dirname(__file__), "algolens", "static", "index.html")

if os.path.exists(static_html_path):
    with open(static_html_path, "r", encoding="utf-8") as f:
        stitch_html = f.read()
    components.html(stitch_html, height=1100, scrolling=True)
else:
    st.error(f"Frontend bundle not found at {static_html_path}")
