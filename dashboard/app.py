import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

st.set_page_config(
    page_title="Biodiversity Guardian AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("🌿 Biodiversity Guardian")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Overview", "🗺️ Biodiversity Map", "🎙️ Sound Monitor", "📷 Wildlife Monitor", "🤖 Conservation AI"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Ecosystem Monitoring Platform**")
st.sidebar.markdown("AI-powered biodiversity conservation")

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