import streamlit as st
import folium
from streamlit_folium import folium_static

def render():
    st.title("🗺️ Biodiversity Map")
    st.markdown("Interactive ecosystem monitoring zones")

    m = folium.Map(location=[-16.5, -56.5], zoom_start=6, tiles="OpenStreetMap")

    zones = [
        {"name": "Wetland Zone A", "lat": -16.8, "lon": -56.2, "risk": "HIGH", "species": 37, "index": 3.82, "trend": -14},
        {"name": "Forest Zone B", "lat": -17.1, "lon": -56.8, "risk": "LOW", "species": 52, "index": 4.12, "trend": 3},
        {"name": "Grassland Zone C", "lat": -16.3, "lon": -57.0, "risk": "MODERATE", "species": 28, "index": 3.45, "trend": -7},
        {"name": "Riparian Zone D", "lat": -16.9, "lon": -55.9, "risk": "HIGH", "species": 31, "index": 3.21, "trend": -18},
        {"name": "Highland Zone E", "lat": -17.3, "lon": -56.3, "risk": "CRITICAL", "species": 15, "index": 2.15, "trend": -32},
    ]

    risk_colors = {"LOW": "green", "MODERATE": "orange", "HIGH": "red", "CRITICAL": "darkred"}

    for zone in zones:
        color = risk_colors[zone["risk"]]
        trend_arrow = "↓" if zone["trend"] < 0 else "↑"
        popup_html = f"""
        <div style='width:200px'>
            <b>{zone['name']}</b><br>
            Species: {zone['species']}<br>
            Index: {zone['index']}<br>
            Trend: {trend_arrow} {abs(zone['trend'])}%<br>
            Risk: <b style='color:{color}'>{zone['risk']}</b>
        </div>
        """
        folium.Marker(
            [zone["lat"], zone["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(m)

    folium_static(m, width=800, height=500)

    st.markdown("---")
    st.subheader("Zone Details")
    selected_zone = st.selectbox("Select a zone:", [z["name"] for z in zones])
    zone = next(z for z in zones if z["name"] == selected_zone)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Species Count", zone["species"])
    with col2:
        st.metric("Biodiversity Index", zone["index"])
    with col3:
        st.metric("Trend", f"{zone['trend']}%", delta_color="inverse")