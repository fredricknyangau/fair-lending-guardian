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

st.title("Bias Audit: TRACK Framework Analysis")

# Chart 1: Plotly grouped bar chart
fig1 = go.Figure(data=[
    go.Bar(name='Before Fair Lending Guardian', x=['market vendor', 'formal employee'], y=[68, 22], marker_color='#A32D2D'),
    go.Bar(name='After Fair Lending Guardian', x=['market vendor', 'formal employee'], y=[31, 21], marker_color='#0F6E56')
])
fig1.update_layout(barmode='group', title_text='Loan denial rate by occupation: before and after')
fig1.update_yaxes(title_text='Denial rate in percent')
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Plotly horizontal bar chart
fig2 = go.Figure(go.Bar(
    x=[9, 9, 7, 6],
    y=['Training corpus skew', 'Occupation as income proxy', 'Address as ethnicity proxy', 'Short feature window'],
    orientation='h',
    marker_color='#A32D2D'
))
fig2.update_layout(title_text='Bias vectors identified in TRACK audit', yaxis={'autorange': 'reversed'})
fig2.add_vline(x=8, line_dash="dash", line_color="#A32D2D", annotation_text="Kill Switch threshold")
st.plotly_chart(fig2, use_container_width=True)

# Counterfactual results
col1, col2 = st.columns(2)
col1.metric("Occupation label swap", "+46pp", "+changing only occupation label reversed decision")
col2.metric("Address swap", "+24pp", "+changing only sub-county raised approval rate")

st.error("Both counterfactual tests exceeded the 20 percentage point Kill Switch threshold. Both variables are now hard-blocked by proxy_block() in guard.py.")

# Three bugs table
bugs_data = [
    {"Bug": "Bug 1", "Root Cause": "Routing rule ignored loan amounts above KES 15,000", "Fix Applied": "RULE A strictly escalates all >KES 15,000 loans to Hunter Agent", "Status": "Resolved"},
    {"Bug": "Bug 2", "Root Cause": "Seasonal income variations were penalized by generic risk prompt", "Fix Applied": "Framed seasonal high-to-low ratio >3.0 as normal/expected", "Status": "Resolved"},
    {"Bug": "Bug 3", "Root Cause": "Missing demographic context in human-in-loop briefing", "Fix Applied": "Hard-coded application dict mapping into the Hunter task string", "Status": "Resolved"},
]
st.dataframe(bugs_data, use_container_width=True)

# TRACK five-dimension table
track_data = [
    {"Dimension": "T", "Question Asked": "Training corpus skew", "Finding": "only 6 percent of training data represented informal traders", "Severity": "9", "Status": "Mitigated"},
    {"Dimension": "R", "Question Asked": "Occupation as income proxy", "Finding": "market vendor label carried a 42-point risk penalty regardless of cashflow", "Severity": "9", "Status": "Mitigated"},
    {"Dimension": "A", "Question Asked": "Address as ethnicity proxy", "Finding": "sub-county correlated with gender and ethnicity in a three-step proxy chain", "Severity": "7", "Status": "Mitigated"},
    {"Dimension": "C", "Question Asked": "Counterfactual stability", "Finding": "changing occupation label reversed decision by 46 percentage points", "Severity": "Kill Switch", "Status": "Mitigated"},
    {"Dimension": "K", "Question Asked": "Knowledge window", "Finding": "8-week analysis missed harvest cycles", "Severity": "6", "Status": "Resolved"},
]
st.dataframe(track_data, use_container_width=True)
