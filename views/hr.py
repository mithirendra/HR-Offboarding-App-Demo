# ── views/hr.py ───────────────────────────────────────────────
# Mitma Offboarding App
# HR view — Section 1 preview, all others locked in Ver 0.
# Called by app.py via show_hr_view()
# ─────────────────────────────────────────────────────────────

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime


def show_hr_view(employees, tasks_master, task_completion, knowledge, exit_surveys, logo_src):

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🏢 HR VIEW")
        st.markdown("---")
        st.markdown("### 📍 HR SECTIONS")

        if "hr_section" not in st.session_state:
            st.session_state.hr_section = "1. Dashboard"

        hr_sections = [
            "1. Dashboard",
            "2. Active Offboardings",
            "3. Compliance Tracker",
            "4. Knowledge Transfer",
            "5. Trends & Analytics",
            "6. Rehire Eligibility",
        ]

        for s in hr_sections:
            if st.session_state.hr_section == s:
                st.markdown(
                    f'<div style="background-color:#f49052; color:white; '
                    f'padding:8px 12px; border-radius:8px; font-size:13px; '
                    f'font-weight:500; margin-bottom:6px;">▶ {s}</div>',
                    unsafe_allow_html=True
                )
            else:
                if st.button(s, key=f"hr_nav_{s}", use_container_width=True):
                    st.session_state.hr_section = s
                    st.rerun()
        st.markdown("---")

        # ─────────────────────────────────────────────
        # Contact links
        # ─────────────────────────────────────────────
        st.markdown(
            f"""
            <div style="
                font-size:13px;
                color:#9a8880;
                text-align:center;
                margin-bottom:40px;
                line-height:1.6;
            ">
            This app is only a <strong>DEMO VERSION</strong> with limited view pages.
            <br><br>
            Contact Mitma Consulting to get access to the <strong>FULL VERSION</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("Contact Mitma Consulting →", "https://mitmaconsulting.framer.ai", use_container_width=True)

        st.markdown("---")


    # ── Pre-calculate shared metrics ──────────────────────────
    active_emp   = employees[employees["status"] == "Active"]
    all_emp      = employees.copy()
    total_active = len(active_emp)

    completion_rates = []
    for _, emp in active_emp.iterrows():
        emp_tasks       = task_completion[task_completion["employee_id"] == emp["employee_id"]]
        total_tasks     = len(emp_tasks)
        completed_tasks = len(emp_tasks[emp_tasks["status"] == "Complete"])
        progress_pct    = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
        last_day        = datetime.strptime(emp["last_day"], "%Y-%m-%d")
        days_left       = (last_day - datetime.today()).days
        at_risk         = days_left <= 7 and progress_pct < 70

        completion_rates.append({
            "employee_id":    emp["employee_id"],
            "name":           emp["name"],
            "department":     emp["department"],
            "manager":        emp["manager"],
            "last_day":       emp["last_day"],
            "departure_type": emp["departure_type"],
            "days_left":      days_left,
            "progress":       progress_pct,
            "at_risk":        at_risk
        })

    completion_df  = pd.DataFrame(completion_rates)
    avg_completion = int(completion_df["progress"].mean()) if not completion_df.empty else 0
    at_risk_count  = len(completion_df[completion_df["at_risk"] == True])

    # ── Main page header ──────────────────────────────────────
    st.markdown("### 🏢 HR VIEW — Offboarding Overview")
    st.markdown("---")

    # ── Locked notice helper ──────────────────────────────────
    # Reused on every locked section
    def show_locked(current_section, logo_src):
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #f0d9cc;
                border-radius:12px;
                padding:40px 36px;
                text-align:center;
                margin-bottom:24px;
            ">
                <div style="font-size:48px;margin-bottom:16px;">🔒</div>
                <div style="font-size:22px;font-weight:700;color:#000000;margin-bottom:12px;">
                    Full Version Only
                </div>
                <div style="font-size:15px;color:#505050;line-height:1.8;margin-bottom:8px;">
                    The HR view is only available in the Full Version of the Mitma Offboarding App.
                </div>
                <div style="font-size:15px;color:#505050;line-height:1.8;margin-bottom:24px;">
                    Contact Mitma Consulting to get access to the Full Version.
                </div>
                <a href="https://mitmaconsulting.framer.ai" target="_blank">
                    <img src="{logo_src}" height="48" alt="Mitma Consulting"/>
                </a>
                <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:24px;">
                    <a href="https://mitmaconsulting.framer.ai/contact" target="_blank" style="
                        padding:10px 24px;
                        background:#f49052;
                        color:white;
                        border-radius:8px;
                        text-decoration:none;
                        font-size:13px;
                        font-weight:600;
                    ">Contact Mitma Consulting →</a>
                    <a href="https://www.linkedin.com/in/mithirendra-maniam/" target="_blank" style="
                        padding:10px 24px;
                        background:#f49052;
                        color:white;
                        border-radius:8px;
                        text-decoration:none;
                        font-size:13px;
                        font-weight:600;
                    ">Connect on LinkedIn →</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Next section button — only show if there is a next section
        next_sections = {
            "2. Active Offboardings": "3. Compliance Tracker",
            "3. Compliance Tracker":  "4. Knowledge Transfer",
            "4. Knowledge Transfer":  "5. Trends & Analytics",
            "5. Trends & Analytics":  "6. Rehire Eligibility",
            "6. Rehire Eligibility":  None
        }

        next_s = next_sections.get(current_section)
        if next_s:
            col1, col2 = st.columns([6, 2])
            with col2:
                if st.button(f"Next: {next_s.split('. ')[1]} →", key=f"hr_next_{current_section}", use_container_width=True):
                    st.session_state.hr_section = next_s
                    st.rerun()


    # ═════════════════════════════════════════════════════════
    # SECTION 1 — DASHBOARD (preview — unlocked)
    # ═════════════════════════════════════════════════════════
    if st.session_state.hr_section == "1. Dashboard":
        st.markdown("### SECTION 1. DASHBOARD")

        with st.container(border=True):

            # ── Top level metrics ─────────────────────────────
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Active Offboardings", total_active)
            with col2:
                st.metric("Avg Completion Rate", f"{avg_completion}%")
            with col3:
                st.metric("At Risk", at_risk_count)
            with col4:
                completed_total = len(employees[employees["status"] == "Completed"])
                st.metric("Completed This Period", completed_total)

            st.markdown(" ")
            st.progress(avg_completion / 100, text=f"Average offboarding completion — {avg_completion}%")
            st.markdown(" ")

            # ── At risk leavers ───────────────────────────────
            st.markdown("#### ⚠️ At Risk Leavers")
            at_risk_df = completion_df[completion_df["at_risk"] == True]

            if at_risk_df.empty:
                st.success("✅ No leavers currently at risk.")
            else:
                for _, row in at_risk_df.iterrows():
                    st.markdown(
                        f"""
                        <div style="
                            background:#fdecea;
                            border-left:4px solid #c62828;
                            border-radius:8px;
                            padding:10px 16px;
                            margin-bottom:6px;
                            font-size:15px;
                            color:#505050;
                        ">
                            🔴 <strong>{row['name']}</strong> — {row['department']} —
                            {row['days_left']} days left — {row['progress']}% complete
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.markdown("")
            st.markdown("")
            st.markdown("")

            # ── Completion by department ──────────────────────
            st.markdown("#### 📊 Completion Rate by Department")
            if not completion_df.empty:
                dept_completion = (
                    completion_df.groupby("department")["progress"]
                    .mean()
                    .round(0)
                    .reset_index()
                )
                dept_completion.columns = ["Department", "Avg Completion %"]

                fig = px.bar(
                    dept_completion,
                    x="Department",
                    y="Avg Completion %",
                    color="Avg Completion %",
                    color_continuous_scale=["#c62828", "#e65100", "#2e7d32"],
                    range_color=[0, 100],
                    text="Avg Completion %"
                )
                fig.update_layout(
                    plot_bgcolor="#fffbf8",
                    paper_bgcolor="#fffbf8",
                    showlegend=False,
                    coloraxis_showscale=False,
                    margin=dict(t=20, b=20)
                )
                fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("")
            st.markdown("")
            st.markdown("")
            
            # ── Departure type split ──────────────────────────
            st.markdown("#### 📊 Departure Type Split")
            departure_counts = (
                active_emp.groupby("departure_type")
                .size()
                .reset_index(name="count")
            )
            if not departure_counts.empty:
                fig2 = px.pie(
                    departure_counts,
                    names="departure_type",
                    values="count",
                    color_discrete_sequence=["#f49052", "#e65100", "#c62828"]
                )
                fig2.update_layout(
                    plot_bgcolor="#fffbf8",
                    paper_bgcolor="#fffbf8",
                    margin=dict(t=20, b=20)
                )
                st.plotly_chart(fig2, use_container_width=True)

        # ── Next section button ───────────────────────────────
        st.markdown(" ")
        col1, col2 = st.columns([6, 2])
        with col2:
            if st.button("Next: Active Offboardings →", key="hr_next_s1", use_container_width=True):
                st.session_state.hr_section = "2. Active Offboardings"
                st.rerun()

    # ═════════════════════════════════════════════════════════
    # SECTIONS 2-6 — LOCKED
    # ═════════════════════════════════════════════════════════
    if st.session_state.hr_section == "2. Active Offboardings":
        st.markdown("### SECTION 2. ACTIVE OFFBOARDINGS")
        show_locked("2. Active Offboardings", logo_src)

    if st.session_state.hr_section == "3. Compliance Tracker":
        st.markdown("### SECTION 3. COMPLIANCE TRACKER")
        show_locked("3. Compliance Tracker", logo_src)

    if st.session_state.hr_section == "4. Knowledge Transfer":
        st.markdown("### SECTION 4. KNOWLEDGE TRANSFER")
        show_locked("4. Knowledge Transfer", logo_src)

    if st.session_state.hr_section == "5. Trends & Analytics":
        st.markdown("### SECTION 5. TRENDS & ANALYTICS")
        show_locked("5. Trends & Analytics", logo_src)

    if st.session_state.hr_section == "6. Rehire Eligibility":
        st.markdown("### SECTION 6. REHIRE ELIGIBILITY")
        show_locked("6. Rehire Eligibility", logo_src)