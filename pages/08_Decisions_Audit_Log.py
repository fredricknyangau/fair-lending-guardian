import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st
import database

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("SQLite Decision Audit Log")
st.markdown("A persistent audit log of all decisions processed through the Guardian system.")

# Ensure DB is initialized
database.init_db()

# Fetch from SQLite
df = database.get_last_10()

st.dataframe(df, use_container_width=True)

st.subheader("SASRA Notification Log")
import sqlite3
import pandas as pd
conn = sqlite3.connect("decisions.db")
try:
    sasra_df = pd.read_sql_query("SELECT * FROM sasra_alerts ORDER BY id DESC LIMIT 10", conn)
    st.dataframe(sasra_df, use_container_width=True)
except Exception:
    st.info("No SASRA alerts generated yet.")
finally:
    conn.close()
