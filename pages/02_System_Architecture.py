import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("System Architecture & Orchestration")
st.markdown("For the academic supervisor and competition judges: this outlines the multi-agent automation flow and regulatory firewalls underlying the application.")

st.divider()

# Level 1: Input & Safety
col1, col2 = st.columns([1, 3])
with col1:
    st.info("📱 **Member Input**\n\nRaw SMS Data & M-Pesa 52-week Inflows")
with col2:
    st.error("🛡️ **GUARD Layer (Pre-Flight)**\n\n1. **Proxy Block**: Rejects gender/sub-county/ethnicity.\n2. **Kill Switch**: Scans for 'loan shark'/'debt collector'.\n3. **Dignity Filter**: Blocks terms like 'unreliable'.\n4. **Pattern Check**: Drops >30% approval raise SASRA alert.")

st.markdown("<h3 style='text-align: center;'>⬇️</h3>", unsafe_allow_html=True)

# Level 2: Agents
c1, c2, c3 = st.columns(3)
with c1:
    st.success("🔭 **Scout Agent**\n\n**Role:** Financial Literacy Coach\n**Task:** Identify financial stress signals from SMS.\n**Output:** Handoff Context (Child ages, Harvest Dates)")
    with st.expander("View Agent Logic & Data"):
        st.markdown("""
        **Data Inputs Consumed:**
        - `member_message` (Raw SMS)
        - `dependants` (Ages)
        - `harvest_months`
        
        **Internal Rules (Prompt Instructions):**
        - Never recommends specific loan products.
        - Translates 'lack of money for school fees' into a recognized financial stress signal rather than immediate default risk.
        - **Kill Switch trigger:** Mentions of 'loan sharks', 'debt collectors' (forces immediate human escalation).
        """)

with c2:
    st.success("🛡️ **Guardian Agent**\n\n**Role:** Loan Triage Officer\n**Task:** 52-week Cashflow & Seasonal Alignment Analysis.\n**Output:** Credit Score (0-100) & Routing Decision")
    with st.expander("View Agent Logic & Data"):
        st.markdown("""
        **Data Inputs Consumed:**
        - `mpesa_weekly_inflows` (52-week array)
        - `loan_amount_kes`
        - `school_fee_months`
        - Scout Agent's Output Context
        
        **Internal Rules (Prompt Instructions):**
        - **Data Firewalled:** Explicitly forbidden from seeing `occupation`, `sub_county`, or `gender`.
        - **Cashflow Math:** Calculates average weekly inflow and high-to-low week ratios. Flags ratios > 3.0 as *normal* for farmers rather than 'high volatility'.
        - **PRIDE Rule:** Hard cap of KES 15,000 for autonomous approval. Over 15K requires Hunter handoff.
        """)

with c3:
    st.success("🎯 **Hunter Agent**\n\n**Role:** Human-in-Loop Coordinator\n**Task:** Match applicant to specific officer based on sub-county/crop expertise.\n**Output:** Officer Briefing Packet")
    with st.expander("View Agent Logic & Data"):
        st.markdown("""
        **Data Inputs Consumed:**
        - `occupation` (e.g., maize farmer)
        - `sub_county` (e.g., Kakamega North)
        - `loan_purpose`
        - Guardian Agent's Output Score & Context
        
        **Internal Rules (Prompt Instructions):**
        - **Safety Rule:** Strictly forbidden from approving or denying loans. Output is a briefing packet only.
        - **Matching:** Looks at the occupation and sub-county to route the ticket to a human officer with localized agricultural knowledge.
        - **Value Add:** Instructed to surface relevant cross-sell opportunities (e.g., drought insurance prior to long rains).
        """)

st.markdown("<h3 style='text-align: center;'>⬇️</h3>", unsafe_allow_html=True)

# Level 3: Output & Audit
c_out1, c_out2 = st.columns(2)
with c_out1:
    st.warning("🧑🏾‍💼 **Human PRIDE Loop**\n\nFinal decision authority rests with the matched human loan officer. The AI is advisory only. Max autonomous approval is KES 15,000.")
with c_out2:
    st.info("💾 **SQLite Audit Log**\n\nEvery decision, score, officer routing, and GUARD check is persistently logged in `decisions.db` for TRACK framework compliance.")

st.divider()
st.markdown("""
### Technology Stack
- **Orchestration**: CrewAI (`Process.sequential`)
- **LLM Routing**: LiteLLM (Primary: Cerebras/Gemini, Fallbacks: Groq, Cohere, Ollama)
- **UI & Visualization**: Streamlit & Plotly
- **Data Persistence**: SQLite3
""")
