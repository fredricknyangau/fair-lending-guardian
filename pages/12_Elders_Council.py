import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Elders Council: PRIDE Loop Governance")

st.subheader("Council Members")
st.markdown(
    """
    <div style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem;">
        <div style="border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
            <h4 style="margin-top: 0;">SACCO Manager</h4>
            <p style="margin-bottom: 0;"><b>Authority:</b> Protocol and operations override.</p>
            <p style="margin-bottom: 0;"><b>Veto Scope:</b> Administrative changes.</p>
        </div>
        <div style="border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
            <h4 style="margin-top: 0;">SACCO Manager</h4>
            <p style="margin-bottom: 0;"><b>Authority:</b> Protocol and operations override.</p>
            <p style="margin-bottom: 0;"><b>Veto Scope:</b> Administrative changes.</p>
        </div>
        <div style="border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
            <h4 style="margin-top: 0;">SACCO Manager</h4>
            <p style="margin-bottom: 0;"><b>Authority:</b> Protocol and operations override.</p>
            <p style="margin-bottom: 0;"><b>Veto Scope:</b> Administrative changes.</p>
        </div>
        <div style="border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
            <h4 style="margin-top: 0;">Women Vendor Representative</h4>
            <p style="margin-bottom: 0;"><b>Authority:</b> Representing vendor demographics.</p>
            <p style="margin-bottom: 0;"><b>Veto Scope:</b> Any model update negatively impacting vendors.</p>
        </div>
        <div style="border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
            <h4 style="margin-top: 0;">Women Vendor Representative</h4>
            <p style="margin-bottom: 0;"><b>Authority:</b> Representing vendor demographics.</p>
            <p style="margin-bottom: 0;"><b>Veto Scope:</b> Any model update negatively impacting vendors.</p>
        </div>
        <div style="border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
            <h4 style="margin-top: 0;">SASRA Representative</h4>
            <p style="margin-bottom: 0;"><b>Authority:</b> Regulatory compliance.</p>
            <p style="margin-bottom: 0;"><b>Veto Scope:</b> Any change violating SASRA guidelines.</p>
        </div>
        <div style="border: 1px solid #A32D2D; padding: 1rem; border-radius: 8px;">
            <h4 style="margin-top: 0; color: #A32D2D;">Community Elder</h4>
            <p style="margin-bottom: 0;"><b>Authority:</b> Cultural alignment.</p>
            <p style="margin-bottom: 0; color: #A32D2D; font-weight: bold;">Veto on any member-facing language is binding and cannot be overridden.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("P - Pause Points"):
    st.write("- Loans above KES 15,000")
    st.write("- Applicants with children under 5")
    st.write("- Food security threshold below KES 150 per person per day")
    st.write("- Any TRACK Kill Switch zone")
    st.write("- First application from a member who filed a complaint in the prior 12 months")

with st.expander("R - Review Cadence"):
    st.write("- Quarterly SASRA audits")
    st.write("- Monthly TRACK report by gender, occupation, sub-county, and age")
    st.write("- Any disparity above 15 percentage points triggers model freeze within 5 business days")

with st.expander("I - Interpretability"):
    st.write("Example denial SMS in Swahili:")
    st.write("Mkopo wako umesimamishwa kwa sababu mapato yako hupungua wakati wa ada za shule. Tunahitaji akiba ya miezi 3. Tunakusaidia kukusanya hizi. Piga simu ya bure kwa kuandika *#123#.")

with st.expander("D - Disagreement Rights"):
    st.write("USSD mechanism: dial *#123#")
    st.write("Free of charge, no time limit, 5-business-day SLA, zero credit score impact.")

with st.expander("E - Elders Council"):
    council_data = [
        {"Role Title": "SACCO Manager", "Authority": "Protocol and operations override", "Veto Scope": "Administrative changes"},
        {"Role Title": "SACCO Manager", "Authority": "Protocol and operations override", "Veto Scope": "Administrative changes"},
        {"Role Title": "SACCO Manager", "Authority": "Protocol and operations override", "Veto Scope": "Administrative changes"},
        {"Role Title": "Women Vendor Representative", "Authority": "Representing vendor demographics", "Veto Scope": "Any model update negatively impacting vendors"},
        {"Role Title": "Women Vendor Representative", "Authority": "Representing vendor demographics", "Veto Scope": "Any model update negatively impacting vendors"},
        {"Role Title": "SASRA Representative", "Authority": "Regulatory compliance", "Veto Scope": "Any change violating SASRA guidelines"},
        {"Role Title": "Community Elder", "Authority": "Cultural alignment", "Veto Scope": "Veto on any member-facing language is binding and cannot be overridden"}
    ]
    st.dataframe(council_data, use_container_width=True)

st.subheader("Kill switch reference")
kill_switch_data = [
    {"Switch": "Scout kill switch", "Dial Code": "*#700#", "Scope": "Pauses Scout outbound SMS"},
    {"Switch": "Guardian kill switch", "Dial Code": "*#733#", "Scope": "Pauses Guardian scoring"},
    {"Switch": "Full system", "Dial Code": "*#799#", "Scope": "Pauses all three agents and convenes Elders Council"},
    {"Switch": "Member appeal", "Dial Code": "*#123#", "Scope": "Free, zero credit score impact"},
]
st.dataframe(kill_switch_data, use_container_width=True)
