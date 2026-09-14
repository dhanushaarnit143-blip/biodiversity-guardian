"""Overview page - Executive Ecosystem Health Intelligence."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path

from components.styles import (
    render_header, render_kpi_card, apply_plotly_theme,
    PRIMARY_EMERALD, RISK_COLORS
)


def get_database_metrics():
    """Retrieve summary metrics from the local SQLite database if available."""
    db_path = Path(__file__).resolve().parent.parent.parent / "data" / "biodiversity.db"
    if not db_path.exists():
        return None
    try:
        conn = sqlite3.connect(db_path)
        metrics_df = pd.read_sql_query("SELECT * FROM biodiversity_metrics ORDER BY timestamp DESC LIMIT 36", conn)
        species_df = pd.read_sql_query("SELECT species_name, species_class, count FROM species_detections", conn)
        conn.close()
        return {"metrics": metrics_df, "species": species_df}
    except Exception:
        return None


def render():
    render_header()

    # Dynamic Anomaly Alert Banner
    st.markdown(
        """
        <div class="alert-banner">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <span style="font-size: 1.4rem;">⚠️</span>
                <div>
                    <strong style="color: #FCA5A5; font-size: 0.95rem;">ANOMALY ALERT — WETLAND ZONE A:</strong>
                    <span style="color: #CBD5E1; font-size: 0.9rem; margin-left: 0.4rem;">
                        42% decrease in amphibian chorus amplitude detected over 90 days. Correlates with 18% surface water index drop.
                    </span>
                </div>
            </div>
            <span class="badge-delta delta-negative" style="font-size: 0.8rem;">HIGH SEVERITY</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Executive KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            render_kpi_card(
                title="Biodiversity Score",
                value="72 / 100",
                delta="-8.4%",
                delta_text="vs 12m avg",
                icon="🌿",
                tone="warning",
                subtext="Shannon H': 3.41 (Healthy ref: 3.91)"
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_kpi_card(
                title="Species Detected",
                value="84 Taxa",
                delta="+3",
                delta_text="new observed",
                icon="🐾",
                tone="info",
                subtext="47 Bioacoustic • 37 Camera Trap"
            ),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            render_kpi_card(
                title="Declining Populations",
                value="11 Species",
                delta="-18%",
                delta_text="abundance drop",
                icon="📉",
                tone="danger",
                subtext="4 Amphibian • 5 Avian • 2 Insect"
            ),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            render_kpi_card(
                title="Ecosystem Risk",
                value="MODERATE",
                delta="89%",
                delta_text="model conf.",
                icon="🛡️",
                tone="warning",
                subtext="Primary Driver: Moisture & Heat Deficit"
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # Main Visual Analytics - Row 1
    col_left, col_right = st.columns([1.3, 1.0])

    with col_left:
        st.markdown("#### 📈 Biodiversity Index Trajectory vs Historical Baseline")
        
        months = ["Jul '25", "Aug '25", "Sep '25", "Oct '25", "Nov '25", "Dec '25", 
                  "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26", "Jun '26"]
        historical_baseline = [4.25, 4.22, 4.20, 4.18, 4.15, 4.12, 4.10, 4.08, 4.05, 4.00, 3.98, 3.95]
        observed_shannon = [4.24, 4.20, 4.18, 4.12, 4.01, 3.92, 3.84, 3.71, 3.59, 3.48, 3.39, 3.28]
        critical_threshold = [3.0] * 12

        fig = go.Figure()

        # Shaded danger zone
        fig.add_trace(go.Scatter(
            x=months, y=critical_threshold,
            mode='lines',
            line=dict(color='rgba(239, 68, 68, 0.4)', width=1, dash='dot'),
            name='Critical Degradation Threshold (3.0 H\')'
        ))

        # Historical baseline
        fig.add_trace(go.Scatter(
            x=months, y=historical_baseline,
            mode='lines',
            name='Historical 5-Year Baseline',
            line=dict(color='rgba(148, 163, 184, 0.7)', width=2, dash='dash')
        ))

        # Current observed
        fig.add_trace(go.Scatter(
            x=months, y=observed_shannon,
            mode='lines+markers',
            name='Current Observations (PAM + Vision)',
            line=dict(color=PRIMARY_EMERALD, width=3.5),
            marker=dict(size=7, color='#34D399', line=dict(width=1.5, color='#064E3B')),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.08)'
        ))

        # Anomaly marker
        fig.add_annotation(
            x="Mar '26", y=3.59,
            text="📉 Accelerated Drop (-14%)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor="#EF4444",
            ax=0, ay=-40,
            font=dict(color="#F87171", size=10),
            bgcolor="rgba(15, 23, 42, 0.8)",
            bordercolor="rgba(239, 68, 68, 0.5)",
            borderwidth=1,
            borderpad=4
        )

        apply_plotly_theme(fig, height=360)
        fig.update_yaxes(title="Shannon Diversity Index (H')", range=[2.7, 4.4])
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("#### 🕸️ Ecosystem Balance: Baseline vs Current")
        
        categories = ['Avian Diversity', 'Amphibian Activity', 'Mammalian Count', 
                      'Insect Biomass', 'Canopy NDVI', 'Soil Moisture']
        
        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=[88, 82, 79, 90, 85, 76],
            theta=categories,
            fill='toself',
            name='Historical Baseline',
            line=dict(color='rgba(148, 163, 184, 0.7)', width=1.5),
            fillcolor='rgba(148, 163, 184, 0.12)'
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=[74, 46, 75, 62, 70, 52],
            theta=categories,
            fill='toself',
            name='Current Status',
            line=dict(color=PRIMARY_EMERALD, width=2.5),
            fillcolor='rgba(16, 185, 129, 0.25)'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#64748B", gridcolor="rgba(255,255,255,0.06)"),
                angularaxis=dict(color="#CBD5E1", gridcolor="rgba(255,255,255,0.06)"),
                bgcolor="rgba(15, 23, 42, 0.4)"
            ),
            height=360,
            margin=dict(l=40, r=40, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Main Visual Analytics - Row 2
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    col_row2_1, col_row2_2 = st.columns([1.1, 1.2])

    with col_row2_1:
        st.markdown("#### 🔬 Observed Taxa Distribution")
        taxa_df = pd.DataFrame({
            "Taxa": ["Avian (Birds)", "Insecta", "Mammalia", "Amphibia", "Reptilia"],
            "Species": [32, 28, 14, 6, 4],
            "Abundance": [480, 1250, 142, 86, 38],
            "Trend": ["-8%", "-14%", "+2%", "-42%", "-4%"]
        })
        
        fig_donut = px.pie(
            taxa_df, values="Species", names="Taxa", hole=0.55,
            color_discrete_sequence=["#10B981", "#38BDF8", "#F59E0B", "#EF4444", "#A855F7"]
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0B1120', width=2)))
        apply_plotly_theme(fig_donut, height=310)
        fig_donut.update_layout(showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_row2_2:
        st.markdown("#### 📋 High-Priority Species Trend Monitor")
        
        species_monitor = [
            {"Species": "Indian Peafowl (Pavo cristatus)", "Taxon": "Bird", "Status": "Stable", "Count": 42, "Change": "+4%", "Color": "#10B981"},
            {"Species": "Asian Koel (Eudynamys scolopaceus)", "Taxon": "Bird", "Status": "Declining", "Count": 18, "Change": "-22%", "Color": "#F59E0B"},
            {"Species": "Pantanal Treefrog (Dendropsophus)", "Taxon": "Amphibian", "Status": "Critical", "Count": 7, "Change": "-54%", "Color": "#EF4444"},
            {"Species": "Sambar Deer (Rusa unicolor)", "Taxon": "Mammal", "Status": "Stable", "Count": 26, "Change": "+1%", "Color": "#10B981"},
            {"Species": "Forest Cicada (Platypleura)", "Taxon": "Insect", "Status": "Declining", "Count": 110, "Change": "-31%", "Color": "#F59E0B"},
        ]

        table_rows = ""
        for s in species_monitor:
            badge_style = f"background: {s['Color']}20; color: {s['Color']}; border: 1px solid {s['Color']}50; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 0.78rem;"
            change_color = "#34D399" if s["Change"].startswith("+") else "#F87171"
            table_rows += f"""
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                <td style="padding: 10px 12px; font-weight: 500; color: #F1F5F9;">{s['Species']}</td>
                <td style="padding: 10px 12px; color: #94A3B8;">{s['Taxon']}</td>
                <td style="padding: 10px 12px;"><span style="{badge_style}">{s['Status']}</span></td>
                <td style="padding: 10px 12px; font-family: monospace; font-size: 0.95rem;">{s['Count']}</td>
                <td style="padding: 10px 12px; color: {change_color}; font-weight: 600; font-family: monospace;">{s['Change']}</td>
            </tr>
            """

        table_html = f"""
        <div class="glass-panel" style="padding: 0.5rem; overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem;">
                <thead>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.12); color: #94A3B8; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em;">
                        <th style="padding: 8px 12px;">Species Name</th>
                        <th style="padding: 8px 12px;">Taxon</th>
                        <th style="padding: 8px 12px;">Trend Status</th>
                        <th style="padding: 8px 12px;">Obs. Count</th>
                        <th style="padding: 8px 12px;">90d Shift</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)
