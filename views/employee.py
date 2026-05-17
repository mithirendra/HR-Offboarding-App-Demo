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

    st.markdown("### 👤 EMPLOYEE VIEW - Offboarding Journey")

    st.markdown("---")

# Custom styled label above the selectbox
    st.markdown(
        '<p style="font-size:16px; font-weight:500; color:#000000; margin-bottom:4px;">'
        'Select employee to get personalised view</p>',
        unsafe_allow_html=True
    )

    selected_name = st.selectbox(
        "",  # empty label — shown via markdown above
        options=active_employees["name"].tolist(),
        key="emp_selector"
    )

    st.markdown("---")


    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 👤 EMPLOYEE VIEW")
        st.markdown("---")
        st.markdown("### 📍 EMPLOYEE SECTIONS")

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
    # Styled cards for key employee details
    hero_values = [
        {"icon": "👤", "title": "Name",           "desc": emp["name"]},
        {"icon": "🏢", "title": "Department",      "desc": emp["department"]},
        {"icon": "📅", "title": "Last Day",        "desc": emp["last_day"]},
        {"icon": "⏱",  "title": "Days Remaining",  "desc": f"{days_left} days"},
    ]
    
    st.markdown("")
    st.markdown("")
    st.markdown("")
    cols = st.columns(4)

    for col, value in zip(cols, hero_values):
        with col:
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #f0d9cc;
                    border-radius:12px;
                    padding:20px;
                    text-align:center;
                    height:100%;
                ">
                    <div style="font-weight:700;font-size:16px;color:#000000;
                                margin-bottom:8px;">{value['title']}</div>
                    <div style="font-size:24px;color:#9a8880;line-height:1.6;">
                        {value['desc']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Employee details ──────────────────────────────────────
    detail_values = [
        {"icon": "💼", "title": "Role",           "desc": emp["role"]},
        {"icon": "👔", "title": "Manager",         "desc": emp["manager"]},
        {"icon": "🚪", "title": "Departure Type",  "desc": emp["departure_type"]},
    ]

    cols = st.columns(3)

    for col, value in zip(cols, detail_values):
        with col:
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #f0d9cc;
                    border-radius:12px;
                    padding:20px;
                    text-align:center;
                    height:100%;
                ">
                    <div style="font-size:28px;margin-bottom:16px;">{value['icon']}</div>
                    <div style="font-weight:700;font-size:16px;color:#000000;
                                margin-bottom:8px;">{value['title']}</div>
                    <div style="font-size:24px;color:#9a8880;line-height:1.6;">
                        {value['desc']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(" ")

    st.markdown("---")

    # ═════════════════════════════════════════════════════════
    # SECTION 1 — YOUR OFFBOARDING JOURNEY
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "1. Your Offboarding Journey":
        # ── Goodbye message ───────────────────────────────────────
    # A personal farewell message from leadership.
    # Sets a warm, human tone for the offboarding journey.
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #f0d9cc;
                border-radius:12px;
                padding:32px 36px;
                margin-bottom:24px;
            ">
                <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                        color:#9a8880;margin-bottom:12px;">A message from leadership</p>
                <p style="font-size:22px;font-weight:700;color:#000000;
                        margin-bottom:16px;line-height:1.3;">
                    Thank you for everything, {emp['name'].split()[0]}.
                </p>
                <p style="font-size:14px;color:#505050;line-height:1.8;margin-bottom:20px;">
                    Every person who joins us leaves a mark — on the team, the culture, and the work 
                    we do together. Your time here has mattered, and we are grateful for the energy, 
                    dedication, and care you brought to your role every day.
                    <br><br>
                    As you move into your next chapter, know that you leave with our full support, 
                    our respect, and our very best wishes. The door is always open.
                </p>
                <p style="font-size:13px;font-weight:600;color:#f49052;">
                    Ir. Mithirendra Maniam
                    <br>
                    <span style="font-weight:400;color:#9a8880;font-size:12px;">
                        Founder and Chief Executive Officer · Mitma Consulting
                    </span>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("### SECTION 1. YOUR OFFBOARDING JOURNEY")

        with st.container(border=True):

            # Get this employee's completed task IDs
            emp_tasks = task_completion[
                (task_completion["employee_id"] == emp["employee_id"]) &
                (task_completion["status"] == "Complete")
            ]
            completed_task_ids = emp_tasks["task_id"].tolist()

            # Define journey stages and which tasks belong to each
            journey_stages = [
                {"stage": "Resignation Accepted",      "icon": "Stage 1", "tasks": [],                          "date": resign_date},
                {"stage": "Knowledge Transfer",         "icon": "Stage 2", "tasks": ["T001", "T002", "T003"],    "date": resign_date + timedelta(weeks=1)},
                {"stage": "Exit Interview & Documents", "icon": "Stage 3", "tasks": ["T007", "T008"],            "date": last_day - timedelta(days=3)},
                {"stage": "Asset Return",               "icon": "Stage 4", "tasks": ["T004", "T005", "T006"],    "date": last_day - timedelta(days=1)},
                {"stage": "Farewell & Departure",       "icon": "Stage 5", "tasks": ["T009"],                    "date": last_day},
            ]

            # ── Render each stage ─────────────────────────────
            for stage in journey_stages:

                if not stage["tasks"]:
                    stage_status = "complete"
                elif all(t in completed_task_ids for t in stage["tasks"]):
                    stage_status = "complete"
                elif any(t in completed_task_ids for t in stage["tasks"]):
                    stage_status = "active"
                else:
                    stage_status = "upcoming"

                # Colour coding per status
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

                if stage["icon"] in ["Stage 1", "Stage 5"]:
                    date_label = "On " + stage["date"].strftime("%d %b %Y")
                else:
                    date_label = "Before " + stage["date"].strftime("%d %b %Y")

                # Stage header card
                st.markdown(
                    f"""
                    <div style="
                        background:{bg_colour};
                        border-left:4px solid {border_colour};
                        border-radius:10px;
                        padding:12px 16px;
                        margin-bottom:8px;
                    ">
                        <div style="font-weight:600;font-size:14px;color:#000000;">
                            {stage['icon']}: {stage['stage']} &nbsp;|&nbsp; {date_label}
                        </div>
                        <div style="font-size:12px;font-weight:500;color:{badge_colour};margin-top:4px;">
                            {badge}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Tasks listed below the stage card
                if stage["tasks"]:
                    stage_tasks = tasks_master[tasks_master["task_id"].isin(stage["tasks"])]
                    for _, task in stage_tasks.iterrows():
                        done      = task["task_id"] in completed_task_ids
                        task_icon = "✅" if done else "⬜"
                        task_bg   = "#f9f9f9"

                        st.markdown(
                            f"""
                            <div style="
                                background:{task_bg};
                                border-radius:8px;
                                padding:8px 16px;
                                margin-bottom:6px;
                                margin-left:16px;
                                font-size:13px;
                                color:#505050;
                            ">
                                {task_icon} {task['description']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        f"""
                        <div style="
                            background:#f9f9f9;
                            border-radius:8px;
                            padding:8px 16px;
                            margin-bottom:6px;
                            margin-left:16px;
                            font-size:13px;
                            color:#505050;
                        ">
                            ✅ Initiated automatically on resignation date.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(" ")

            # ── Legend ────────────────────────────────────────
            st.markdown(
                "**Legend:**  "
                "✅ Complete &nbsp;&nbsp;|&nbsp;&nbsp;"
                "🔄 In Progress &nbsp;&nbsp;|&nbsp;&nbsp;"
                "⏳ Upcoming &nbsp;&nbsp;|&nbsp;&nbsp;"
                "⬜ Task pending",
                unsafe_allow_html=True
            )

            # ── Next section button ───────────────────────────
            col1, col2 = st.columns([6, 2])
            with col2:
                st.markdown(
                    """
                    <style>
                    #next_btn button {
                        background-color: #f49052 !important;
                        color: white !important;
                        border: none !important;
                        border-radius: 8px !important;
                        font-weight: 600 !important;
                    }
                    </style>
                    <div id="next_btn">
                    """,
                    unsafe_allow_html=True
                )
                if st.button("Next: Knowledge Transfer →", key="next_s1", use_container_width=True):
                    st.session_state.section = "2. Knowledge Transfer"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════
    # SECTION 2 — KNOWLEDGE TRANSFER
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "2. Knowledge Transfer":
        st.markdown("### SECTION 2. KNOWLEDGE TRANSFER")

        with st.container(border=True):
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

                kt_status = "complete" if signed_off == total_docs else "active" if submitted > 0 or signed_off > 0 else "upcoming"
                kt_badge = {
                    "complete": '<span class="status-complete">✅ Complete</span>',
                    "active":   '<span class="status-inprogress">🔄 In Progress</span>',
                    "upcoming": '<span class="status-pending">⏳ Upcoming</span>'
                }[kt_status]
                st.markdown(kt_badge, unsafe_allow_html=True)

                progress = (signed_off + submitted) / total_docs
                st.progress(progress, text=f"{int(progress * 100)}% submitted or signed off")
                st.markdown(" ")

                for _, doc in emp_kt.iterrows():
                    status_icon = {
                        "Signed off":  "✅",
                        "Submitted":   "📨",
                        "In Progress": "🔄",
                        "Pending":     "⬜"
                    }.get(doc["status"], "⬜")

                    bg_colour = {
                        "Signed off":  "#e8f5e9",
                        "Submitted":   "#fff3e0",
                        "In Progress": "#fff3e0",
                        "Pending":     "#fdecea"
                    }.get(doc["status"], "#f9f9f9")

                    border_colour = {
                        "Signed off":  "#2e7d32",
                        "Submitted":   "#e65100",
                        "In Progress": "#e65100",
                        "Pending":     "#c62828"
                    }.get(doc["status"], "#f0d9cc")

                    st.markdown(
                        f"""
                        <div style="
                            background:{bg_colour};
                            border-left:4px solid {border_colour};
                            border-radius:8px;
                            padding:10px 16px;
                            margin-bottom:6px;
                            font-size:15px;
                            color:#505050;
                        ">
                            {status_icon} <strong>{doc['document_title']}</strong>
                            &nbsp;|&nbsp; Handover to: {doc['handover_to']}
                            &nbsp;|&nbsp; Status: {doc['status']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # ── Next section button ───────────────────────────
            st.markdown(" ")
            col1, col2 = st.columns([6, 2])
            with col2:
                if st.button("Next: Asset Return →", key="next_s2", use_container_width=True):
                    st.session_state.section = "3. Asset Return"
                    st.rerun()

    # ═════════════════════════════════════════════════════════
    # SECTION 3 — ASSET RETURN
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "3. Asset Return":
        st.markdown("### SECTION 3. ASSET RETURN")

        with st.container(border=True):
            asset_tasks = tasks_master[tasks_master["category"] == "Asset Return"]
            emp_asset_completion = task_completion[
                (task_completion["employee_id"] == emp["employee_id"]) &
                (task_completion["task_id"].isin(asset_tasks["task_id"]))
            ]

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

            ar_status = "complete" if returned == total_assets else "active" if returned > 0 else "upcoming"
            ar_badge = {
                "complete": '<span class="status-complete">✅ Complete</span>',
                "active":   '<span class="status-inprogress">🔄 In Progress</span>',
                "upcoming": '<span class="status-pending">⏳ Upcoming</span>'
            }[ar_status]
            st.markdown(ar_badge, unsafe_allow_html=True)

            ar_progress = returned / total_assets if total_assets > 0 else 0
            st.progress(ar_progress, text=f"{int(ar_progress * 100)}% returned")
            st.markdown(" ")

            for _, asset in asset_status.iterrows():
                done          = asset["status"] == "Complete"
                icon          = "✅" if done else "⬜"
                date_str      = f"&nbsp;|&nbsp; Returned: {asset['completion_date']}" if done else ""
                bg_colour     = "#e8f5e9" if done else "#fdecea"
                border_colour = "#2e7d32" if done else "#c62828"

                st.markdown(
                    f"""
                    <div style="
                        background:{bg_colour};
                        border-left:4px solid {border_colour};
                        border-radius:8px;
                        padding:10px 16px;
                        margin-bottom:6px;
                        font-size:15px;
                        color:#505050;
                    ">
                        {icon} <strong>{asset['description']}</strong>
                        &nbsp;|&nbsp; Due: last day
                        {date_str}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ── Next section button ───────────────────────────
            st.markdown(" ")
            col1, col2 = st.columns([6, 2])
            with col2:
                if st.button("Next: Exit Survey →", key="next_s3", use_container_width=True):
                    st.session_state.section = "4. Exit Survey"
                    st.rerun()

    # ═════════════════════════════════════════════════════════
    # SECTION 4 — EXIT SURVEY
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "4. Exit Survey":
        st.markdown("### SECTION 4. EXIT SURVEY")

        with st.container(border=True):
            emp_survey = exit_surveys[exit_surveys["employee_id"] == emp["employee_id"]]

            if emp_survey.empty:
                st.warning("You have not completed your exit survey yet.")
                st.markdown(
                    "Your exit survey helps the company understand your experience. "
                    "It takes less than 5 minutes and your responses are confidential."
                )
                st.button("Start Exit Survey", disabled=True, key="start_survey")
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

                for _, row in emp_survey.iterrows():
                    stars = "⭐" * int(row["rating"])

                    if row["rating"] >= 4:
                        bg_colour     = "#e8f5e9"
                        border_colour = "#2e7d32"
                    elif row["rating"] == 3:
                        bg_colour     = "#fff3e0"
                        border_colour = "#e65100"
                    else:
                        bg_colour     = "#fdecea"
                        border_colour = "#c62828"

                    open_text_html = (
                        f'<div style="font-size:14px;color:#9a8880;margin-top:6px;">'
                        f'"{row["open_text"]}"</div>'
                        if row["open_text"] else ""
                    )

                    st.markdown(
                        f"""
                        <div style="
                            background:{bg_colour};
                            border-left:4px solid {border_colour};
                            border-radius:8px;
                            padding:10px 16px;
                            margin-bottom:8px;
                            font-size:15px;
                            color:#505050;
                        ">
                            <div style="font-weight:600;color:#000000;margin-bottom:4px;">
                                {row['question']}
                            </div>
                            <div>{stars} ({row['rating']} / 5)</div>
                            {open_text_html}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # ── Next section button ───────────────────────────
            st.markdown(" ")
            col1, col2 = st.columns([6, 2])
            with col2:
                if st.button("Next: Farewell & Departure →", key="next_s4", use_container_width=True):
                    st.session_state.section = "5. Farewell & Departure"
                    st.rerun()

    # ═════════════════════════════════════════════════════════
    # SECTION 5 — FAREWELL & DEPARTURE
    # ═════════════════════════════════════════════════════════
    if st.session_state.section == "5. Farewell & Departure":
        st.markdown("### SECTION 5. FAREWELL & DEPARTURE")

        with st.container(border=True):

            # ── Alumni network ────────────────────────────────
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
                    if st.button("✅ Join Alumni Network", key="alumni_btn"):
                        st.session_state.alumni_opted_in = True
                        st.rerun()
                with col2:
                    st.button("Skip for now", key="alumni_skip")

        # ── Farewell messages ─────────────────────────────────
        st.markdown(" ")
        with st.container(border=True):
            st.markdown("#### 💬 5b. Farewell Messages")
            st.markdown(f"Messages left for **{emp['name']}** by colleagues.")

            farewell_messages = [
                {"from": "James Okafor", "message": "It has been an absolute pleasure working with you. Wishing you all the best in your next chapter!"},
                {"from": "Priya Nair",   "message": "You brought so much energy and clarity to every project. You will be missed!"},
                {"from": "David Lim",    "message": "Thank you for everything you contributed. Good luck — stay in touch!"},
            ]

            for msg in farewell_messages:
                st.markdown(
                    f"""
                    <div style="
                        background:#fff3e0;
                        border-left:4px solid #f49052;
                        border-radius:8px;
                        padding:10px 16px;
                        margin-bottom:16px;
                        font-size:15px;
                        color:#505050;
                    ">
                        <strong>{msg['from']}</strong> &nbsp;|&nbsp; {msg['message']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ── Final documents ───────────────────────────────────
        st.markdown(" ")
        with st.container(border=True):
            st.markdown("#### 📄 5c. Final Documents")

            doc_items = [
                {"icon": "📝", "title": "Resignation acceptance letter", "desc": "Issued by HR"},
                {"icon": "💰", "title": "Final payslip details",         "desc": "Issued by Finance"},
                {"icon": "📋", "title": "Reference letter request",      "desc": "Request via your manager"},
            ]

            cols = st.columns(3)
            for col, item in zip(cols, doc_items):
                with col:
                    st.markdown(
                        f"""
                        <div style="
                            background:#ffffff;
                            border:1px solid #f0d9cc;
                            border-radius:12px;
                            padding:20px;
                            margin-bottom:16px;
                            text-align:center;
                        ">
                            <div style="font-size:28px;margin-bottom:12px;">{item['icon']}</div>
                            <div style="font-weight:700;font-size:15px;color:#000000;
                                        margin-bottom:8px;">{item['title']}</div>
                            <div style="font-size:13px;color:#9a8880;">{item['desc']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )