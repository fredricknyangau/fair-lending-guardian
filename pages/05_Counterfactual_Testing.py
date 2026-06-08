import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("One-Variable Counterfactual Simulator")
st.markdown("Change one variable at a time for Grace's application to see the impact on routing decisions and approval scores. This demonstrates the TRACK counterfactual test interactively.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Variables")
    occupation = st.selectbox("Occupation Label", ["market vendor", "formal employee", "maize farmer"])
    address = st.selectbox("Sub-county Address", ["Kakamega North", "Westlands Nairobi"])
    loan_amount = st.slider("Loan Amount (KES)", 5000, 50000, 28000, step=1000)

with col2:
    st.subheader("Simulated Outcome")
    
    # Base score heuristics for simulation
    base_score = 42
    
    if occupation == "formal employee":
        base_score += 46
        st.success("Occupation change: Approval jumps 46 points!")
    elif occupation == "maize farmer":
        base_score += 46 # System fix gives her same score

    if address == "Westlands Nairobi":
        base_score += 24
        st.success("Address change: Approval jumps 24 points!")
        
    # Cap score at 98
    final_score = min(base_score, 98)
    
    st.metric("Simulated Guardian Score", f"{final_score}/100")
    
    if loan_amount > 15000:
        st.warning(f"Routing Decision: **Escalate to Hunter Agent** (Loan amount KES {loan_amount} exceeds KES 15,000 threshold)")
    elif final_score >= 90:
        st.success("Routing Decision: **Approve directly**")
    elif final_score >= 70:
        st.info("Routing Decision: **Escalate to Hunter Agent**")
    else:
        st.error("Routing Decision: **Decline**")

st.divider()
st.info("In a traditional algorithm, simply changing the occupation label from 'market vendor' to 'formal employee' flips the decision, despite identical cashflow. This system ignores these labels in favor of 52-week cashflow patterns.")
