# ── app.py ────────────────────────────────────────────────────
# Mitma Offboarding App — Ver 0
# Public demo — no login required.
# ─────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
from datetime import datetime
import base64

from views.employee import show_employee_view
from views.manager  import show_manager_view
from views.hr       import show_hr_view

# ── Page configuration ────────────────────────────────────────
st.set_page_config(
    page_title="Mitma Offboarding App | Mitma Consulting",
    page_icon="assets/mitma_favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom styles ─────────────────────────────────────────────
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #ffece1;
        }
        .status-complete {
            color: white;
            background-color: #2e7d32;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 500;
        }
        .status-inprogress {
            color: white;
            background-color: #e65100;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 500;
        }
        .status-pending {
            color: white;
            background-color: #c62828;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

        /* ─────────────────────────────────────────────
        Force Montserrat across all Streamlit elements
        Streamlit 1.57 requires more specific selectors
        ───────────────────────────────────────────── */
        * {
            font-family: 'Montserrat', sans-serif !important;
        }

        html, body {
            font-family: 'Montserrat', sans-serif !important;
        }

        h1, h2, h3, h4, h5, h6, p, div, span, label, button {
            font-family: 'Montserrat', sans-serif !important;
        }

        [data-testid="stMarkdownContainer"] * {
            font-family: 'Montserrat', sans-serif !important;
        }

        [data-testid="stSidebar"] * {
            font-family: 'Montserrat', sans-serif !important;
        }
            
        [data-testid="stSidebar"] {
            background-color: #ffece1;
        }
            
        /* Main page background */
        [data-testid="stAppViewContainer"] {
            background-color: #fffbf8;
        }
        
        /* ─────────────────────────────────────────────
        Hide Streamlit default header elements
        including the hamburger menu and
        the Deploy button for a cleaner demo look.
        ───────────────────────────────────────────── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stSidebarCollapseButton"] {display: none;}
                            
        /* ─────────────────────────────────────────────
        DEMO NOTICE STYLING
        ───────────────────────────────────────────── */
            
        .demo-notice {
            background: #ffffff;
            border: 1px solid #f0d9cc;
            border-radius: 12px;
            padding: 48px 40px;
            text-align: center;
            font-family: 'Montserrat', sans-serif;
            max-width: 600px;
            margin: 40px auto;
        }
        .demo-notice-icon {
            font-size: 40px;
            margin-bottom: 16px;
        }
        .demo-notice-title {
            font-size: 22px;
            font-weight: 700;
            color: #000000;
            margin-bottom: 12px;
        }
        .demo-notice-text {
            font-size: 14px;
            color: #505050;
            margin-bottom: 8px;
        }
        .demo-notice-contact {
            font-size: 13px;
            color: #505050;
            margin-bottom: 24px;
        }
        .demo-notice-logo {
            height: 48px;
            margin-bottom: 24px;
        }
        .demo-notice-buttons {
            display: flex;
            flex-direction: row;
            gap: 10px;
            align-items: center;
            justify-content: center;
            margin-top: 8px;
            flex-wrap: wrap;
        }
        .demo-notice-btn {
            padding: 10px 24px;
            background: #f49052;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
        }
        .demo-notice-btn:hover {
            background: #505050;
        }
        .demo-notice-btn-linkedin {
            padding: 10px 24px;
            background: #f49052;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
        }
        .demo-notice-btn-linkedin:hover {
            background: #505050;
        }
        
        /* ─────────────────────────────────────────────
        SIDEBAR STYLING
        Streamlit sidebar needs explicit targeting
        as it is rendered in a separate container
        from the main page content.
        ───────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: #ffece1;
            font-family: 'Montserrat', sans-serif;
        }

        [data-testid="stSidebar"] * {
            font-family: 'Montserrat', sans-serif;
        }

        [data-testid="stSidebar"] .stRadio label {
            font-size: 13px;
            font-weight: 500;
            color: #505050;
        }
        
        /* ─────────────────────────────────────────────
        LINK BUTTON STYLING
        Targets Streamlit's native link button and
        applies Mitma Consulting orange colour.
        Second button targets LinkedIn blue.
        ───────────────────────────────────────────── */
        [data-testid="stLinkButton"] a {
            background-color: #505050 !important;
            color: white !important;
            border-radius: 8px !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            border: none !important;
        }

        [data-testid="stLinkButton"] a:hover {
            background-color: #f49052 !important;
            color: white !important;
        }
        
        /* ─────────────────────────────────────────────
        Fix link button font colour
        Streamlit link buttons default to blue
        This forces white text on all link buttons
        ───────────────────────────────────────────── */
        [data-testid="stLinkButton"] a {
            color: white !important;
            text-decoration: none !important;
        }

        [data-testid="stLinkButton"] a:hover {
            color: white !important;
        }
        
        [data-testid="stLinkButton"] > a,
        [data-testid="stLinkButton"] > a:visited,
        [data-testid="stLinkButton"] > a:hover,
        [data-testid="stLinkButton"] > a:active {
            color: white !important;
            text-decoration: none !important;
        }
          
        /* Main page button hover */
        .stButton > button:hover {
            background-color: #f49052 !important;
            border-color: #f49052 !important;
            color: white !important;
        }
            
        /* Selectbox dropdown background */
        .stSelectbox > div > div {
            background-color: #ffece1 !important;
        }
        
    </style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────
DATA_DIR = "data/data_files"

@st.cache_data
def load_data():
    employees        = pd.read_csv(f"{DATA_DIR}/departing_employees.csv")
    tasks_master     = pd.read_csv(f"{DATA_DIR}/tasks_master.csv")
    task_completion  = pd.read_csv(f"{DATA_DIR}/task_completion.csv")
    knowledge        = pd.read_csv(f"{DATA_DIR}/knowledge_transfer.csv")
    exit_surveys     = pd.read_csv(f"{DATA_DIR}/exit_surveys.csv")
    return employees, tasks_master, task_completion, knowledge, exit_surveys

employees, tasks_master, task_completion, knowledge, exit_surveys = load_data()

# ── View switcher in sidebar ──────────────────────────────────
# Top of sidebar — controls which view loads.
# Each view then adds its own sidebar content below this.
def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_image_base64("assets/mitma_logo.png")
logo_src    = f"data:image/png;base64,{logo_base64}"

with st.sidebar:
    st.markdown(
        f"""
        <div style="
            font-family:'Montserrat',sans-serif;
            font-weight:700;
            font-size:18px;
            color:#f49052;
            text-align:center;
            margin-bottom:4px;
        ">
        MITMA OFFBOARDING APP
        </div>
        <div style="
            font-size:12px;
            color:#9a8880;
            text-align:center;
            margin-bottom:4px;
        ">
        BY MITMA CONSULTING
        </div>
        <div style="text-align:center;margin-bottom:24px;">
            <span style="
                font-size:10px;
                font-weight:600;
                background:#505050;
                color:white;
                padding:2px 10px;
                border-radius:10px;
            ">DEMO VERSION</span>
        </div>
        <div style="text-align:center;margin-top:50px; margin-bottom:16px;">
            <a href="https://mitmaconsulting.framer.ai" target="_blank">
                <img src="{logo_src}" height="48" alt="Mitma Consulting"/>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # st.markdown("### View")
    selected_view = st.radio(
        "Select to Navigate View",
        options=["👤 Employee", "👔 Manager", "🏢 HR"]
    )

    st.markdown("---")

# ── Render selected view ──────────────────────────────────────
if selected_view == "👤 Employee":
    show_employee_view(employees, tasks_master, task_completion, knowledge, exit_surveys)

elif selected_view == "👔 Manager":
    show_manager_view(employees, tasks_master, task_completion, knowledge, exit_surveys, logo_src)

elif selected_view == "🏢 HR":
    show_hr_view(employees, tasks_master, task_completion, knowledge, exit_surveys, logo_src)


# Show footer
st.markdown("""
<div style='text-align:center; padding:20px 0 10px;
            font-size:11px; color:#c0a080;
            border-top:0.5px solid #f0d0b8;
            margin-top:40px;'>
    © 2026 Mitma Consulting · Mitma Offboarding App Demo Version 0 ·
    Built by Mithirendra Maniam
</div>
""", unsafe_allow_html=True)