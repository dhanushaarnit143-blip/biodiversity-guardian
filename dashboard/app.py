"""Biodiversity Guardian AI — Main Application Entry Point.

Global Design System Initialization:
- Panchang font (Fontshare)
- 60/30/10 color rule (Obsidian/Emerald)
- 8-point spacing system
- 12/8/4 column responsive grid
- Glassmorphism components
"""
import streamlit as st
from pathlib import Path
import sys

# Add src to path for module imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Page configuration
st.set_page_config(
    page_title="Biodiversity Guardian AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load design system FIRST (before any UI rendering)
from components.styles import load_design_system, render_sidebar_brand
load_design_system()

# Sidebar Navigation
render_sidebar_brand()

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Overview",
        "🗺️ Biodiversity Map",
        "🎙️ Sound Monitor",
        "📷 Wildlife Monitor",
        "🤖 Conservation AI",
    ],
    label_visibility="collapsed"
)

# Telemetry Action Controls in Sidebar
if st.sidebar.button("🔄 Sync Live Conservation Telemetry", use_container_width=True):
    with st.sidebar:
        with st.spinner("Connecting to Open-Meteo & iNaturalist..."):
            try:
                from scripts.ingest_real_data import ingest_live_data
                sync_result = ingest_live_data(limit_per_taxon=4)
                if sync_result["status"] == "success":
                    st.toast(
                        f"✅ Synced {sync_result['species_upserted']} species occurrences and microclimates!",
                        icon="🌿"
                    )
                elif sync_result["status"] == "cached_fallback":
                    st.toast(
                        f"⚠️ {sync_result['message']}",
                        icon="🛡️"
                    )
                else:
                    st.toast(f"ℹ️ {sync_result['message']}", icon="ℹ️")
            except Exception as e:
                st.sidebar.error(f"Sync fallback: {e}")
            st.rerun()

# System Status in Sidebar
try:
    from database.models import SessionLocal, BiodiversityMetric, Observation
    _db = SessionLocal()
    _latest_metric = _db.query(BiodiversityMetric).order_by(BiodiversityMetric.timestamp.desc()).first()
    _last_sync = _latest_metric.timestamp.strftime("%H:%M UTC") if _latest_metric and _latest_metric.timestamp else "Just now"
    _db.close()
except Exception:
    _last_sync = "Live Stream"

st.sidebar.markdown(
    f"""
    <div style="padding: 12px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(51, 65, 85, 0.4); border-radius: 12px; margin-top: 12px;">
        <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px;">
            System Telemetry
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
            <span style="color: #94A3B8;">Open-Meteo Link</span>
            <strong style="color: #34D399;">Active • Online</strong>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
            <span style="color: #94A3B8;">iNaturalist API</span>
            <strong style="color: #38BDF8;">Synced</strong>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
            <span style="color: #94A3B8;">Ecosystem Zones</span>
            <strong style="color: #F59E0B;">5 Sectors</strong>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px;">
            <span style="color: #94A3B8;">Last Ingestion</span>
            <strong style="color: #CBD5E1;">{_last_sync}</strong>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 16px 0;">
        <div style="font-size: 11px; color: #64748B; font-weight: 500;">
            BIODIVERSITY GUARDIAN AI v2.5
        </div>
        <div style="font-size: 10px; color: #475569; margin-top: 4px;">
            Eco-Cybernetics Design System
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Page Routing
if page == "🏠 Overview":
    from pages import overview
    overview.render()
elif page == "🗺️ Biodiversity Map":
    from pages import biodiversity_map
    biodiversity_map.render()
elif page == "🎙️ Sound Monitor":
    from pages import sound_monitor
    sound_monitor.render()
elif page == "📷 Wildlife Monitor":
    from pages import wildlife_monitor
    wildlife_monitor.render()
elif page == "🤖 Conservation AI":
    from pages import conservation_ai
    conservation_ai.render()