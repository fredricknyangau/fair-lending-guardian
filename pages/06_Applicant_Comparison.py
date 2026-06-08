import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Applicant Comparison")
st.markdown("Comparing Grace against a hypothetical formal employee with identical weekly income.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Grace Achieng")
    st.markdown("**Occupation:** Market Vendor")
    st.markdown("**Income:** KES 3,231 / week")
    st.markdown("**Before Fix:** 20/100 (Penalized for occupation label)")
    st.success("**After Fix:** 88/100")
    st.info("The system now correctly assesses her seasonal income as stable and reliable.")

with col2:
    st.subheader("Formal Employee")
    st.markdown("**Occupation:** Formal Employee")
    st.markdown("**Income:** KES 3,231 / week")
    st.markdown("**Before Fix:** 88/100 (Benefited from occupation label)")
    st.success("**After Fix:** 88/100")
    st.info("The formal employee's score remains unchanged, proving the system removed the label penalty without breaking.")
