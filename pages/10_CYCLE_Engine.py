import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("CYCLE Engine: Self-Improvement Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("CSAT score", "4.3 out of 5.0", "+0.4")
col2.metric("Escalation rate", "18 percent", "-6 percent")
col3.metric("Average resolution time", "11 minutes", "-4 minutes")
col4.metric("Dignity filter blocks this week", "3", "-2")

st.info("Sunday 2AM EAT analysis complete. Top failure mode: 41 percent of escalated applications involved school fee timing mismatches with the harvest calendar. Course-correction proposed: integrate Kenya Ministry of Education term calendar into Scout Agent knowledge base. Loop Validation approval received via Slack on Monday 9 June 2026. Fix is now active.")

with st.expander("Capture"):
    st.write("CSAT score: 4.3 out of 5.0, up 0.4 from last week. Escalation rate: 18 percent, down 6 percent from last week. Average resolution time: 11 minutes, down 4 minutes from last week. Dignity filter blocks this week: 3, down 2 from last week.")

with st.expander("Yield Insights"):
    st.write("Top failure mode: 41 percent of escalated applications involved school fee timing mismatches with the harvest calendar.")

with st.expander("Course-Correct"):
    st.write("Fix proposed: integrate Kenya Ministry of Education term calendar into Scout Agent knowledge base.")

with st.expander("Loop Validation"):
    st.write("Loop Validation approval received via Slack on Monday 9 June 2026.")

with st.expander("Explain"):
    st.write("Fix deployed: Monday 9 June 2026 after Loop Validation Slack approval.")

st.subheader("GUARD function status")
guard_data = [
    {"Function": "proxy_block", "Trigger Condition": "gender ethnicity tribe religion sub_county_risk", "Last Fired": "never in current session"},
    {"Function": "kill_switch_check", "Trigger Condition": "loan shark debt collector lawyer court", "Last Fired": "never in current session"},
    {"Function": "dignity_filter", "Trigger Condition": "unreliable risky informal unverifiable unstable suspicious irregular", "Last Fired": "3 times this week, blocked"},
    {"Function": "unusual_pattern_check", "Trigger Condition": "approval rate drop greater than 30pp vs baseline", "Last Fired": "not triggered"},
]
st.dataframe(guard_data, use_container_width=True)

st.subheader("Open limitations tracker")
limitations_data = [
    {"Limitation": "M-Pesa inflow data is hardcoded (Grace mock)", "Priority": "High", "Status": "Connect to real M-Pesa statement parser"},
    {"Limitation": "52-week inflows are not fetched live", "Priority": "High", "Status": "Integrate Safaricom Open API or statement upload"},
    {"Limitation": "LLM_PROVIDER switching requires restart", "Priority": "Medium", "Status": "Done"},
    {"Limitation": "No persistent audit log of decisions", "Priority": "High", "Status": "Add SQLite/PostgreSQL decision log"},
    {"Limitation": "No multilingual SMS output", "Priority": "High", "Status": "Add Swahili and Dholuo output modes"},
    {"Limitation": "SASRA unusual_pattern_check raises ValueError as a stub, not a real alert", "Priority": "High", "Status": "Wire to real alerting channel (email/SMS gateway needed)"},
    {"Limitation": "LLM temperature is fixed at 0.2", "Priority": "Low", "Status": "Expose temperature as env var"},
    {"Limitation": "Gemini 503 transient errors on Hunter turn rely on CrewAI internal retry only", "Priority": "High", "Status": "Add explicit retry loop"},
]
st.dataframe(limitations_data, use_container_width=True)
