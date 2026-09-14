"""Modern design system and UI components for Biodiversity Guardian AI."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Color Palette (Emerald & Midnight Slate)
PRIMARY_EMERALD = "#10B981"
DARK_FOREST = "#064E3B"
BG_DARK = "#0B1120"
CARD_BG = "rgba(30, 41, 59, 0.7)"
BORDER_COLOR = "rgba(51, 65, 85, 0.6)"
TEXT_LIGHT = "#F8FAFC"
TEXT_MUTED = "#94A3B8"

RISK_COLORS = {
    "LOW": {"color": "#10B981", "bg": "rgba(16, 185, 129, 0.15)", "border": "#10B981"},
    "MODERATE": {"color": "#F59E0B", "bg": "rgba(245, 158, 11, 0.15)", "border": "#F59E0B"},
    "HIGH": {"color": "#F97316", "bg": "rgba(249, 115, 22, 0.15)", "border": "#F97316"},
    "CRITICAL": {"color": "#EF4444", "bg": "rgba(239, 68, 68, 0.18)", "border": "#EF4444"},
}


def apply_custom_styles():
    """Inject modern styling into Streamlit app."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Reset */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding & Clean layout */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }

    /* Glassmorphism Cards */
    .glass-panel {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
        transition: all 0.25s ease-in-out;
    }

    .glass-panel:hover {
        border-color: rgba(16, 185, 129, 0.35);
        transform: translateY(-2px);
        box-shadow: 0 15px 30px -5px rgba(16, 185, 129, 0.12);
    }

    /* Metric Card Modern Styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(16, 185, 129, 0.4);
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10B981, #059669);
    }

    .metric-card.warning::before {
        background: linear-gradient(90deg, #F59E0B, #D97706);
    }
    .metric-card.danger::before {
        background: linear-gradient(90deg, #EF4444, #B91C1C);
    }
    .metric-card.info::before {
        background: linear-gradient(90deg, #0EA5E9, #0284C7);
    }

    .metric-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #F8FAFC;
        line-height: 1.1;
    }

    .metric-subtext {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .badge-delta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.15rem 0.45rem;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
    }

    .delta-positive {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .delta-negative {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Glowing Live Indicator */
    .pulse-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 0 rgba(16, 185, 129, 0.6);
        animation: pulse 2s infinite;
        vertical-align: middle;
        margin-right: 6px;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Risk Status Pills */
    .risk-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Clean modern buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1.4rem;
        font-weight: 600;
        font-size: 0.92rem;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
        transition: all 0.2s ease;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #34D399 0%, #059669 100%);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
        transform: translateY(-1px);
        color: #FFFFFF;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background: #090D16;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Custom Streamlit tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.5);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 8px;
        padding: 0 16px;
        font-weight: 600;
        color: #94A3B8;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #10B981 !important;
        color: #FFFFFF !important;
    }

    /* Alert Banner */
    .alert-banner {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.12) 0%, rgba(249, 115, 22, 0.08) 100%);
        border-left: 4px solid #EF4444;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header(active_zone="Pantanal Biodiversity Corridor"):
    """Render top hero brand bar."""
    header_html = f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.8rem 0 1.6rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.07); margin-bottom: 1.8rem;">
        <div>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.8rem;">🌿</span>
                <span style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em; background: linear-gradient(90deg, #F8FAFC 0%, #34D399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    BIODIVERSITY GUARDIAN AI
                </span>
                <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; font-size: 0.72rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3);">
                    V2.4 BIO-INTELLIGENCE
                </span>
            </div>
            <p style="margin: 0.3rem 0 0 2.55rem; font-size: 0.88rem; color: #94A3B8;">
                Passive Acoustic Monitoring • Computer Vision • Multimodal Threat Forecasting
            </p>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); padding: 0.5rem 1rem; border-radius: 12px; font-size: 0.82rem; color: #CBD5E1;">
                <span class="pulse-dot"></span> SENSORS ONLINE: <strong style="color: #34D399;">72 / 72</strong>
            </div>
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); padding: 0.5rem 1rem; border-radius: 12px; font-size: 0.82rem; color: #CBD5E1;">
                🛰️ SATELLITE: <strong style="color: #38BDF8;">LIVE SYNC</strong>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_kpi_card(title, value, delta=None, delta_text="", icon="📊", tone="info", subtext=""):
    """Generate HTML for a styled KPI card."""
    delta_class = "delta-positive" if not str(delta).startswith("-") else "delta-negative"
    delta_arrow = "↑" if not str(delta).startswith("-") else "↓"
    
    delta_html = ""
    if delta is not None:
        delta_html = f'<span class="badge-delta {delta_class}">{delta_arrow} {abs(float(str(delta).replace("+","").replace("-",""))):.0f}% {delta_text}</span>' if str(delta).replace("+","").replace("-","").replace(".","").isdigit() else f'<span class="badge-delta {delta_class}">{delta} {delta_text}</span>'

    html = f"""
    <div class="metric-card {tone}">
        <div class="metric-title">{icon} {title}</div>
        <div style="display: flex; align-items: baseline; justify-content: space-between;">
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """
    return html


def apply_plotly_theme(fig, height=360):
    """Format Plotly charts to seamlessly match the dark eco aesthetic."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1", size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
        ),
    )
    return fig


def render_sidebar():
    """Render a redesigned, professional sidebar."""
    st.sidebar.markdown(
        """
        <div style="padding: 0.5rem 0 1rem 0; text-align: center;">
            <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">🌱</div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #F8FAFC; letter-spacing: -0.01em;">
                GUARDIAN AI
            </div>
            <div style="font-size: 0.74rem; color: #10B981; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px;">
                Ecosystem Health OS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    # Ecosystem Region Selector
    region = st.sidebar.selectbox(
        "🌿 Active Biosphere",
        [
            "Pantanal Wetland Sanctuary",
            "Western Ghats Cloud Forest",
            "Amazon Canopy Basin (Sector 4)",
            "Congo Basin Lowland Forest"
        ],
        index=0
    )
    
    st.sidebar.markdown("---")
    return region
