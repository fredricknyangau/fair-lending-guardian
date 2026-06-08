import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st
from guard import proxy_block, kill_switch_check, dignity_filter

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Live GUARD Playground")
st.markdown("Test the safety layer interactivity. Type a message and watch the exact GUARD function fire.")

test_message = st.text_area("Enter a message or application text to test:")

if st.button("Run GUARD checks"):
    st.divider()
    st.subheader("Results")
    
    # 1. Kill Switch Check
    try:
        kill_switch_check(test_message)
        st.success("kill_switch_check: Passed")
    except ValueError as e:
        st.error(f"kill_switch_check: FAILED - {e}")
        
    # 2. Dignity Filter Check
    try:
        dignity_filter(test_message)
        st.success("dignity_filter: Passed")
    except ValueError as e:
        st.error(f"dignity_filter: FAILED - {e}")
        
    # 3. Proxy Block Check (testing with the text as keys/values conceptually)
    # We will simulate feature dict from the text
    features_to_test = {}
    for word in test_message.replace(":", " ").replace(",", " ").split():
        features_to_test[word.lower()] = True

    try:
        proxy_block(features_to_test)
        st.success("proxy_block: Passed")
    except ValueError as e:
        st.error(f"proxy_block: FAILED - {e}")
