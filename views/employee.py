# ── views/employee.py ─────────────────────────────────────────
# Mitma Offboarding App
# Employee view — all sections for the departing employee.
# Called by app.py via show_employee_view()
# ─────────────────────────────────────────────────────────────

import streamlit as st
from datetime import datetime, timedelta


def show_employee_view(employees, tasks_master, task_completion, knowledge, exit_surveys):

    # ── Filter to active employees ────────────────────────────
    active_employees = employees[employees["status"] == "Active"]

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 👤 Employee View")
        st.markdown("---")

        selected_name = st.selectbox(
            "Select employee",
            options=active_employees["name"].tolist(),
            key="emp_selector"
        )

        st.markdown("---")
        st.markdown("### 📍 Offboarding Sections")

        if "section" not in st.session_state:
            st.session_state.section = "1. Your Offboarding Journey"

        sections = [
            "1. Your Offboarding Journey",
            "2. Knowledge Transfer",
            "3. Asset Return",
            "4. Exit Survey",
            "5. Farewell & Departure"
        ]

        for s in sections:
            if st.session_state.section == s:
                st.markdown(
                    f'<div style="background-color:#f49052; color:white; '
                    f'padding:8px 12px; border-radius:8px; font-size:13px; '
                    f'font-weight:500; margin-bottom:6px;">▶ {s}</div>',
                    unsafe_allow_html=True
                )
            else:
                if st.button(s, key=f"nav_{s}", use_container_width=True):
                    st.session_state.section = s
                    st.rerun()

    # ── Get selected employee — used throughout all sections ──
    emp         = active_employees[active_employees["name"] == selected_name].iloc[0]
    resign_date = datetime.strptime(emp["resignation_date"], "%Y-%m-%d")
    last_day    = datetime.strptime(emp["last_day"], "%Y-%m-%d")
    days_left   = (last_day - datetime.today()).days

    # ── Reset to section 1 when employee changes ──────────────
    if st.session_state.get("last_selected") != selected_name:
        st.session_state.section       = "1. Your Offboarding Journey"
        st.session_state.last_selected = selected_name
        st.rerun()

    # ── Hero card ─────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Name", emp["name"])
    with col2:
        st.metric("Department", emp["department"])
    with col3:
        st.metric("Last Day", emp["last_day"])
    with col4:
        st.metric("Days Remaining", f"{days_left} days")

    st.markdown(
        f"**Role:** {emp['role']} &nbsp;|&nbsp; "
        f"**Manager:** {emp['manager']} &nbsp;|&nbsp; "
        f"**Departure type:** {emp['departure_type']}",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ═════════════════════════════════════════════════════════
    # SECTION 1 — YOUR OFFBOARDING JOURNEY
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "1. Your Offboarding Journey":
        st.markdown("### SECTION 1. YOUR OFFBOARDING JOURNEY")

        # Get this employee's completed task IDs
        emp_tasks = task_completion[
            (task_completion["employee_id"] == emp["employee_id"]) &
            (task_completion["status"] == "Complete")
        ]
        completed_task_ids = emp_tasks["task_id"].tolist()

        # Define journey stages and which tasks belong to each
        journey_stages = [
            {
                "stage": "Resignation Accepted",
                "icon":  "Stage 1",
                "tasks": [],
                "date":  resign_date
            },
            {
                "stage": "Knowledge Transfer",
                "icon":  "Stage 2",
                "tasks": ["T001", "T002", "T003"],
                "date":  resign_date + timedelta(weeks=1)
            },
            {
                "stage": "Exit Interview & Documents",
                "icon":  "Stage 3",
                "tasks": ["T007", "T008"],
                "date":  last_day - timedelta(days=3)
            },
            {
                "stage": "Asset Return",
                "icon":  "Stage 4",
                "tasks": ["T004", "T005", "T006"],
                "date":  last_day - timedelta(days=1)
            },
            {
                "stage": "Farewell & Departure",
                "icon":  "Stage 5",
                "tasks": ["T009"],
                "date":  last_day
            },
        ]

        # ── Render each stage ─────────────────────────────────
        for stage in journey_stages:

            # Work out stage status based on task completion
            if not stage["tasks"]:
                stage_status = "complete"
            elif all(t in completed_task_ids for t in stage["tasks"]):
                stage_status = "complete"
            elif any(t in completed_task_ids for t in stage["tasks"]):
                stage_status = "active"
            else:
                stage_status = "upcoming"

            # Colour coded HTML badge
            status_badge = {
                "complete": '<span class="status-complete">✅ Complete</span>',
                "active":   '<span class="status-inprogress">🔄 In Progress</span>',
                "upcoming": '<span class="status-pending">⏳ Upcoming</span>'
            }[stage_status]

            # Stage 1 and 5 show "On", all others show "Before"
            if stage["icon"] in ["Stage 1", "Stage 5"]:
                date_label = "On " + stage["date"].strftime("%d %b %Y")
            else:
                date_label = "Before " + stage["date"].strftime("%d %b %Y")

            # Status badge above the expander
            st.markdown(status_badge, unsafe_allow_html=True)

            # Stage as expander
            with st.expander(f"{stage['icon']}:  {stage['stage']}  |  {date_label}"):
                if not stage["tasks"]:
                    st.success("Initiated automatically on resignation date.")
                else:
                    stage_tasks = tasks_master[tasks_master["task_id"].isin(stage["tasks"])]
                    for _, task in stage_tasks.iterrows():
                        done = task["task_id"] in completed_task_ids
                        icon = "✅" if done else "⬜"
                        st.markdown(f"{icon} {task['description']}")

            st.markdown(" ")

        # ── Legend ────────────────────────────────────────────
        st.markdown(
            "**Legend:**  "
            "✅ Complete &nbsp;&nbsp;|&nbsp;&nbsp;"
            "🔄 In Progress &nbsp;&nbsp;|&nbsp;&nbsp;"
            "⏳ Upcoming &nbsp;&nbsp;|&nbsp;&nbsp;"
            "⬜ Task pending",
            unsafe_allow_html=True
        )

    # ═════════════════════════════════════════════════════════
    # SECTION 2 — KNOWLEDGE TRANSFER
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "2. Knowledge Transfer":
        st.markdown("### SECTION 2. KNOWLEDGE TRANSFER")

        emp_kt = knowledge[knowledge["employee_id"] == emp["employee_id"]]

        if emp_kt.empty:
            st.info("No knowledge transfer documents assigned yet.")
        else:
            total_docs = len(emp_kt)
            signed_off = len(emp_kt[emp_kt["status"] == "Signed off"])
            submitted  = len(emp_kt[emp_kt["status"] == "Submitted"])
            pending    = len(emp_kt[emp_kt["status"] == "Pending"])

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
            kt_status = "complete" if signed_off == total_docs else "active" if submitted > 0 or signed_off > 0 else "upcoming"
            kt_badge = {
                "complete": '<span class="status-complete">✅ Complete</span>',
                "active":   '<span class="status-inprogress">🔄 In Progress</span>',
                "upcoming": '<span class="status-pending">⏳ Upcoming</span>'
            }[kt_status]
            st.markdown(kt_badge, unsafe_allow_html=True)

            # Progress bar
            progress = (signed_off + submitted) / total_docs
            st.progress(progress, text=f"{int(progress * 100)}% submitted or signed off")
            st.markdown(" ")

            # Document list
            with st.expander("View documents"):
                for _, doc in emp_kt.iterrows():
                    status_icon = {
                        "Signed off":  "✅",
                        "Submitted":   "📨",
                        "In Progress": "🔄",
                        "Pending":     "⬜"
                    }.get(doc["status"], "⬜")

                    st.markdown(
                        f"{status_icon} **{doc['document_title']}** "
                        f"&nbsp;|&nbsp; Handover to: {doc['handover_to']} "
                        f"&nbsp;|&nbsp; Status: {doc['status']}",
                        unsafe_allow_html=True
                    )

    # ═════════════════════════════════════════════════════════
    # SECTION 3 — ASSET RETURN
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "3. Asset Return":
        st.markdown("### SECTION 3. ASSET RETURN")

        asset_tasks = tasks_master[tasks_master["category"] == "Asset Return"]
        emp_asset_completion = task_completion[
            (task_completion["employee_id"] == emp["employee_id"]) &
            (task_completion["task_id"].isin(asset_tasks["task_id"]))
        ]

        # Merge task details with completion status
        asset_status = asset_tasks.merge(
            emp_asset_completion[["task_id", "status", "completion_date"]],
            on="task_id",
            how="left"
        )
        asset_status["status"] = asset_status["status"].fillna("Pending")

        total_assets   = len(asset_status)
        returned       = len(asset_status[asset_status["status"] == "Complete"])
        pending_assets = total_assets - returned

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", total_assets)
        with col2:
            st.metric("Returned", returned)
        with col3:
            st.metric("Pending", pending_assets)

        st.markdown(" ")

        # Status badge
        ar_status = "complete" if returned == total_assets else "active" if returned > 0 else "upcoming"
        ar_badge = {
            "complete": '<span class="status-complete">✅ Complete</span>',
            "active":   '<span class="status-inprogress">🔄 In Progress</span>',
            "upcoming": '<span class="status-pending">⏳ Upcoming</span>'
        }[ar_status]
        st.markdown(ar_badge, unsafe_allow_html=True)

        # Progress bar
        ar_progress = returned / total_assets if total_assets > 0 else 0
        st.progress(ar_progress, text=f"{int(ar_progress * 100)}% returned")
        st.markdown(" ")

        # Asset list
        with st.expander("View assets"):
            for _, asset in asset_status.iterrows():
                done     = asset["status"] == "Complete"
                icon     = "✅" if done else "⬜"
                date_str = f"&nbsp;|&nbsp; Returned: {asset['completion_date']}" if done else ""

                st.markdown(
                    f"{icon} **{asset['description']}** "
                    f"&nbsp;|&nbsp; Due: last day "
                    f"{date_str}",
                    unsafe_allow_html=True
                )

    # ═════════════════════════════════════════════════════════
    # SECTION 4 — EXIT SURVEY
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "4. Exit Survey":
        st.markdown("### SECTION 4. EXIT SURVEY")

        emp_survey = exit_surveys[exit_surveys["employee_id"] == emp["employee_id"]]

        if emp_survey.empty:
            st.warning("You have not completed your exit survey yet.")
            st.markdown(
                "Your exit survey helps the company understand your experience. "
                "It takes less than 5 minutes and your responses are confidential."
            )
            st.button("Start Exit Survey", disabled=True)
            st.caption("Survey will be enabled in your final week.")
        else:
            st.success("Exit survey completed. Thank you.")

            avg_rating = emp_survey["rating"].mean()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Rating", f"{avg_rating:.1f} / 5")
            with col2:
                sentiment_row = emp_survey[emp_survey["sentiment"] != ""]
                if not sentiment_row.empty:
                    sentiment = sentiment_row.iloc[0]["sentiment"]
                    compound  = sentiment_row.iloc[0]["compound_score"]
                    st.metric("Overall Sentiment", f"{sentiment} ({compound})")

            st.markdown(" ")

            with st.expander("View survey responses"):
                for _, row in emp_survey.iterrows():
                    stars = "⭐" * int(row["rating"])
                    st.markdown(f"**{row['question']}**")
                    st.markdown(f"{stars} ({row['rating']} / 5)")
                    if row["open_text"]:
                        st.markdown(f"> *{row['open_text']}*")
                    st.markdown(" ")

    # ═════════════════════════════════════════════════════════
    # SECTION 5 — FAREWELL & DEPARTURE
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "5. Farewell & Departure":
        st.markdown("### SECTION 5. FAREWELL & DEPARTURE")

        # ── Alumni network ────────────────────────────────────
        st.markdown("#### 🌐 5a. Alumni Network")
        st.markdown(
            "Stay connected after you leave. The Mitma alumni network gives you access "
            "to a community of former colleagues, events, and opportunities."
        )

        if "alumni_opted_in" not in st.session_state:
            st.session_state.alumni_opted_in = False

        if st.session_state.alumni_opted_in:
            st.success("✅ You have opted in to the alumni network. We will be in touch.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Join Alumni Network"):
                    st.session_state.alumni_opted_in = True
                    st.rerun()
            with col2:
                st.button("Skip for now")

        # ── Farewell messages ─────────────────────────────────
        st.markdown("---")
        st.markdown("#### 💬 5b. Farewell Messages")
        st.markdown(f"Messages left for **{emp['name']}** by colleagues.")

        farewell_messages = [
            {"from": "James Okafor", "message": "It has been an absolute pleasure working with you. Wishing you all the best in your next chapter!"},
            {"from": "Priya Nair",   "message": "You brought so much energy and clarity to every project. You will be missed!"},
            {"from": "David Lim",    "message": "Thank you for everything you contributed. Good luck — stay in touch!"},
        ]

        for msg in farewell_messages:
            st.markdown(
                f"**{msg['from']}** &nbsp;|&nbsp; *{msg['message']}*",
                unsafe_allow_html=True
            )
            st.markdown(" ")

        # ── Final documents ───────────────────────────────────
        st.markdown("---")
        st.markdown("#### 📄 5c. Final Documents")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("📝 **Resignation acceptance letter**")
            st.caption("Issued by HR")
        with col2:
            st.markdown("💰 **Final payslip details**")
            st.caption("Issued by Finance")
        with col3:
            st.markdown("📋 **Reference letter request**")
            st.caption("Request via your manager")