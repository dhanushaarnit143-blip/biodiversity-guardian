import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def render():
    st.title("🌍 Ecosystem Health Overview")
    st.markdown("Real-time biodiversity monitoring dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Biodiversity Score", "72/100", delta="-8", delta_color="inverse")
    with col2:
        st.metric("Species Detected", "84", delta="+3")
    with col3:
        st.metric("Species Declining", "11", delta="+2", delta_color="inverse")
    with col4:
        st.metric("Ecosystem Risk", "MODERATE", delta="↑", delta_color="inverse")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Biodiversity Trend (6 Months)")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        shannon = [4.21, 4.18, 4.03, 3.72, 3.41, 3.28]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=shannon, mode="lines+markers", name="Shannon Index", line=dict(color="#228B22", width=3)))
        fig.update_layout(xaxis_title="Month", yaxis_title="Shannon Index", template="plotly_white", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Species Distribution")
        categories = ["Birds", "Mammals", "Amphibians", "Insects", "Reptiles"]
        counts = [25, 12, 8, 42, 7]
        fig = px.pie(values=counts, names=categories, color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Risk Level Distribution Across Zones")
    zones = ["Wetland A", "Forest B", "Grassland C", "Riparian D", "Highland E"]
    risks = ["HIGH", "LOW", "MODERATE", "HIGH", "CRITICAL"]
    risk_colors = {"LOW": "#228B22", "MODERATE": "#FFD700", "HIGH": "#FF8C00", "CRITICAL": "#DC143C"}
    fig = go.Figure(data=[go.Bar(x=zones, y=[3, 1, 2, 3, 4], marker_color=[risk_colors[r] for r in risks], text=risks, textposition="auto")])
    fig.update_layout(yaxis_title="Risk Score", template="plotly_white", height=300)
    st.plotly_chart(fig, use_container_width=True)