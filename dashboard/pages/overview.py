"""Overview Page — Executive Ecosystem Health Intelligence.

Fully compliant with the Global Design System:
- Panchang typography
- 60/30/10 color rule (Obsidian/Emerald)
- 8-point spacing system
- 12/8/4 column responsive grid
- Glassmorphism cards
- Consistent component patterns
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from components.styles import (
    load_design_system,
    render_header,
    render_metric_card,
    render_alert,
    apply_plotly_theme,
    render_glass_panel,
    render_section_header,
    PRIMARY_ACCENT,
    ACCENT_LIGHT,
    SUCCESS,
    WARNING,
    DANGER,
    INFO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER,
    BORDER_SUBTLE,
    SPACING,
)


def render():
    # Load global design system
    load_design_system()
    
    # Render unified header
    render_header(
        sensors_online="72 / 72",
        satellite_status="LIVE SYNC"
    )

    # Anomaly Alert Banner
    st.markdown(render_alert(
        message="<strong>ANOMALY ALERT — WETLAND ZONE A:</strong> 42% decrease in amphibian chorus amplitude detected over 90 days. Correlates with 18% surface water index drop.",
        level="critical",
        icon="⚠️"
    ), unsafe_allow_html=True)

    # Executive KPI Cards - 4 Column Grid
    st.markdown(
        f"""
        <div style="
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: {SPACING['md']};
            margin-bottom: {SPACING['xl']};
        ">
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(render_metric_card(
            title="Biodiversity Score",
            value="72 / 100",
            delta="-8.4%",
            delta_text="vs 12m avg",
            icon="🌿",
            tone="warning",
            subtext="Shannon H': 3.41 (Healthy ref: 3.91)",
            delta_is_negative=True
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_metric_card(
            title="Species Detected",
            value="84 Taxa",
            delta="+3",
            delta_text="new observed",
            icon="🐾",
            tone="info",
            subtext="47 Bioacoustic • 37 Camera Trap"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_metric_card(
            title="Declining Populations",
            value="11 Species",
            delta="-18%",
            delta_text="abundance drop",
            icon="📉",
            tone="danger",
            subtext="4 Amphibian • 5 Avian • 2 Insect",
            delta_is_negative=True
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(render_metric_card(
            title="Ecosystem Risk",
            value="MODERATE",
            delta="89%",
            delta_text="model conf.",
            icon="🛡️",
            tone="warning",
            subtext="Primary Driver: Moisture & Heat Deficit"
        ), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Main Visual Analytics Row 1
    st.markdown(render_section_header(
        "Biodiversity Index Trajectory vs Historical Baseline",
        "Shannon Diversity Index (H') — 12 month rolling window with 5-year baseline"
    ), unsafe_allow_html=True)

    col_left, col_right = st.columns([1.3, 1.0])

    with col_left:
        months = ["Jul '25", "Aug '25", "Sep '25", "Oct '25", "Nov '25", "Dec '25",
                  "Jan '26", "Feb '26", "Mar '26", "Apr '26", "May '26", "Jun '26"]
        historical_baseline = [4.25, 4.22, 4.20, 4.18, 4.15, 4.12, 4.10, 4.08, 4.05, 4.00, 3.98, 3.95]
        observed_shannon = [4.24, 4.20, 4.18, 4.12, 4.01, 3.92, 3.84, 3.71, 3.59, 3.48, 3.39, 3.28]
        critical_threshold = [3.0] * 12

        fig = go.Figure()

        # Shaded danger zone
        fig.add_trace(go.Scatter(
            x=months + months[::-1],
            y=critical_threshold + [4.5]*12,
            fill='toself',
            fillcolor='rgba(239, 68, 68, 0.06)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Critical Degradation Zone (H\' < 3.0)',
            hoverinfo='skip',
            showlegend=True
        ))

        # Historical baseline
        fig.add_trace(go.Scatter(
            x=months, y=historical_baseline,
            mode='lines',
            name='Historical 5-Year Baseline',
            line=dict(color='rgba(148, 163, 184, 0.7)', width=2, dash='dash'),
            hovertemplate='%{x}<br>Baseline: %{y:.2f}<extra></extra>'
        ))

        # Current observed
        fig.add_trace(go.Scatter(
            x=months, y=observed_shannon,
            mode='lines+markers',
            name='Current Observations (PAM + Vision)',
            line=dict(color='#10B981', width=3.5),
            marker=dict(size=7, color='#34D399', line=dict(width=1.5, color='#064E3B')),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.08)',
            hovertemplate='%{x}<br>Observed: %{y:.2f}<extra></extra>'
        ))

        # Anomaly annotation
        fig.add_annotation(
            x="Mar '26", y=3.59,
            text="📉 Accelerated Drop (-14%)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor="#EF4444",
            ax=0, ay=-40,
            font=dict(color="#F87171", size=11, family="Panchang"),
            bgcolor="rgba(15, 23, 42, 0.9)",
            bordercolor="rgba(239, 68, 68, 0.5)",
            borderwidth=1,
            borderpad=6
        )

        apply_plotly_theme(fig, height=380)
        fig.update_yaxes(title="Shannon Diversity Index (H')", range=[2.7, 4.5])
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown(
            render_glass_panel(
                content="<h4 style='margin: 0 0 16px 0; font-size: 15px; color: #F8FAFC;'>Ecosystem Balance Radar</h4>",
                padding="20px"
            ), unsafe_allow_html=True
        )
        
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
            line=dict(color='#10B981', width=2.5),
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

    # Row 2: Taxa Distribution + Priority Species Table
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    
    col_row2_1, col_row2_2 = st.columns([1.1, 1.2])

    with col_row2_1:
        st.markdown(render_section_header(
            "Observed Taxa Distribution",
            "Species richness by taxonomic class with 90-day trend"
        ), unsafe_allow_html=True)
        
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
        fig_donut.update_traces(
            textposition='inside', 
            textinfo='percent+label', 
            marker=dict(line=dict(color='#0B1120', width=2)),
            hovertemplate='%{label}<br>Species: %{value}<br>%{percent}<extra></extra>'
        )
        apply_plotly_theme(fig_donut, height=320)
        fig_donut.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_row2_2:
        st.markdown(render_section_header(
            "High-Priority Species Trend Monitor",
            "Bio-indicator species with >20% abundance change flagged for intervention"
        ), unsafe_allow_html=True)
        
        species_data = [
            {"species": "Indian Peafowl (Pavo cristatus)", "taxon": "Bird", "status": "Stable", "count": 42, "change": "+4%", "color": "#10B981"},
            {"species": "Asian Koel (Eudynamys scolopaceus)", "taxon": "Bird", "status": "Declining", "count": 18, "change": "-22%", "color": "#F59E0B"},
            {"species": "Pantanal Treefrog (Dendropsophus)", "taxon": "Amphibian", "status": "Critical", "count": 7, "change": "-54%", "color": "#EF4444"},
            {"species": "Sambar Deer (Rusa unicolor)", "taxon": "Mammal", "status": "Stable", "count": 26, "change": "+1%", "color": "#10B981"},
            {"species": "Forest Cicada (Platypleura)", "taxon": "Insect", "status": "Declining", "count": 110, "change": "-31%", "color": "#F59E0B"},
        ]

        table_rows = ""
        for s in species_data:
            badge_style = f"background: {s['color']}20; color: {s['color']}; border: 1px solid {s['color']}50; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;"
            change_color = "#34D399" if s["change"].startswith("+") else "#F87171"
            table_rows += f"""
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                <td style="padding: 12px 16px; font-weight: 500; color: #F1F5F9;">{s['species']}</td>
                <td style="padding: 12px 16px; color: #94A3B8;">{s['taxon']}</td>
                <td style="padding: 12px 16px;"><span style="{badge_style}">{s['status']}</span></td>
                <td style="padding: 12px 16px; font-family: monospace; font-size: 14px;">{s['count']}</td>
                <td style="padding: 12px 16px; color: {change_color}; font-weight: 600; font-family: monospace;">{s['change']}</td>
            </tr>
            """
        
        full_table = f"""
        <div class="glass-panel" style="padding: 8px; overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
                <thead>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.12); color: #94A3B8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">
                        <th style="padding: 10px 16px;">Species Name</th>
                        <th style="padding: 10px 16px;">Taxon</th>
                        <th style="padding: 10px 16px;">Trend Status</th>
                        <th style="padding: 10px 16px;">Obs. Count</th>
                        <th style="padding: 10px 16px;">90d Shift</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        """
        st.markdown(full_table, unsafe_allow_html=True)


if __name__ == "__main__":
    render()