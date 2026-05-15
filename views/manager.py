# ── views/manager.py ──────────────────────────────────────────
# Mitma Offboarding App
# Manager view — oversight and handover management.
# Called by app.py via show_manager_view()
# ─────────────────────────────────────────────────────────────

import streamlit as st
from datetime import datetime, timedelta


def show_manager_view(employees, tasks_master, task_completion, knowledge, exit_surveys):

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 👔 Manager View")
        st.markdown("---")

        # Get unique managers from active employees only
        active_employees = employees[employees["status"] == "Active"]
        manager_names    = sorted(active_employees["manager"].unique().tolist())

        selected_manager = st.selectbox(
            "Select manager",
            options=manager_names,
            key="mgr_selector"
        )

        # Get all active leavers under this manager
        mgr_team = active_employees[active_employees["manager"] == selected_manager]

        st.markdown("---")
        st.markdown(f"**Active leavers:** {len(mgr_team)}")

        if mgr_team.empty:
            st.info("No active leavers in your team.")
            return

        # Select which team member to view
        selected_leaver = st.selectbox(
            "Select team member",
            options=mgr_team["name"].tolist(),
            key="mgr_leaver_selector"
        )

        # ── Section navigation ────────────────────────────────
        st.markdown("---")
        st.markdown("### 📍 Manager Sections")

        if "mgr_section" not in st.session_state:
            st.session_state.mgr_section = "1. Overview"

        mgr_sections = [
            "1. Overview",
            "2. Offboarding Checklist",
            "3. Knowledge Transfer",
            "4. Handover Plan",
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

    # ── Get selected leaver record ─────────────────────────────
    # All sections below use this employee record
    mgr_emp     = mgr_team[mgr_team["name"] == selected_leaver].iloc[0]
    resign_date = datetime.strptime(mgr_emp["resignation_date"], "%Y-%m-%d")
    last_day    = datetime.strptime(mgr_emp["last_day"], "%Y-%m-%d")
    days_left   = (last_day - datetime.today()).days

    # ── Reset to section 1 when leaver changes ────────────────
    if st.session_state.get("last_selected_leaver") != selected_leaver:
        st.session_state.mgr_section          = "1. Overview"
        st.session_state.last_selected_leaver = selected_leaver
        st.rerun()

    # ── Main page header ──────────────────────────────────────
    st.markdown(f"### 👔 Managing Exit For Employee — {mgr_emp['name']}")
    st.markdown(
        f"**Role:** {mgr_emp['role']} &nbsp;|&nbsp; "
        f"**Department:** {mgr_emp['department']} &nbsp;|&nbsp; "
        f"**Last day:** {mgr_emp['last_day']} &nbsp;|&nbsp; "
        f"**Days remaining:** {days_left} days",
        unsafe_allow_html=True
    )
    st.markdown("---")

   # ═════════════════════════════════════════════════════════
    # SECTION 1 — OVERVIEW
    # ═════════════════════════════════════════════════════════
    if st.session_state.mgr_section == "1. Overview":
        st.markdown("### SECTION 1. OVERVIEW")

        # ── Key metrics ───────────────────────────────────────
        # Summary of this leaver's offboarding progress at a glance
        emp_task_completion = task_completion[
            task_completion["employee_id"] == mgr_emp["employee_id"]
        ]
        total_tasks     = len(emp_task_completion)
        completed_tasks = len(emp_task_completion[emp_task_completion["status"] == "Complete"])
        pending_tasks   = total_tasks - completed_tasks
        progress_pct    = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Days Remaining", f"{days_left} days")
        with col2:
            st.metric("Tasks Completed", f"{completed_tasks} of {total_tasks}")
        with col3:
            st.metric("Tasks Pending", pending_tasks)
        with col4:
            st.metric("Overall Progress", f"{progress_pct}%")

        # Overall progress bar
        st.progress(progress_pct / 100, text=f"{progress_pct}% complete")
        st.markdown(" ")

        # ── Journey status ────────────────────────────────────
        # Shows which stage of the offboarding this employee is in
        st.markdown("#### Current Stage")

        journey_stages = [
            {"stage": "Resignation Accepted",       "tasks": []},
            {"stage": "Knowledge Transfer",          "tasks": ["T001", "T002", "T003"]},
            {"stage": "Exit Interview & Documents",  "tasks": ["T007", "T008"]},
            {"stage": "Asset Return",                "tasks": ["T004", "T005", "T006"]},
            {"stage": "Farewell & Departure",        "tasks": ["T009"]},
        ]

        completed_task_ids = emp_task_completion[
            emp_task_completion["status"] == "Complete"
        ]["task_id"].tolist()

        for i, stage in enumerate(journey_stages):
            if not stage["tasks"]:
                stage_status = "complete"
            elif all(t in completed_task_ids for t in stage["tasks"]):
                stage_status = "complete"
            elif any(t in completed_task_ids for t in stage["tasks"]):
                stage_status = "active"
            else:
                stage_status = "upcoming"

            status_badge = {
                "complete": '<span class="status-complete">✅ Complete</span>',
                "active":   '<span class="status-inprogress">🔄 In Progress</span>',
                "upcoming": '<span class="status-pending">⏳ Upcoming</span>'
            }[stage_status]

            st.markdown(
                f"**Stage {i+1}: {stage['stage']}** &nbsp;|&nbsp; {status_badge}",
                unsafe_allow_html=True
            )

        # ── Alerts ────────────────────────────────────────────
        # Flags anything the manager needs to action urgently
        st.markdown(" ")
        st.markdown("#### ⚠️ Alerts")

        alerts = []

        # Flag if days remaining is low and tasks are still pending
        if days_left <= 7 and pending_tasks > 0:
            alerts.append(f"🔴 {pending_tasks} tasks still pending with {days_left} days remaining.")

        # Flag if knowledge transfer is not complete
        kt_docs    = knowledge[knowledge["employee_id"] == mgr_emp["employee_id"]]
        kt_pending = len(kt_docs[kt_docs["status"].isin(["Pending", "In Progress"])])
        if kt_pending > 0:
            alerts.append(f"🟠 {kt_pending} knowledge transfer documents not yet signed off.")

        # Flag if access revocation task is not complete
        access_task = task_completion[
            (task_completion["employee_id"] == mgr_emp["employee_id"]) &
            (task_completion["task_id"] == "T010")
        ]
        if access_task.empty or access_task.iloc[0]["status"] != "Complete":
            alerts.append("🔴 IT access revocation request not yet submitted.")

        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ No urgent actions required.")
    
    # ═════════════════════════════════════════════════════════
    # SECTION 2 — OFFBOARDING CHECKLIST
    # ═════════════════════════════════════════════════════════
    if st.session_state.mgr_section == "2. Offboarding Checklist":
        st.markdown("### SECTION 2. OFFBOARDING CHECKLIST")

        # Get all manager tasks from the master list
        mgr_tasks = tasks_master[tasks_master["assigned_to"] == "Manager"]

        # Get completion status for this employee
        mgr_task_completion = task_completion[
            task_completion["employee_id"] == mgr_emp["employee_id"]
        ]

        # Merge task details with completion status
        checklist = mgr_tasks.merge(
            mgr_task_completion[["task_id", "status", "completion_date"]],
            on="task_id",
            how="left"
        )
        checklist["status"] = checklist["status"].fillna("Pending")

        # ── Summary metrics ───────────────────────────────────
        total    = len(checklist)
        complete = len(checklist[checklist["status"] == "Complete"])
        pending  = total - complete

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", total)
        with col2:
            st.metric("Completed", complete)
        with col3:
            st.metric("Pending", pending)

        # Progress bar
        progress = complete / total if total > 0 else 0
        st.progress(progress, text=f"{int(progress * 100)}% complete")
        st.markdown(" ")

        # ── Checklist by category ─────────────────────────────
        # Group tasks by category so manager can see them clearly
        categories = checklist["category"].unique().tolist()

        for category in categories:
            st.markdown(f"**{category}**")

            cat_tasks = checklist[checklist["category"] == category]

            for _, task in cat_tasks.iterrows():
                done     = task["status"] == "Complete"
                icon     = "✅" if done else "⬜"
                date_str = f" — Done {task['completion_date']}" if done and task["completion_date"] else ""

                st.markdown(
                    f"{icon} {task['description']}{date_str}"
                )

            st.markdown(" ")
    
    # ═════════════════════════════════════════════════════════
    # SECTION 3 — KNOWLEDGE TRANSFER
    # ═════════════════════════════════════════════════════════
    if st.session_state.mgr_section == "3. Knowledge Transfer":
        st.markdown("### SECTION 3. KNOWLEDGE TRANSFER")

        # Get knowledge transfer documents for this employee
        mgr_kt = knowledge[knowledge["employee_id"] == mgr_emp["employee_id"]]

        if mgr_kt.empty:
            st.info("No knowledge transfer documents assigned yet.")
        else:
            # ── Summary metrics ───────────────────────────────
            total_docs  = len(mgr_kt)
            signed_off  = len(mgr_kt[mgr_kt["status"] == "Signed off"])
            submitted   = len(mgr_kt[mgr_kt["status"] == "Submitted"])
            in_progress = len(mgr_kt[mgr_kt["status"] == "In Progress"])
            pending     = len(mgr_kt[mgr_kt["status"] == "Pending"])

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Documents", total_docs)
            with col2:
                st.metric("Signed Off", signed_off)
            with col3:
                st.metric("Submitted", submitted)
            with col4:
                st.metric("Pending", pending)

            # Status badge
            kt_status = "complete" if signed_off == total_docs else "active" if submitted > 0 or in_progress > 0 else "upcoming"
            kt_badge = {
                "complete": '<span class="status-complete">✅ Complete</span>',
                "active":   '<span class="status-inprogress">🔄 In Progress</span>',
                "upcoming": '<span class="status-pending">⏳ Upcoming</span>'
            }[kt_status]
            st.markdown(kt_badge, unsafe_allow_html=True)

            # Progress bar
            progress = (signed_off + submitted) / total_docs if total_docs > 0 else 0
            st.progress(progress, text=f"{int(progress * 100)}% submitted or signed off")
            st.markdown(" ")

            # ── Document list ─────────────────────────────────
            # Manager can see each document and sign off status
            st.markdown("#### Documents to Review and Sign Off")

            for _, doc in mgr_kt.iterrows():
                status_icon = {
                    "Signed off":  "✅",
                    "Submitted":   "📨",
                    "In Progress": "🔄",
                    "Pending":     "⬜"
                }.get(doc["status"], "⬜")

                st.markdown(
                    f"{status_icon} **{doc['document_title']}** "
                    f"&nbsp;|&nbsp; Status: {doc['status']} "
                    f"&nbsp;|&nbsp; From: {doc['employee_name']}",
                    unsafe_allow_html=True
                )

            st.markdown(" ")

            # ── Manager action ────────────────────────────────
            # Reminder to the manager to sign off pending documents
            if signed_off < total_docs:
                st.warning(
                    f"{total_docs - signed_off} document(s) still need your sign off. "
                    f"Review and confirm with {mgr_emp['name']} before their last day."
                )
            else:
                st.success("All knowledge transfer documents signed off.")
    
    # ═════════════════════════════════════════════════════════
    # SECTION 4 — HANDOVER PLAN
    # ═════════════════════════════════════════════════════════
    if st.session_state.mgr_section == "4. Handover Plan":
        st.markdown("### SECTION 4. HANDOVER PLAN")

        # ── Replacement planning ──────────────────────────────
        # Tracks whether a replacement has been triggered
        st.markdown("#### 🔄 Replacement Planning")

        if "replacement_triggered" not in st.session_state:
            st.session_state.replacement_triggered = False

        if st.session_state.replacement_triggered:
            st.success("✅ Replacement hiring workflow triggered. HR has been notified.")
        else:
            st.warning("Replacement hiring has not been triggered yet.")
            if st.button("🚀 Trigger Replacement Hiring Workflow"):
                st.session_state.replacement_triggered = True
                st.rerun()

        st.markdown(" ")

        # ── Responsibility handover ───────────────────────────
        # Who takes over each of the departing employee's responsibilities
        st.markdown("#### 👥 Responsibility Handover")
        st.markdown(
            f"Define who takes over **{mgr_emp['name']}'s** responsibilities "
            f"after their last day on **{mgr_emp['last_day']}**."
        )

        # Synthetic handover responsibilities — role based
        handover_items = [
            {"responsibility": "Day to day team coordination",     "handover_to": "TBD", "status": "⬜ Not assigned"},
            {"responsibility": "Stakeholder communications",        "handover_to": "TBD", "status": "⬜ Not assigned"},
            {"responsibility": "Ongoing project oversight",         "handover_to": "TBD", "status": "⬜ Not assigned"},
            {"responsibility": "Client or vendor relationships",    "handover_to": "TBD", "status": "⬜ Not assigned"},
            {"responsibility": "Reporting and performance reviews", "handover_to": "TBD", "status": "⬜ Not assigned"},
        ]

        for item in handover_items:
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**{item['responsibility']}**")
            with col2:
                st.markdown(f"Handover to: {item['handover_to']}")
            with col3:
                st.markdown(item["status"])

        st.markdown(" ")
        st.caption("Handover assignments will be editable in the full build.")

        # ── Team communication ────────────────────────────────
        # Reminds manager to communicate the departure to the team
        st.markdown("---")
        st.markdown("#### 📢 Team Communication")

        if "team_notified" not in st.session_state:
            st.session_state.team_notified = False

        if st.session_state.team_notified:
            st.success(f"✅ Team has been notified of {mgr_emp['name']}'s departure.")
        else:
            st.warning("Your team has not been notified of this departure yet.")
            st.markdown(
                "It is important to communicate the departure clearly and respectfully. "
                "Let your team know the last day, what changes to expect, and who to contact."
            )
            if st.button("✅ Mark Team as Notified"):
                st.session_state.team_notified = True
                st.rerun()

        # ── Exit interview ────────────────────────────────────
        # Reminds manager to schedule and complete the exit interview
        st.markdown("---")
        st.markdown("#### 🗣️ Exit Interview")

        if "exit_interview_done" not in st.session_state:
            st.session_state.exit_interview_done = False

        if st.session_state.exit_interview_done:
            st.success("✅ Exit interview completed and notes submitted to HR.")
        else:
            st.warning("Exit interview has not been completed yet.")
            st.markdown(
                "Schedule the exit interview in the final week. "
                "Submit your notes to HR after the session."
            )
            if st.button("✅ Mark Exit Interview as Complete"):
                st.session_state.exit_interview_done = True
                st.rerun()