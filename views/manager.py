# ── views/manager.py ──────────────────────────────────────────
# Mitma Offboarding App
# Manager view — Section 1 unlocked, Sections 2-5 locked in Ver 0.
# Called by app.py via show_manager_view()
# ─────────────────────────────────────────────────────────────

import streamlit as st
from datetime import datetime, timedelta


def show_manager_view(employees, tasks_master, task_completion, knowledge, exit_surveys, logo_src):

    # ── Sidebar — sections only ───────────────────────────────
    with st.sidebar:
        st.markdown("### 👔 MANAGER VIEW")
        st.markdown("---")
        st.markdown("### 📍 MANAGER SECTIONS")

        if "mgr_section" not in st.session_state:
            st.session_state.mgr_section = "1. Overview"

        mgr_sections = [
            "1. Overview",
            "2. Offboarding Checklist",
            "3. Knowledge Transfer",
            "4. Handover Plan",
            "5. Team Dashboard",
        ]

        for s in mgr_sections:
            if st.session_state.mgr_section == s:
                st.markdown(
                    f'<div style="background-color:#f49052; color:white; '
                    f'padding:8px 12px; border-radius:8px; font-size:13px; '
                    f'font-weight:500; margin-bottom:6px;">▶ {s}</div>',
                    unsafe_allow_html=True
                )
            else:
                if st.button(s, key=f"mgr_nav_{s}", use_container_width=True):
                    st.session_state.mgr_section = s
                    st.rerun()

    # ── Main page header ──────────────────────────────────────
    st.markdown("### 👔 MANAGER VIEW — Offboarding Oversight")
    st.markdown(
        """
        <div style="
            background:#ffece1;
            border-left:4px solid #f49052;
            border-radius:6px;
            padding:10px 16px;
            font-size:13px;
            color:#505050;
            margin-bottom:24px;
        ">
        👀 <strong>Demo Preview</strong> · You are viewing a sample of the Manager view. 
        Some sections are available in the Full Version only.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Manager selector ──────────────────────────────────────
    active_employees = employees[employees["status"] == "Active"]
    manager_names    = sorted(active_employees["manager"].unique().tolist())

    st.markdown(
        '<p style="font-size:16px;font-weight:500;color:#000000;margin-bottom:4px;">Select manager to get personalised view</p>',
        unsafe_allow_html=True
    )
    selected_manager = st.selectbox(
        "",
        options=manager_names,
        key="mgr_selector",
        label_visibility="collapsed"
    )

    # ── Calculate team immediately after manager selected ─────
    mgr_team = active_employees[active_employees["manager"] == selected_manager]

    # ── Reset when manager changes ────────────────────────────
    if st.session_state.get("last_selected_manager") != selected_manager:
        st.session_state.mgr_section           = "1. Overview"
        st.session_state.last_selected_manager = selected_manager
        if "mgr_leaver_selector" in st.session_state:
            del st.session_state["mgr_leaver_selector"]
        st.rerun()

    if mgr_team.empty:
        st.info("No active leavers in this manager's team.")
        return

    st.markdown(f"**Active leavers:** {len(mgr_team)}")
    st.markdown(" ")

    # ── Leaver selector ───────────────────────────────────────
    st.markdown(
        '<p style="font-size:16px;font-weight:500;color:#000000;margin-bottom:4px;">Select team member</p>',
        unsafe_allow_html=True
    )
    
    leaver_options = mgr_team["name"].tolist()
    
    # Default to first leaver in the list when manager changes
    default_index = 0
    
    selected_leaver = st.selectbox(
        "",
        options=leaver_options,
        index=default_index,
        key=f"mgr_leaver_selector_{selected_manager}",
        label_visibility="collapsed"
    )

    # ── Reset when leaver changes ─────────────────────────────
    if st.session_state.get("last_selected_leaver") != selected_leaver:
        st.session_state.mgr_section          = "1. Overview"
        st.session_state.last_selected_leaver = selected_leaver
        st.rerun()

    st.markdown("---")

    # ── Get selected leaver record ────────────────────────────
    mgr_emp     = mgr_team[mgr_team["name"] == selected_leaver].iloc[0]
    resign_date = datetime.strptime(mgr_emp["resignation_date"], "%Y-%m-%d")
    last_day    = datetime.strptime(mgr_emp["last_day"], "%Y-%m-%d")
    days_left   = (last_day - datetime.today()).days

    # ── Employee header cards ─────────────────────────────────
    st.markdown(f"### Managing Exit For — {mgr_emp['name']}")

    header_values = [
        {"icon": "💼", "title": "Role",          "desc": mgr_emp["role"]},
        {"icon": "🏢", "title": "Department",     "desc": mgr_emp["department"]},
        {"icon": "📅", "title": "Last Day",       "desc": mgr_emp["last_day"]},
        {"icon": "⏱",  "title": "Days Remaining", "desc": f"{days_left} days"},
    ]

    cols = st.columns(4)
    for col, value in zip(cols, header_values):
        with col:
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #f0d9cc;
                    border-radius:12px;
                    padding:20px;
                    text-align:center;
                ">
                    <div style="font-size:28px;margin-bottom:12px;">{value['icon']}</div>
                    <div style="font-weight:700;font-size:16px;color:#000000;
                                margin-bottom:8px;">{value['title']}</div>
                    <div style="font-size:15px;color:#9a8880;">{value['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(" ")
    st.markdown("---")

    # ── Locked notice helper ──────────────────────────────────
    def show_locked(current_section):
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
                    The Manager view is only available in the Full Version of the Mitma Offboarding App.
                </div>
                <div style="font-size:15px;color:#505050;line-height:1.8;margin-bottom:16px;">
                    Contact Mitma Consulting to get access to the Full Version.
                </div>
                <a href="https://mitmaconsulting.framer.ai" target="_blank">
                    <img src="{logo_src}" height="48" alt="Mitma Consulting"/>
                </a>
                <div style="display:flex;justify-content:center;gap:12px;
                            flex-wrap:wrap;margin-top:24px;">
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

        # Next section button
        next_sections = {
            "2. Offboarding Checklist": "3. Knowledge Transfer",
            "3. Knowledge Transfer":    "4. Handover Plan",
            "4. Handover Plan":         "5. Team Dashboard",
            "5. Team Dashboard":        None
        }

        next_s = next_sections.get(current_section)
        if next_s:
            col1, col2 = st.columns([6, 2])
            with col2:
                if st.button(
                    f"Next: {next_s.split('. ')[1]} →",
                    key=f"mgr_next_{current_section}",
                    use_container_width=True
                ):
                    st.session_state.mgr_section = next_s
                    st.rerun()

    # ═════════════════════════════════════════════════════════
    # SECTION 1 — OVERVIEW (unlocked)
    # ═════════════════════════════════════════════════════════
    if st.session_state.mgr_section == "1. Overview":
        st.markdown("### SECTION 1. OVERVIEW")

        with st.container(border=True):

            emp_task_completion = task_completion[
                task_completion["employee_id"] == mgr_emp["employee_id"]
            ]
            total_tasks     = len(emp_task_completion)
            completed_tasks = len(emp_task_completion[emp_task_completion["status"] == "Complete"])
            pending_tasks   = total_tasks - completed_tasks
            progress_pct    = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

            # Days remaining colour
            if days_left <= 3:
                days_colour = "#c62828"
            elif days_left <= 7:
                days_colour = "#e65100"
            else:
                days_colour = "#2e7d32"

            st.markdown(
                f'<div style="background-color:{days_colour}; color:white; '
                f'padding:14px 20px; border-radius:12px; font-size:20px; '
                f'font-weight:600; margin-bottom:16px; display:inline-block;">'
                f'⏱ {days_left} days remaining — {mgr_emp["name"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown(" ")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall Progress",  f"{progress_pct}%")
            with col2:
                st.metric("Tasks Completed",   f"{completed_tasks} of {total_tasks}")
            with col3:
                st.metric("Tasks Pending",     pending_tasks)
            with col4:
                st.metric("Departure Type",    mgr_emp["departure_type"])

            st.progress(progress_pct / 100, text=f"{progress_pct}% complete")
            st.markdown(" ")

            # ── Stage status ──────────────────────────────────
            st.markdown("#### 📍 Journey Stage Status")

            completed_task_ids = emp_task_completion[
                emp_task_completion["status"] == "Complete"
            ]["task_id"].tolist()

            journey_stages = [
                {"stage": "Resignation Accepted",      "tasks": []},
                {"stage": "Knowledge Transfer",         "tasks": ["T001", "T002", "T003"]},
                {"stage": "Exit Interview & Documents", "tasks": ["T007", "T008"]},
                {"stage": "Asset Return",               "tasks": ["T004", "T005", "T006"]},
                {"stage": "Farewell & Departure",       "tasks": ["T009"]},
            ]

            for i, stage in enumerate(journey_stages):

                if not stage["tasks"]:
                    stage_status = "complete"
                elif all(t in completed_task_ids for t in stage["tasks"]):
                    stage_status = "complete"
                elif any(t in completed_task_ids for t in stage["tasks"]):
                    stage_status = "active"
                else:
                    stage_status = "upcoming"

                if stage_status == "complete":
                    bg_colour     = "#e8f5e9"
                    border_colour = "#2e7d32"
                    badge         = "✅ Complete"
                    badge_colour  = "#2e7d32"
                elif stage_status == "active":
                    bg_colour     = "#fff3e0"
                    border_colour = "#e65100"
                    badge         = "🔄 In Progress"
                    badge_colour  = "#e65100"
                else:
                    bg_colour     = "#fdecea"
                    border_colour = "#c62828"
                    badge         = "⏳ Upcoming"
                    badge_colour  = "#c62828"

                st.markdown(
                    f"""
                    <div style="
                        background:{bg_colour};
                        border-left:4px solid {border_colour};
                        border-radius:10px;
                        padding:12px 16px;
                        margin-bottom:8px;
                    ">
                        <div style="font-weight:600;font-size:15px;color:#000000;">
                            Stage {i+1}: {stage['stage']}
                        </div>
                        <div style="font-size:13px;font-weight:500;
                                    color:{badge_colour};margin-top:4px;">
                            {badge}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ── Alerts ────────────────────────────────────────
            st.markdown(" ")
            st.markdown("#### ⚠️ Pending Actions")

            alerts = []

            if days_left <= 7 and pending_tasks > 0:
                alerts.append(f"🔴 {pending_tasks} tasks still pending with only {days_left} days remaining.")

            kt_docs    = knowledge[knowledge["employee_id"] == mgr_emp["employee_id"]]
            kt_pending = len(kt_docs[kt_docs["status"].isin(["Pending", "In Progress"])])
            if kt_pending > 0:
                alerts.append(f"🟠 {kt_pending} knowledge transfer document(s) not yet signed off.")

            access_task = task_completion[
                (task_completion["employee_id"] == mgr_emp["employee_id"]) &
                (task_completion["task_id"] == "T010")
            ]
            if access_task.empty or access_task.iloc[0]["status"] != "Complete":
                alerts.append("🔴 IT access revocation request not yet submitted.")

            exit_task = task_completion[
                (task_completion["employee_id"] == mgr_emp["employee_id"]) &
                (task_completion["task_id"] == "T011")
            ]
            if exit_task.empty or exit_task.iloc[0]["status"] != "Complete":
                alerts.append("🟠 Exit interview notes not yet submitted to HR.")

            if not st.session_state.get("team_notified", False):
                alerts.append("🟠 Team has not been notified of this departure yet.")

            if alerts:
                for alert in alerts:
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
                            {alert}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.success("✅ No pending actions. Offboarding is on track.")

        # ── Next section button ───────────────────────────────
        st.markdown(" ")
        col1, col2 = st.columns([6, 2])
        with col2:
            if st.button("Next: Offboarding Checklist →", key="mgr_next_s1", use_container_width=True):
                st.session_state.mgr_section = "2. Offboarding Checklist"
                st.rerun()

    # ═════════════════════════════════════════════════════════
    # SECTIONS 2-5 — LOCKED
    # ═════════════════════════════════════════════════════════
    if st.session_state.mgr_section == "2. Offboarding Checklist":
        st.markdown(f"### SECTION 2. OFFBOARDING CHECKLIST — {mgr_emp['name']}")
        show_locked("2. Offboarding Checklist")

    if st.session_state.mgr_section == "3. Knowledge Transfer":
        st.markdown(f"### SECTION 3. KNOWLEDGE TRANSFER — {mgr_emp['name']}")
        show_locked("3. Knowledge Transfer")

    if st.session_state.mgr_section == "4. Handover Plan":
        st.markdown(f"### SECTION 4. HANDOVER PLAN — {mgr_emp['name']}")
        show_locked("4. Handover Plan")

    if st.session_state.mgr_section == "5. Team Dashboard":
        st.markdown(f"### SECTION 5. TEAM DASHBOARD — {mgr_emp['name']}")
        show_locked("5. Team Dashboard")