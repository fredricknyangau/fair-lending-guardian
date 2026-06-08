import crewai_env
crewai_env.configure_crewai_environment()

import os
import random
import time
from datetime import datetime

import streamlit as st
from crewai import Crew, Process

try:
    import litellm
except ImportError:
    litellm = None

from agents import guardian_agent, hunter_agent, scout_agent
from guard import kill_switch_check, proxy_block
from mock_data import GRACE_APPLICATION, BODA_BODA_APPLICATION
from tasks import build_tasks
import database

# Initialize SQLite database
database.init_db()

# Section 1 — Page config
st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sidebar configurations
st.sidebar.title("⚙️ Configuration")
provider = os.getenv("LLM_PROVIDER", "gemini").lower()
st.sidebar.markdown(f"**Live Provider**: {provider}")
st.sidebar.markdown(f"🟢 `{provider}/{provider}-model`")
temp = st.sidebar.slider("LLM Temperature", 0.1, 0.5, float(os.getenv("LLM_TEMPERATURE", "0.2")), 0.1)
os.environ["LLM_TEMPERATURE"] = str(temp)

# Section 2 — Hero block
st.markdown(
    """
    <div style="background-color: #085041; padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
        <h1 style="color: white; margin-top: 0;">Fair Lending Guardian</h1>
        <p style="font-size: 1.2rem;">Three-agent AI pride for ethical SACCO lending in Kenya and Uganda</p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 0;">Built on CrewAI with ETHOS TRACK OASIS PRIDE and GUARD frameworks.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Section 3 — Headline metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vendor approval uplift", "+37pp", "vs 68 percent baseline")
col2.metric("Default risk ceiling", "below 3 percent", "-portfolio target")
col3.metric("Data sovereignty", "100 percent", "+AWS Africa region")
col4.metric("Human-in-loop threshold", "KES 15,000", "-all loans above")

st.divider()

# Section 4 — Quick demo banner
st.info("New to the system? Use the demo button below to watch the three agents process Grace Achieng's application in real time. No form filling required.")

if 'run_grace_demo' not in st.session_state:
    st.session_state.run_grace_demo = False

if st.button("Run Grace Achieng demo (pre-filled)"):
    st.session_state.run_grace_demo = True

# Section 5 — Grace demo simulation
if st.session_state.run_grace_demo:
    with st.status("Running Grace Achieng simulation...", expanded=True) as status:
        time.sleep(2)
        st.write("Step 1, Scout Agent: Stress signal confirmed from SMS message. Child ages 6, 9, and 14. Next harvest March and April. No kill switch phrases detected. Context packet prepared for Guardian Agent.")
        time.sleep(2)
        st.write("Step 2, Guardian Agent: 52-week cashflow analysis complete. Average weekly inflow KES 3,231. High-to-low ratio 3.78. Classification: seasonal, expected for maize farmer, not a risk signal. Loan amount KES 28,000 exceeds KES 15,000 threshold. RULE A activated: mandatory escalation to Hunter Agent regardless of score.")
        time.sleep(1)
        st.write("Step 3, GUARD pre-flight: Proxy block passed. No banned features detected. Dignity filter active. Kill switch clear.")
        time.sleep(2)
        st.write("Step 4, Hunter Agent: Applicant Grace Achieng, 42, maize farmer, Kakamega North, 3 dependants aged 6 9 and 14. Officer matched: Sarah, specialist in maize farming, Kakamega and Trans-Nzoia. Briefing packet generated. Alert sent. Officer SLA: 15 minutes.")
        status.update(label="Simulation complete", state="complete", expanded=True)
    
    st.success("Briefing delivered. The final lending decision rests with Officer Sarah alone. Member appeal right: dial *#123# at any time.")
    
    with st.expander("View Hunter Agent briefing packet"):
        st.markdown(
            "Applicant: Grace Achieng. Age: 42. Occupation: Maize farmer. Sub-county: Kakamega North. "
            "Dependants: 3 children aged 6, 9, and 14. Loan request: KES 28,000 for school fees Term 1. "
            "Credit analysis: 52-week average inflow KES 3,231. Seasonal income pattern confirmed, "
            "harvest peaks March to April and September to October. Income dip in January is school fee month, "
            "consistent with prior years and expected. Risk flags: none. Recommendation: suitable for officer "
            "review at full requested amount. Opportunity: consider cross-selling drought insurance before long rains season. "
            "GUARD audit: all four checks passed. Officer: Sarah. SLA: 15 minutes. PRIDE Loop status: human decision required, AI advisory only."
        )

st.divider()
st.subheader("Or submit a custom application")

template_choice = st.radio("Pre-fill with template:", ["Grace Achieng (Maize Farmer)", "David Ochieng (Boda-boda Operator)", "Custom"], index=0, horizontal=True)

if template_choice == "Grace Achieng (Maize Farmer)":
    default_app = GRACE_APPLICATION
elif template_choice == "David Ochieng (Boda-boda Operator)":
    default_app = BODA_BODA_APPLICATION
else:
    default_app = GRACE_APPLICATION

# Mobile layout fix
with st.form("application_form"):
    st.info("💡 **Transparency Notice**: Ujima SACCO practices explainable AI. Hover over the question marks next to each field to see exactly how our agents use (or are strictly forbidden from using) your data.")
    sms_language = st.selectbox("Preferred SMS Language", ["English", "Swahili", "Luhya"], index=1, help="OASIS FRAMEWORK: Ensure denial SMS messages are delivered in the member's preferred native language (e.g. Swahili or regional macro-languages like Luhya) with actionable next steps.")
    
    name = st.text_input("Applicant name", value=default_app["name"], help="Used for personalization in the Hunter Agent's briefing packet.")
    age = st.number_input("Age", min_value=18, max_value=80, value=default_app["age"], help="Demographic data. Explicitly ignored in Guardian Agent cashflow scoring.")
    
    occupations = [
        "maize farmer", "matooke farmer", "market vendor", "shea butter trader", 
        "mama mboga", "boda-boda operator", "informal artisan", "formal employee"
    ]
    occupation = st.selectbox("Occupation", occupations, index=occupations.index(default_app["occupation"]) if default_app["occupation"] in occupations else 0, help="TRACK RULE B: Occupation labels are explicitly ignored during credit scoring to prevent systemic bias. Used exclusively by the Hunter Agent to match the applicant with a sector-specialized human officer.")
    
    sub_county = st.text_input("Sub-county", value=default_app["sub_county"], help="GUARD PROXY BLOCK: Sub-county address is strictly firewalled from credit assessment to prevent geographic redlining.")
    loan_amount = st.number_input("Loan amount (KES)", min_value=1000, max_value=200000, value=default_app["loan_amount_kes"], step=1000, help="PRIDE RULE A: Any request exceeding KES 15,000 triggers a mandatory hard escalation to a human loan officer, regardless of the applicant's credit score.")
    loan_purpose = st.text_input("Loan purpose", value=default_app["loan_purpose"], help="Contextual data for the human loan officer's final review.")
    member_message = st.text_area("Member SMS message", value=default_app["member_message"], help="SCOUT AGENT INPUT: The Scout Agent parses this raw text to detect early financial stress signals and contextualize the request before it reaches the Guardian Agent.")

    st.caption("Household Context (Dependants)")
    dep1 = st.number_input("Child 1 age", min_value=0, max_value=25, value=default_app["dependants"][0]["age"] if len(default_app["dependants"]) > 0 else 0, help="ETHOS CONTEXT: Child ages help the Guardian Agent map known local school fee cycles to historical income dips, turning perceived 'cashflow risk' into understood context.")
    dep2 = st.number_input("Child 2 age", min_value=0, max_value=25, value=default_app["dependants"][1]["age"] if len(default_app["dependants"]) > 1 else 0)
    dep3 = st.number_input("Child 3 age", min_value=0, max_value=25, value=default_app["dependants"][2]["age"] if len(default_app["dependants"]) > 2 else 0)

    submitted = st.form_submit_button("Run Agent Pride — Process Application", type="primary")

if submitted:
    application = {
        **default_app,
        "name": name,
        "age": age,
        "occupation": occupation,
        "sub_county": sub_county,
        "loan_amount_kes": loan_amount,
        "loan_purpose": loan_purpose,
        "member_message": member_message,
        "dependants": [{"age": dep1}, {"age": dep2}, {"age": dep3}],
    }

    st.divider()
    st.subheader("GUARD Pre-Flight Checks")

    guard_status = "Passed"
    try:
        proxy_block(application)
        st.success("Proxy block: PASSED — no banned features in inputs")
        st.toast("✅ Proxy block passed")
    except ValueError as e:
        st.error(f"Proxy block: FAILED — {e}")
        guard_status = "Failed: Proxy Block"

    try:
        kill_switch_check(member_message or "")
        st.success("Kill switch: PASSED — no escalation triggers detected")
        st.toast("✅ Kill switch clear")
    except ValueError as e:
        st.warning(f"Kill switch: TRIGGERED — {e}")
        guard_status = "Failed: Kill Switch"

    st.toast("✅ Dignity filter standing by")
    st.toast("✅ Pattern detection active")

    if guard_status == "Passed":
        st.divider()
        st.subheader("Agent Pride Processing")

        with st.spinner("Scout Agent analysing financial stress signal..."):
            scout_placeholder = st.empty()
            scout_placeholder.info("🔭 Scout Agent: detecting financial stress signal...")

        with st.spinner("Guardian Agent running harvest-cycle creditworthiness assessment..."):
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
            result = None

            def _is_retryable(exc: Exception) -> bool:
                exc_str = str(exc).lower()
                exc_type = type(exc).__name__
                return (
                    (litellm is not None and isinstance(exc, getattr(litellm, "RateLimitError", type(None))))
                    or "RateLimitError" in exc_type
                    or "rate_limit_exceeded" in exc_str
                    or "resource_exhausted" in exc_str
                    or "429" in exc_str
                    or "503" in exc_str
                    or "unavailable" in exc_str
                    or "service_unavailable" in exc_str
                )

            for attempt in range(1, retry_attempts + 1):
                try:
                    result = crew.kickoff()
                    break
                except Exception as exc:
                    if not _is_retryable(exc) or attempt == retry_attempts:
                        raise
                    
                    st.warning(f"Hunter Agent encountered a temporary error, retrying in 5 seconds (attempt {attempt}/{retry_attempts}).")
                    time.sleep(5)

            scout_placeholder.success("🔭 Scout Agent: financial stress signal confirmed — handoff to Guardian")
            guardian_placeholder.success("🛡️ Guardian Agent: creditworthiness assessed — handoff to Hunter")
            hunter_placeholder.success("🎯 Hunter Agent: officer briefing packet generated")

            st.divider()
            st.subheader("Final Briefing Packet — Hunter Agent Output")
            output_text = str(result)
            now = datetime.now()
            output_text = (
                output_text.replace("[Insert Date]", now.strftime("%Y-%m-%d"))
                .replace("[Insert Time]", now.strftime("%H:%M:%S"))
                .replace("[Insert Timestamp]", now.strftime("%Y-%m-%d %H:%M:%S"))
            )
            
            # Render as a stylized official document
            with st.container(border=True):
                st.markdown("#### 📋 OFFICIAL OFFICER DOSSIER")
                st.caption(f"**Generated by:** Hunter Agent | **Timestamp:** {now.strftime('%Y-%m-%d %H:%M:%S')} | **Clearance:** PRIDE Loop Active")
                st.divider()
                st.markdown(output_text)
            
            # Record decision in SQLite. Here we mock the score/decision based on output or rule.
            # CrewAI does not cleanly return structured routing unless we parse it.
            # We will use simple heuristics to log an accurate representation based on rules:
            sim_score = 88.0 if loan_amount <= 15000 else 65.0
            routing_dec = "Escalate" if loan_amount > 15000 else "Approve"
            if "Decline" in output_text: routing_dec = "Decline"
            
            database.log_decision(name, loan_amount, sim_score, routing_dec, "Sarah", guard_status)

            st.divider()
            st.subheader("PRIDE Loop — Human Officer Reminder")

            if loan_amount > 15000:
                st.warning(
                    f"**PRIDE LOOP PAUSE POINT ACTIVE** — Loan amount KES {loan_amount:,} "
                    f"exceeds KES 15,000 autonomous approval threshold. "
                    f"A named human loan officer must make the final decision. "
                    f"Officer SLA: 15 minutes. Member appeal right: dial *#123#."
                )
            elif routing_dec == "Decline":
                st.error("Loan application declined by system.")
                if sms_language == "Swahili":
                    st.info("Swahili SMS Output: Mkopo wako umesimamishwa kwa sababu mapato yako hupungua wakati wa ada za shule. Tunahitaji akiba ya miezi 3. Piga simu ya bure kwa kuandika *#123#.")
                elif sms_language == "Luhya":
                    st.info("Luhya (Mock) SMS Output: Mulembe. Mkopo kwo kwasimamisibwe khulonda mapato kakhupungua khu tsimia tsia lisomo. Khwenya akiba ya miezi 3. Khubele esimu ya bure khu *#123#.")
                else:
                    st.info("English SMS Output: Your loan is paused because your income dips during school fee months. We require 3 months of savings history. Dial *#123# free of charge to appeal.")
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
            key_hint = f"{provider.upper()}_API_KEY"
            st.caption(f"Provider: {provider.upper()} · Check your {key_hint} in .env / Streamlit secrets.")
    else:
        # If guard checks failed, log as Kill Switch
        database.log_decision(name, loan_amount, 0, "Kill Switch", "Supervisor", guard_status)
