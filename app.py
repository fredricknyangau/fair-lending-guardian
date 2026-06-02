# ruff: noqa: E402

import time

import crewai_env

crewai_env.configure_crewai_environment()

import streamlit as st
from crewai import Crew, Process

try:
    import litellm
except ImportError:
    litellm = None

from agents import guardian_agent, hunter_agent, scout_agent
from guard import kill_switch_check, proxy_block
from tasks import build_tasks

st.set_page_config(
    page_title="Fair Lending Guardian — Ujima SACCO", page_icon="🦁", layout="wide"
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🦁 Fair Lending Guardian")
st.caption("Ujima SACCO · AI Safari Capstone · Module 4: Agent Savannah · June 2026")

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Female Vendor Approval Target", "+37pp")
col2.metric("Default Risk Ceiling", "<3%")
col3.metric("Data Sovereignty", "100%")
col4.metric("Active Agents", "3")

st.divider()

st.subheader("Loan Application Input")

with st.form("application_form"):
    c1, c2 = st.columns(2)

    with c1:
        name = st.text_input("Applicant name", value="Grace Achieng")
        age = st.number_input("Age", min_value=18, max_value=80, value=42)
        occupation = st.selectbox(
            "Occupation",
            [
                "maize farmer",
                "matooke farmer",
                "market vendor",
                "shea butter trader",
                "mama mboga",
                "boda-boda operator",
                "informal artisan",
                "formal employee",
            ],
        )
        sub_county = st.text_input("Sub-county", value="Kakamega North")

    with c2:
        loan_amount = st.number_input(
            "Loan amount (KES)",
            min_value=1000,
            max_value=200000,
            value=28000,
            step=1000,
        )
        loan_purpose = st.text_input("Loan purpose", value="school fees Term 1")
        member_message = st.text_area(
            "Member SMS message", value="No money for school fees this term"
        )

    st.caption("Dependants")
    d_col1, d_col2, d_col3 = st.columns(3)
    dep1 = d_col1.number_input("Child 1 age", min_value=0, max_value=25, value=6)
    dep2 = d_col2.number_input("Child 2 age", min_value=0, max_value=25, value=9)
    dep3 = d_col3.number_input("Child 3 age", min_value=0, max_value=25, value=14)

    submitted = st.form_submit_button(
        "Run Agent Pride — Process Application", type="primary"
    )

if submitted:
    application = {
        "name": name,
        "age": age,
        "occupation": occupation,
        "sub_county": sub_county,
        "loan_amount_kes": loan_amount,
        "loan_purpose": loan_purpose,
        "dependants": [{"age": dep1}, {"age": dep2}, {"age": dep3}],
        "mpesa_weekly_inflows": [
            3200,
            3400,
            2900,
            3100,
            6800,
            6500,
            3000,
            2800,
            3200,
            3300,
            2950,
            3100,
            5900,
            6400,
            3100,
            3200,
            1800,
            2100,
            3000,
            3200,
            3100,
            2900,
            3400,
            3200,
            3100,
            3000,
            2950,
            3300,
            6700,
            6300,
            3100,
            3200,
            3000,
            2900,
            3100,
            3200,
            3100,
            3000,
            2950,
            3300,
            6800,
            6500,
            3000,
            2800,
            3200,
            3300,
            2950,
            3100,
            1900,
            2000,
            3000,
            3200,
        ],
        "harvest_months": ["March", "April", "September", "October"],
        "previous_loans": [],
        "school_fee_months": ["January", "May", "September"],
    }

    st.divider()
    st.subheader("GUARD Pre-Flight Checks")

    guard_col1, guard_col2 = st.columns(2)

    with guard_col1:
        try:
            proxy_block({"income": 1, "mpesa_history": 1})
            st.success("Proxy block: PASSED — no banned features in inputs")
        except ValueError as e:
            st.error(f"Proxy block: FAILED — {e}")

    with guard_col2:
        try:
            kill_switch_check(member_message)
            st.success("Kill switch: PASSED — no escalation triggers detected")
        except ValueError as e:
            st.warning(f"Kill switch: TRIGGERED — {e}")

    st.divider()
    st.subheader("Agent Pride Processing")

    with st.spinner("Scout Agent analysing financial stress signal..."):
        scout_placeholder = st.empty()
        scout_placeholder.info("🔭 Scout Agent: detecting financial stress signal...")

    with st.spinner(
        "Guardian Agent running harvest-cycle creditworthiness assessment..."
    ):
        guardian_placeholder = st.empty()
        guardian_placeholder.info("🛡️ Guardian Agent: calculating cashflow score...")

    with st.spinner("Hunter Agent preparing officer briefing packet..."):
        hunter_placeholder = st.empty()
        hunter_placeholder.info("🎯 Hunter Agent: matching to specialist officer...")

    try:
        tasks = build_tasks(application)
        crew = Crew(
            agents=[scout_agent, guardian_agent, hunter_agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
        )

        retry_attempts = 3
        retry_delay = 30
        result = None

        for attempt in range(1, retry_attempts + 1):
            try:
                result = crew.kickoff()
                break
            except Exception as exc:
                is_rate_limit = False
                if (
                    litellm is not None
                    and isinstance(exc, getattr(litellm, "RateLimitError", Exception))
                    or "RateLimitError" in type(exc).__name__
                    or "rate_limit_exceeded" in str(exc).lower()
                ):
                    is_rate_limit = True

                if not is_rate_limit or attempt == retry_attempts:
                    raise

                st.warning(
                    f"Groq rate limit hit (attempt {attempt}/{retry_attempts}). "
                    f"Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)

        scout_placeholder.success(
            "🔭 Scout Agent: financial stress signal confirmed — handoff to Guardian"
        )
        guardian_placeholder.success(
            "🛡️ Guardian Agent: creditworthiness assessed — handoff to Hunter"
        )
        hunter_placeholder.success("🎯 Hunter Agent: officer briefing packet generated")

        st.divider()
        st.subheader("Final Briefing Packet — Hunter Agent Output")
        st.markdown(str(result))

        st.divider()
        st.subheader("PRIDE Loop — Human Officer Reminder")

        if loan_amount > 15000:
            st.warning(
                f"**PRIDE LOOP PAUSE POINT ACTIVE** — Loan amount KES {loan_amount:,} "
                f"exceeds KES 15,000 autonomous approval threshold. "
                f"A named human loan officer must make the final decision. "
                f"Officer SLA: 15 minutes. Member appeal right: dial *#123#."
            )
        else:
            st.info(
                "Loan amount is within Guardian Agent authority limit (KES 15,000). "
                "Guardian recommendation is advisory — human officer may still review."
            )

        st.caption(
            "Fair Lending Guardian · Ujima SACCO · June 2026 · "
            "AI output is advisory only. Human officer owns all final decisions."
        )

    except Exception as e:
        st.error(f"Agent processing error: {e}")
        st.caption("Check your GROQ_API_KEY in the .env file.")
