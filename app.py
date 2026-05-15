# ── app.py ────────────────────────────────────────────────────
# Mitma Offboarding App — Ver 0
# Public demo — no login required.
# ─────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
from datetime import datetime

from views.employee import show_employee_view
from views.manager  import show_manager_view
from views.hr       import show_hr_view

# ── Page configuration ────────────────────────────────────────
st.set_page_config(
    page_title="Mitma Offboarding App",
    page_icon="🚪",
    layout="wide"
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

# ── Header ────────────────────────────────────────────────────
st.markdown("## 🚪 Mitma Offboarding App")
st.markdown("---")

# ── View switcher in sidebar ──────────────────────────────────
# Top of sidebar — controls which view loads.
# Each view then adds its own sidebar content below this.
with st.sidebar:
    st.markdown("### View")
    selected_view = st.radio(
        "Select view",
        options=["👤 Employee", "👔 Manager", "🏢 HR"],
        label_visibility="collapsed"
    )
    st.markdown("---")

# ── Render selected view ──────────────────────────────────────
if selected_view == "👤 Employee":
    show_employee_view(employees, tasks_master, task_completion, knowledge, exit_surveys)

elif selected_view == "👔 Manager":
    show_manager_view(employees, tasks_master, task_completion, knowledge, exit_surveys)

elif selected_view == "🏢 HR":
    st.markdown("### 🏢 HR View")
    st.info("Coming soon.")


# Show footer
st.markdown("""
<div style='text-align:center; padding:20px 0 10px;
            font-size:11px; color:#c0a080;
            border-top:0.5px solid #f0d0b8;
            margin-top:40px;'>
    © 2026 Mitma Consulting · Mitma Offboarding App Version 0·
    Built by Mithirendra Maniam
</div>
""", unsafe_allow_html=True)