"""Biodiversity Map - Spatial Ecosystem Risk & Telemetry."""
import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go
import pandas as pd

from components.styles import (
    render_header, apply_plotly_theme, PRIMARY_EMERALD, RISK_COLORS
)

ZONES_DATA = [
    {
        "id": "ZA",
        "name": "Wetland Zone A (Lagoa das Araras)",
        "lat": -16.82,
        "lon": -56.24,
        "risk": "HIGH",
        "species": 37,
        "shannon": 3.22,
        "trend": -18.4,
        "ndvi": 0.52,
        "soil_moisture": "24%",
        "temp": "31.2°C",
        "threat": "Rapid seasonal water retreat & high evaporation",
        "key_species": ["Pantanal Treefrog", "Jabiru Stork", "Marsh Deer", "Capybara"]
    },
    {
        "id": "ZB",
        "name": "Forest Corridor Zone B (Mata Virgem)",
        "lat": -17.15,
        "lon": -56.81,
        "risk": "LOW",
        "species": 58,
        "shannon": 4.15,
        "trend": +2.8,
        "ndvi": 0.84,
        "soil_moisture": "58%",
        "temp": "25.6°C",
        "threat": "Stable microclimate; nominal bioacoustic density",
        "key_species": ["Jaguar", "Ocelot", "Blue-and-Yellow Macaw", "Howler Monkey"]
    },
    {
        "id": "ZC",
        "name": "Savanna Transition C (Cerrado Ridge)",
        "lat": -16.35,
        "lon": -57.02,
        "risk": "MODERATE",
        "species": 29,
        "shannon": 3.42,
        "trend": -6.2,
        "ndvi": 0.61,
        "soil_moisture": "32%",
        "temp": "29.8°C",
        "threat": "Cattle grazing pressure along northern buffer",
        "key_species": ["Maned Wolf", "Giant Anteater", "Seriema", "Armadillo"]
    },
    {
        "id": "ZD",
        "name": "Riparian River Delta D (Rio Claro Basin)",
        "lat": -16.94,
        "lon": -55.95,
        "risk": "HIGH",
        "species": 42,
        "shannon": 3.18,
        "trend": -15.1,
        "ndvi": 0.68,
        "soil_moisture": "44%",
        "temp": "28.4°C",
        "threat": "Sediment runoff from upstream agricultural clearing",
        "key_species": ["Giant River Otter", "Caiman", "Kingfisher", "Anhinga"]
    },
    {
        "id": "ZE",
        "name": "Highland Plateau E (Serra do Amolar)",
        "lat": -17.38,
        "lon": -56.32,
        "risk": "CRITICAL",
        "species": 16,
        "shannon": 2.18,
        "trend": -34.5,
        "ndvi": 0.41,
        "soil_moisture": "19%",
        "temp": "34.1°C",
        "threat": "Wildfire burn scar recovery zone; acute canopy loss",
        "key_species": ["Puma (Transient)", "Lizards", "Dry-scrub Finches"]
    },
]


def render():
    render_header()
    st.markdown("### 🗺️ Geospatial Ecosystem Risk & Sensor Telemetry")
    st.markdown("Real-time Passive Acoustic & Camera Trap spatial nodes overlaid on ecological risk contours.")

    # Filter Controls
    col_f1, col_f2, col_f3 = st.columns([1.5, 1.5, 2.0])
    with col_f1:
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            ["CRITICAL", "HIGH", "MODERATE", "LOW"],
            default=["CRITICAL", "HIGH", "MODERATE", "LOW"]
        )
    with col_f2:
        map_style = st.selectbox(
            "Map Layer",
            ["CartoDB DarkMatter (Night Ops)", "OpenStreetMap (Topographic)", "Satellite Sim (High-Res)"],
            index=0
        )
    with col_f3:
        st.markdown(
            """
            <div style="display: flex; gap: 0.8rem; align-items: center; margin-top: 1.8rem; font-size: 0.8rem;">
                <span>🟢 Low (Healthy)</span>
                <span>🟡 Moderate</span>
                <span>🟠 High</span>
                <span>🔴 Critical</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Filtered Zones
    filtered_zones = [z for z in ZONES_DATA if z["risk"] in risk_filter]

    # Folium Map Setup
    tiles_map = {
        "CartoDB DarkMatter (Night Ops)": "CartoDB dark_matter",
        "OpenStreetMap (Topographic)": "OpenStreetMap",
        "Satellite Sim (High-Res)": "CartoDB Positron"
    }

    center_lat = -16.85
    center_lon = -56.45
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles=tiles_map.get(map_style, "CartoDB dark_matter")
    )

    color_hex_map = {
        "LOW": "#10B981",
        "MODERATE": "#F59E0B",
        "HIGH": "#F97316",
        "CRITICAL": "#EF4444"
    }

    for zone in filtered_zones:
        color = color_hex_map[zone["risk"]]
        trend_arrow = "↓" if zone["trend"] < 0 else "↑"
        
        # Outer buffer ring (indicating monitoring range)
        folium.Circle(
            location=[zone["lat"], zone["lon"]],
            radius=14000,
            color=color,
            weight=1.5,
            fill=True,
            fill_color=color,
            fill_opacity=0.12,
        ).add_to(m)

        # Center pulse marker
        popup_html = f"""
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; color: #0F172A; width: 230px; padding: 4px;">
            <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 4px;">{zone['name']}</div>
            <div style="display: inline-block; background: {color}20; color: {color}; border: 1px solid {color}; padding: 2px 8px; border-radius: 12px; font-weight: 700; font-size: 0.75rem; margin-bottom: 8px;">
                RISK: {zone['risk']} ({trend_arrow} {abs(zone['trend'])}%)
            </div>
            <div style="font-size: 0.85rem; line-height: 1.4; color: #334155;">
                • <strong>Shannon Index:</strong> {zone['shannon']}<br/>
                • <strong>Species Count:</strong> {zone['species']} taxa<br/>
                • <strong>Canopy NDVI:</strong> {zone['ndvi']}<br/>
                • <strong>Soil Moisture:</strong> {zone['soil_moisture']}<br/>
            </div>
            <div style="font-size: 0.78rem; color: #64748B; margin-top: 6px; border-top: 1px solid #E2E8F0; padding-top: 4px;">
                <em>{zone['threat']}</em>
            </div>
        </div>
        """
        
        folium.CircleMarker(
            location=[zone["lat"], zone["lon"]],
            radius=8,
            color="#FFFFFF",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=280)
        ).add_to(m)

    # Render map
    folium_static(m, width=1280, height=480)

    # Zone Inspector Section
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🔬 Detailed Sector Intelligence & Microclimate")

    selected_zone_name = st.selectbox(
        "Select Monitoring Sector for Diagnostic Deep-Dive:",
        [z["name"] for z in ZONES_DATA],
        index=0
    )
    zone = next(z for z in ZONES_DATA if z["name"] == selected_zone_name)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Biodiversity Index (H')", f"{zone['shannon']}", delta=f"{zone['trend']}%")
    with c2:
        st.metric("Species Richness", f"{zone['species']} Taxa", delta=f"{len(zone['key_species'])} key bio-indicators")
    with c3:
        st.metric("Canopy Health (NDVI)", f"{zone['ndvi']}", delta="Optimal > 0.75" if zone['ndvi'] > 0.75 else "Stress Detected", delta_color="normal" if zone['ndvi'] > 0.75 else "inverse")
    with c4:
        st.metric("Soil Moisture Index", zone['soil_moisture'], delta="Volumetric")
    with c5:
        st.metric("Surface Temp Anomaly", zone['temp'], delta="+2.4°C vs 10yr avg", delta_color="inverse")

    # Diagnostic & Key Species Pill
    st.markdown(
        f"""
        <div class="glass-panel" style="margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 0.8rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Primary Ecological Driver:</span>
                    <p style="font-size: 0.95rem; color: #F1F5F9; margin: 4px 0 0 0;">
                        {zone['threat']}
                    </p>
                </div>
                <div>
                    <span style="font-size: 0.8rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Key Bio-Indicator Species:</span>
                    <div style="display: flex; gap: 0.5rem; margin-top: 4px;">
                        {' '.join([f'<span style="background: rgba(16,185,129,0.15); color: #34D399; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">{sp}</span>' for sp in zone['key_species']])}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
