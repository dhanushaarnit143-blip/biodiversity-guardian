import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def render():
    st.title("🤖 Conservation AI")
    st.markdown("AI-powered conservation recommendations based on ecosystem analysis")

    st.subheader("Current Ecosystem Status")

    col1, col2, col3 = st.columns(3)
    with col1:
        risk = st.selectbox("Risk Level", ["LOW", "MODERATE", "HIGH", "CRITICAL"], index=1)
    with col2:
        shannon = st.slider("Shannon Index", 0.0, 5.0, 3.28, 0.01)
    with col3:
        richness = st.number_input("Species Count", 1, 100, 34)

    st.subheader("Environmental Conditions")
    col4, col5, col6 = st.columns(3)
    with col4:
        temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 28.5)
    with col5:
        rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0, 120.0)
    with col6:
        vegetation = st.slider("Vegetation Index", 0.0, 1.0, 0.55, 0.01)

    if st.button("🤖 Generate Recommendation", type="primary"):
        with st.spinner("Analyzing ecosystem data..."):
            try:
                from conservation_agent import ConservationAgent
                from biodiversity.metrics import calculate_biodiversity_score

                risk_result = {
                    "risk_level": risk,
                    "confidence": 0.85,
                }
                biodiversity = {
                    "shannon_index": shannon,
                    "species_richness": richness,
                    "evenness": shannon / 3.5 if shannon > 0 else 0,
                }
                env = {
                    "temperature": temperature,
                    "rainfall": rainfall,
                    "vegetation_index": vegetation,
                }
                changes = []
                if shannon < 3.0:
                    changes.append({"metric": "shannon_index", "direction": "declining", "severity": "high", "z_score": -2.5})
                if richness < 25:
                    changes.append({"metric": "species_richness", "direction": "declining", "severity": "moderate", "z_score": -1.8})
                if temperature > 35:
                    changes.append({"metric": "temperature", "direction": "above_normal", "severity": "moderate", "z_score": 2.1})

                agent = ConservationAgent()
                recommendation = agent.generate_recommendation(risk_result, biodiversity, env, changes)

                st.subheader("Conservation Recommendation")
                st.markdown(recommendation)

            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Ask a Question")
    question = st.text_input("Enter your conservation question:")

    if question:
        with st.spinner("Thinking..."):
            try:
                from conservation_agent import ConservationAgent
                agent = ConservationAgent()
                response = agent.generate_recommendation(
                    {"risk_level": "MODERATE", "confidence": 0.7},
                    {"shannon_index": 3.28, "species_richness": 34, "evenness": 0.94},
                    {"temperature": 28.5, "rainfall": 120, "vegetation_index": 0.55},
                    []
                )
                st.markdown(response)
            except Exception as e:
                st.error(f"Error: {e}")