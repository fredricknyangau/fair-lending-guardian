import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Algorithmic Transparency (XAI)")
st.markdown("A core requirement of the PRIDE framework is explainability. This chart breaks down exactly how the Guardian Agent arrived at Grace's final score of 88/100, removing the 'black box' of traditional AI models.")

fig = go.Figure(go.Waterfall(
    name="Guardian Score Calculation",
    orientation="v",
    measure=["absolute", "relative", "relative", "relative", "relative", "total"],
    x=["Base Credit Score", "Length of M-Pesa History", "Harvest Cycle Alignment", "January Income Dip", "School Fee Expected Correlation", "Final Guardian Score"],
    textposition="outside",
    text=["40", "+20", "+30", "-15", "+13", "88"],
    y=[40, 20, 30, -15, 13, 0],
    connector={"line": {"color": "rgb(63, 63, 63)"}},
    increasing={"marker": {"color": "#0F6E56"}},
    decreasing={"marker": {"color": "#E55B3C"}},
    totals={"marker": {"color": "#1C355E"}}
))

fig.update_layout(
    title="Guardian Agent Scoring Breakdown (Grace Achieng)",
    showlegend=False,
    waterfallgap=0.3,
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, width="stretch")

st.info("Traditional algorithms penalize the applicant for the January income dip. The Guardian Agent recognizes the dip, but then applies a counter-weight (+13) because the dip perfectly correlates with the local school fee cycle, demonstrating financial consistency rather than instability.")
