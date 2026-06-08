import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st
import plotly.graph_objects as go
from mock_data import GRACE_APPLICATION

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Income Pattern Analysis")

st.markdown("Grace's 52-week M-Pesa income chart")

inflows = GRACE_APPLICATION["mpesa_weekly_inflows"]
weeks = list(range(1, 53))
avg_inflow = 3231

fig = go.Figure()

# Add line chart for inflows
fig.add_trace(go.Scatter(
    x=weeks, y=inflows,
    mode='lines+markers',
    name='Weekly Inflows (KES)',
    line=dict(color='#0F6E56', width=2),
    marker=dict(size=6)
))

# Add horizontal line for average
fig.add_hline(y=avg_inflow, line_dash="dash", line_color="blue", annotation_text="Average: KES 3,231")

# Add annotations for harvest peaks and school fee dips
fig.add_vrect(x0=8, x1=16, fillcolor="green", opacity=0.1, line_width=0, annotation_text="Harvest Peak (Mar-Apr)", annotation_position="top left")
fig.add_vrect(x0=36, x1=44, fillcolor="green", opacity=0.1, line_width=0, annotation_text="Harvest Peak (Sep-Oct)", annotation_position="top left")
fig.add_vrect(x0=1, x1=4, fillcolor="orange", opacity=0.1, line_width=0, annotation_text="School Fee Dip (Jan)", annotation_position="bottom right")

fig.update_layout(
    title="Grace Achieng - 52 Week M-Pesa Inflows",
    xaxis_title="Week",
    yaxis_title="KES",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.info("A traditional algorithm sees the dips and rejects Grace. This chart shows exactly why that is wrong, in one glance. Seasonal income spikes (harvest months) are classified as neutral, not risk flags. A high-to-low ratio above 3.0 = expected for farmers.")
