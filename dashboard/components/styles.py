"""Biodiversity Guardian AI — Global Design System Components.

This module provides the unified design system for the entire application,
implementing the Panchang font, 60/30/10 color rule, 8-point spacing,
12/8/4 column grid, and all component patterns.
"""
import streamlit as st
from pathlib import Path
from typing import Optional, List, Dict, Any

# Design System Color Tokens
PRIMARY_ACCENT = "#10B981"
ACCENT_HOVER = "#059669"
ACCENT_LIGHT = "#34D399"

NEUTRAL_BASE = "#0B1120"
NEUTRAL_ELEVATED = "#121826"
NEUTRAL_HIGHLIGHT = "#1E293B"

SECONDARY_BASE = "#0F172A"
SECONDARY_ELEVATED = "#162034"
SECONDARY_MUTED = "#1E293B"

SUCCESS = "#10B981"
SUCCESS_BG = "rgba(16, 185, 129, 0.15)"
WARNING = "#F59E0B"
WARNING_BG = "rgba(245, 158, 11, 0.15)"
DANGER = "#EF4444"
DANGER_BG = "rgba(239, 68, 68, 0.15)"
INFO = "#38BDF8"
INFO_BG = "rgba(56, 189, 248, 0.15)"

BORDER = "rgba(51, 65, 85, 0.6)"
BORDER_SUBTLE = "rgba(51, 65, 85, 0.3)"
BORDER_ACCENT = "rgba(16, 185, 129, 0.3)"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"
TEXT_MUTED = "#94A3B8"


def load_design_system():
    """Inject the global design system CSS into the Streamlit app."""
    css_path = Path(__file__).resolve().parent.parent / "assets" / "design-system.css"
    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_header(
    title: str = "BIODIVERSITY GUARDIAN AI",
    subtitle: str = "Passive Acoustic Monitoring • Computer Vision • Multimodal Threat Forecasting",
    version: str = "V2.5 BIO-INTELLIGENCE",
    sensors_online: str = "72 / 72",
    satellite_status: str = "LIVE SYNC"
):
    """Render the top brand header with live telemetry."""
    header_html = f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0 24px 0;
        border-bottom: 1px solid {BORDER_SUBTLE};
        margin-bottom: 28px;
    ">
        <div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 28px;">🌿</span>
                <span style="
                    font-size: 26px;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                    background: linear-gradient(90deg, {TEXT_PRIMARY} 0%, {ACCENT_LIGHT} 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                ">
                    {title}
                </span>
                <span style="
                    background: rgba(16, 185, 129, 0.15);
                    color: {ACCENT_LIGHT};
                    font-size: 11.5px;
                    font-weight: 700;
                    padding: 4px 12px;
                    border-radius: 12px;
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                ">
                    {version}
                </span>
            </div>
            <p style="
                margin: 6px 0 0 40px;
                font-size: 14px;
                color: {TEXT_MUTED};
                font-weight: 400;
            ">
                {subtitle}
            </p>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="
                background: {NEUTRAL_ELEVATED};
                border: 1px solid {BORDER};
                padding: 8px 16px;
                border-radius: 12px;
                font-size: 13px;
                color: {TEXT_SECONDARY};
            ">
                <span class="pulse-dot"></span>
                SENSORS ONLINE: <strong style="color: {ACCENT_LIGHT};">{sensors_online}</strong>
            </div>
            <div style="
                background: {NEUTRAL_ELEVATED};
                border: 1px solid {BORDER};
                padding: 8px 16px;
                border-radius: 12px;
                font-size: 13px;
                color: {TEXT_SECONDARY};
            ">
                🛰️ SATELLITE: <strong style="color: {INFO};">{satellite_status}</strong>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_metric_card(
    title: str,
    value: str,
    delta: Optional[str] = None,
    delta_text: str = "",
    icon: str = "📊",
    tone: str = "info",
    subtext: str = "",
    delta_is_negative: bool = False
) -> str:
    """Generate HTML for a styled KPI metric card following design system."""
    delta_class = "delta-negative" if delta_is_negative else "delta-positive"
    delta_arrow = "↓" if delta_is_negative else "↑"
    
    tone_border = {
        "info": ACCENT_LIGHT,
        "warning": WARNING,
        "danger": DANGER,
        "success": SUCCESS
    }.get(tone, ACCENT_LIGHT)
    
    delta_html = ""
    if delta is not None:
        abs_delta = abs(float(str(delta).replace("+","").replace("-","").replace("%","").replace(",","")))
        delta_display = f"{delta_arrow} {abs_delta:.0f}% {delta_text}" if "%" in str(delta) or str(delta).replace(".","").replace("-","").isdigit() else f"{delta} {delta_text}"
        delta_html = f'<span class="badge-delta {delta_class}">{delta_display}</span>'

    return f"""
    <div class="metric-card metric-card--{tone}" style="--accent-color: {tone_border};">
        <div class="metric-title">{icon} {title}</div>
        <div style="display: flex; align-items: baseline; justify-content: space-between;">
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """


def render_alert(
    message: str,
    level: str = "critical",
    icon: str = "⚠️",
    dismissible: bool = False
) -> str:
    """Render an alert banner following design system."""
    level_config = {
        "critical": {"bg": DANGER_BG, "border": DANGER, "text": "#FCA5A5"},
        "warning": {"bg": WARNING_BG, "border": WARNING, "text": "#FCD34D"},
        "info": {"bg": INFO_BG, "border": INFO, "text": "#7DD3FC"},
        "success": {"bg": SUCCESS_BG, "border": SUCCESS, "text": "#6EE7B7"}
    }
    cfg = level_config.get(level, level_config["critical"])
    
    return f"""
    <div class="alert alert--{level}" style="
        background: {cfg['bg']};
        border-left-color: {cfg['border']};
        color: {cfg['text']};
        border-radius: 0 16px 16px 0;
        padding: 16px 20px;
        margin-bottom: 24px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    ">
        <span style="font-size: 22px; margin-top: 2px;">{icon}</span>
        <div style="flex: 1; font-size: 15px; line-height: 1.6;">
            <strong style="font-size: 15px;">{message}</strong>
        </div>
    </div>
    """


def render_status_pill(
    text: str,
    level: str = "moderate",
    icon: str = ""
) -> str:
    """Render a status pill badge."""
    level_config = {
        "low": {"bg": SUCCESS_BG, "color": SUCCESS, "border": f"rgba(16,185,129,0.3)"},
        "moderate": {"bg": WARNING_BG, "color": WARNING, "border": f"rgba(245,158,11,0.3)"},
        "high": {"bg": WARNING_BG, "color": "#F97316", "border": f"rgba(249,115,22,0.3)"},
        "critical": {"bg": DANGER_BG, "color": DANGER, "border": f"rgba(239,68,68,0.3)"}
    }
    cfg = level_config.get(level, level_config["moderate"])
    
    return f"""
    <span class="status-pill status-pill--{level}" style="
        background: {cfg['bg']};
        color: {cfg['color']};
        border: 1px solid {cfg['border']};
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    ">
        {icon} {text}
    </span>
    """


def render_section_header(title: str, description: str = "", action_html: str = "") -> str:
    """Render a consistent section header."""
    return f"""
    <div style="margin-bottom: 24px;">
        <h3 style="
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: {TEXT_PRIMARY};
            margin: 0 0 8px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            {title}
            {action_html}
        </h3>
        {f'<p style="margin: 0; font-size: 14px; color: {TEXT_MUTED};">{description}</p>' if description else ''}
    </div>
    """


def apply_plotly_theme(fig, height: int = 360, title_font_size: int = 14):
    """Apply the design system theme to Plotly charts."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(
            family="Panchang, sans-serif",
            color=TEXT_SECONDARY,
            size=11
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=TEXT_SECONDARY),
            bgcolor="rgba(0,0,0,0)",
            bordercolor=BORDER_SUBTLE,
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            title_font=dict(size=12, color=TEXT_MUTED),
            tickfont=dict(size=11, color=TEXT_MUTED)
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            title_font=dict(size=12, color=TEXT_MUTED),
            tickfont=dict(size=11, color=TEXT_MUTED)
        ),
        hoverlabel=dict(
            bgcolor=NEUTRAL_ELEVATED,
            bordercolor=BORDER,
            font=dict(family="Panchang, sans-serif", size=12, color=TEXT_PRIMARY)
        )
    )
    return fig


def render_glass_panel(content: str, padding: str = "16px 20px", border_accent: bool = False) -> str:
    """Render a glassmorphism panel container."""
    border_style = f"border-left: 3px solid {PRIMARY_ACCENT};" if border_accent else f"border: 1px solid {BORDER};"
    
    return f"""
    <div class="glass-panel" style="
        {border_style}
        padding: {padding};
        margin-bottom: 16px;
    ">
        {content}
    </div>
    """


def render_data_table(headers: List[str], rows: List[List[str]], striped: bool = True) -> str:
    """Render a data table following design system."""
    header_row = "".join([f'<th style="padding: 8px 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: {TEXT_MUTED}; border-bottom: 1px solid {BORDER}; background: {SECONDARY_BASE};">{h}</th>' for h in headers])
    
    body_rows = ""
    for i, row in enumerate(rows):
        bg = f"background: {SECONDARY_BASE};" if striped and i % 2 == 0 else ""
        cells = "".join([f'<td style="padding: 10px 12px; color: {TEXT_SECONDARY}; border-bottom: 1px solid {BORDER_SUBTLE}; {bg}">{cell}</td>' for cell in row])
        body_rows += f'<tr style="{bg}">{cells}</tr>'
    
    return f"""
    <div class="glass-panel" style="padding: 8px; overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
            <thead>
                <tr>{header_row}</tr>
            </thead>
            <tbody>
                {body_rows}
            </tbody>
        </table>
    </div>
    """


def render_sidebar_brand():
    """Render the redesigned sidebar brand section."""
    st.sidebar.markdown(
        f"""
        <div style="padding: 8px 0 20px 0; text-align: center;">
            <div style="font-size: 32px; margin-bottom: 4px;">🌱</div>
            <div style="
                font-weight: 800;
                font-size: 18px;
                color: {TEXT_PRIMARY};
                letter-spacing: -0.01em;
            ">
                GUARDIAN AI
            </div>
            <div style="
                font-size: 12px;
                color: {ACCENT_LIGHT};
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-top: 4px;
            ">
                Ecosystem Health OS
            </div>
        </div>
        <hr style="border-color: {BORDER_SUBTLE}; margin: 16px 0;">
        """,
        unsafe_allow_html=True
    )


# Spacing tokens for consistent use across components
SPACING = {
    "xs": "8px",    # --space-1
    "sm": "16px",   # --space-2
    "md": "24px",   # --space-3
    "lg": "32px",   # --space-4
    "xl": "40px",   # --space-5
    "2xl": "48px",  # --space-6
    "3xl": "64px",  # --space-8
    "4xl": "96px",  # --space-10
}

# Section spacing (double internal)
SECTION_SPACING = {
    "sm": "32px",   # 2x xs
    "md": "48px",   # 2x sm
    "lg": "64px",   # 2x md
    "xl": "96px",   # 2x lg
}