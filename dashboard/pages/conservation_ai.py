"""Conservation AI - LLM-Powered Decision Support & Threat Mitigation Agent."""
import streamlit as st
import sys
from pathlib import Path
from components.styles import render_header, PRIMARY_EMERALD

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def render():
    render_header()
    st.markdown("### 🤖 Conservation Intelligence Agent & Ecosystem Decision Support")
    st.markdown("Multimodal LLM reasoning over bioacoustic, camera trap, climate & satellite telemetry to generate actionable conservation strategy.")

    # Current System Status Cards
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("Current Risk Level", "HIGH", "⚠️", "warning"),
        ("Shannon Diversity (H')", "3.28", "📊", "info"),
        ("Active Alerts", "7 Zones", "🚨", "danger"),
        ("Next Satellite Sync", "T-4h 23m", "🛰️", "info")
    ]
    for col, (title, val, icon, tone) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card {tone}">
                <div class="metric-title">{icon} {title}</div>
                <div class="metric-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Input Section - Natural Language Query + Structured Inputs
    st.markdown("#### 🧠 Ask the Conservation Intelligence Agent")
    
    query_type = st.radio(
        "Interaction Mode:",
        ["💬 Natural Language Query", "⚙️ Structured Scenario Builder"],
        horizontal=True
    )

    if query_type == "💬 Natural Language Query":
        user_question = st.text_area(
            "Enter your conservation question:",
            placeholder="e.g., 'Why is amphibian diversity collapsing in Wetland Zone A despite stable rainfall?' or 'Generate a 30-day intervention plan for Highland Plateau E recovery.'",
            height=100
        )
        
        col_btn, col_ctx = st.columns([1, 3])
        with col_btn:
            if st.button("🚀 Generate Recommendation", type="primary", use_container_width=True):
                if user_question:
                    with st.spinner("Processing multimodal ecosystem context through conservation reasoning engine..."):
                        # Simulate LLM response
                        response = generate_mock_response(user_question)
                        st.session_state.conservation_response = response
                else:
                    st.warning("Please enter a question first.")
    
    else:
        st.markdown("##### Build Custom Conservation Scenario")
        c1, c2 = st.columns(2)
        with c1:
            zone = st.selectbox("Target Sector", ["Wetland Zone A", "Forest Corridor B", "Savanna C", "Riparian D", "Highland E"])
            intervention = st.selectbox("Intervention Type", ["Hydrological Restoration", "Fire Break Establishment", "Anti-Poaching Patrol", "Invasive Species Removal", "Corridor Reforestation"])
        with c2:
            budget = st.slider("Available Budget ($USD)", 10000, 1000000, 250000, step=10000)
            timeline = st.selectbox("Timeline", ["Emergency (7 days)", "Short-term (30 days)", "Medium (90 days)", "Long-term (1 year)"])
        
        if st.button("📋 Generate Strategic Plan", type="primary", use_container_width=True):
            with st.spinner("Synthesizing adaptive management plan..."):
                prompt = f"Create a {timeline} intervention plan for {intervention} in {zone} with ${budget:,} budget."
                response = generate_mock_response(prompt)
                st.session_state.conservation_response = response

    # Display Response
    if "conservation_response" in st.session_state:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown(st.session_state.conservation_response, unsafe_allow_html=True)

    # Quick Action Buttons
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("#### ⚡ Rapid Assessment Protocols")
    
    quick_cols = st.columns(4)
    quick_actions = [
        ("📊 Weekly Biodiversity Report", "Generate automated 7-day trend summary for all 5 sectors"),
        ("🔥 Fire Risk Forecast", "72-hour wildfire probability mapping from thermal + NDVI anomaly"),
        ("💧 Hydrological Stress Index", "Real-time water availability vs population demand model"),
        ("🛡️ Poaching Threat Score", "Camera trap + acoustic anomaly correlation for illegal activity")
    ]
    
    for i, (title, desc) in enumerate(quick_actions):
        with quick_cols[i]:
            if st.button(title, use_container_width=True):
                st.info(f"Executing: {desc}")

    # Knowledge Base
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    with st.expander("📚 Conservation Knowledge Base & Protocol Library"):
        st.markdown("""
        **Standard Operating Procedures:**
        - **PAM-001:** Passive Acoustic Monitoring Deployment & Calibration
        - **CT-002:** Camera Trap Grid Stratification (2km × 2km resolution)
        - **RS-003:** Remote Sensing NDVI/EVI Change Detection Thresholds (>15% = Alert)
        - **IR-004:** Intervention Response Timeline (Critical: <48h | High: <7d | Mod: <30d)
        
        **Key References:**
        - IUCN Red List Assessment Criteria v3.1
        - CBD Aichi Targets & Post-2020 Global Biodiversity Framework
        - Pantanal Conservation Action Plan (ICMBio/MMA Brazil)
        - SHAP Explainability Standards for Ecological ML (Lundberg et al.)
        """)


def generate_mock_response(question: str) -> str:
    """Generate contextual conservation response based on question type."""
    q = question.lower()
    
    if any(kw in q for kw in ['amphibian', 'frog', 'treefrog', 'wetland']):
        return f"""
        <div class="glass-panel" style="border-left: 4px solid #EF4444;">
            <div style="font-size: 0.8rem; color: #EF4444; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem;">
                🚨 CRITICAL PRIORITY — Amphibian Hydrological Collapse
            </div>
            
            <h4 style="color: #F8FAFC; margin: 0.5rem 0;">Diagnosis: Pantanal Treefrog (Dendropsophus) Population Decline</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                <div class="glass-panel">
                    <strong style="color: #34D399;">Confirmed Drivers:</strong>
                    <ul style="margin: 0.5rem 0; padding-left: 1.2rem; color: #CBD5E1; font-size: 0.88rem;">
                        <li>Surface water extent ↓ 18% (Sentinel-2, 90d)</li>
                        <li>Soil moisture ↓ to 24% (SMAP satellite)</li>
                        <li>Peak temp +2.4°C above 10yr mean</li>
                        <li>Chorus amplitude ↓ 42% (PAM, 90d)</li>
                    </ul>
                </div>
                <div class="glass-panel">
                    <strong style="color: #F59E0B;">Contributing Factors:</strong>
                    <ul style="margin: 0.5rem 0; padding-left: 1.2rem; color: #CBD5E1; font-size: 0.88rem;">
                        <li>Upstream cattle ranch drainage channels</li>
                        <li>Delayed wet season onset (ENSO transition)</li>
                        <li>Chytrid fungus eDNA detected (Seq: BR-PT-2024)</li>
                    </ul>
                </div>
            </div>

            <h4 style="color: #F8FAFC;">🛡️ Recommended Immediate Actions (T-0 to T+14 days):</h4>
            <ol style="color: #CBD5E1; line-height: 1.8; padding-left: 1.2rem; font-size: 0.9rem;">
                <li><strong>Emergency Hydrological Intervention:</strong> Deploy 3 solar pumps to maintain 40cm water depth in 5 core breeding pools (Cost: ~$18K).</li>
                <li><strong>Disease Surveillance:</strong> Immediate eDNA sampling + skin swab protocol across 15 sites for Bd/Bsal detection.</li>
                <li><strong>Temporary Exclusion Zones:</strong> Fence 2.5km perimeter around Zone A breeding nucleus; restrict cattle access.</li>
                <li><strong>Acoustic Monitoring Surge:</strong> Increase PAM sampling to 15-min intervals; enable real-time threshold alerts.</li>
                <li><strong>Stakeholder Coordination:</strong> Engage upstream ranchers for voluntary wetland retention (payment for ecosystem services).</li>
            </ol>

            <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(16,185,129,0.1); border-radius: 8px; border: 1px solid rgba(16,185,129,0.3);">
                <strong style="color: #34D399;">Decision Confidence: 89%</strong> | <strong style="color: #38BDF8;">SHAP Primary Drivers:</strong> Soil Moisture (0.34) | Temp Anomaly (0.28) | NDVI Trend (0.18) | Chorus Index (0.12)
            </div>
        </div>
        """
    
    elif any(kw in q for kw in ['fire', 'wildfire', 'burn', 'highland', 'plateau']):
        return f"""
        <div class="glass-panel" style="border-left: 4px solid #F97316;">
            <div style="font-size: 0.8rem; color: #F97316; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem;">
                🔥 HIGH PRIORITY — Post-Fire Landscape Recovery
            </div>
            
            <h4 style="color: #F8FAFC; margin: 0.5rem 0;">Scenario: Highland Plateau E (Serra do Amolar) Burn Scar Recovery</h4>
            
            <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6;">
            The 34.5% Shannon Index collapse is driven by canopy loss (>60% tree cover), 
            resulting in microclimate desiccation and predator release on ground-dwelling taxa.
            </p>

            <h4 style="color: #F8FAFC;">🌱 90-Day Adaptive Restoration Protocol:</h4>
            <ol style="color: #CBD5E1; line-height: 1.8; padding-left: 1.2rem; font-size: 0.9rem;">
                <li><strong>Phase 1 (Days 1-14):</strong> Establish 15km firebreaks using controlled mosaic burning; deploy drone seeding of fire-adapted native grasses (Paspalum, Andropogon).</li>
                <li><strong>Phase 2 (Days 15-45):</strong> Install 50 artificial water points; plant 2000 native saplings (Handroanthus, Tabebuia) in erosion gullies.</li>
                <li><strong>Phase 3 (Days 46-90):</strong> Camera trap grid reactivation; bioacoustic baseline re-establishment; predator exclusion fencing for recovering small mammal populations.</li>
            </ol>

            <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(249,115,22,0.1); border-radius: 8px; border: 1px solid rgba(249,115,22,0.3);">
                <strong style="color: #FB923C;">Estimated Budget: $185,000</strong> | <strong style="color: #38BDF8;">Key Metric:</strong> Target H' ≥ 2.8 by Day 90
            </div>
        </div>
        """

    else:
        return f"""
        <div class="glass-panel" style="border-left: 4px solid #10B981;">
            <div style="font-size: 0.8rem; color: #10B981; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem;">
                📋 STRATEGIC ASSESSMENT — Multimodal Ecosystem Intelligence
            </div>
            
            <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem;">
            Based on your query: <em style="color: #38BDF8;">"{question}"</em>
            </p>

            <h4 style="color: #F8FAFC;">🔍 Cross-Modal Evidence Synthesis:</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 0.8rem; margin: 1rem 0;">
                <div class="glass-panel" style="border-left: 3px solid #10B981;">
                    <strong style="color: #34D399;">Bioacoustic (PAM)</strong><br/>
                    <span style="color: #CBD5E1; font-size: 0.85rem;">142 hrs analyzed • 18 spp vocal • 3 declining chorus</span>
                </div>
                <div class="glass-panel" style="border-left: 3px solid #38BDF8;">
                    <strong style="color: #38BDF8;">Camera Traps (CT)</strong><br/>
                    <span style="color: #CBD5E1; font-size: 0.85rem;">2,840 trap-nights • 28 spp detected • 7 new records</span>
                </div>
                <div class="glass-panel" style="border-left: 3px solid #F59E0B;">
                    <strong style="color: #F59E0B;">Climate Telemetry</strong><br/>
                    <span style="color: #CBD5E1; font-size: 0.85rem;">Temp +1.8°C • Rainfall -12% • VPD +23%</span>
                </div>
                <div class="glass-panel" style="border-left: 3px solid #EF4444;">
                    <strong style="color: #EF4444;">Satellite (Sentinel)</strong><br/>
                    <span style="color: #CBD5E1; font-size: 0.85rem;">NDVI -0.08 • Water -18% • Fire alerts: 3 active</span>
                </div>
            </div>

            <h4 style="color: #F8FAFC;">🎯 Prioritized Conservation Actions:</h4>
            <ol style="color: #CBD5E1; line-height: 1.7; padding-left: 1.2rem; font-size: 0.9rem;">
                <li><strong>Zone A (Wetland):</strong> Emergency hydrological intervention — Priority 1 (Amphibian collapse)</li>
                <li><strong>Zone E (Highland):</strong> Post-fire restoration & predator exclusion — Priority 1 (Canopy loss)</li>
                <li><strong>Zone D (Riparian):</strong> Sediment trap installation upstream — Priority 2 (Water quality)</li>
                <li><strong>Zone C (Savanna):</strong> Grazing management agreement with landowners — Priority 2 (Habitat pressure)</li>
                <li><strong>Zone B (Forest):</strong> Maintain passive monitoring; no immediate intervention — Priority 3 (Stable)</li>
            </ol>

            <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(16,185,129,0.1); border-radius: 8px; border: 1px solid rgba(16,185,129,0.3);">
                <strong style="color: #34D399;">Overall Ecosystem Health Score: 67/100</strong> | 
                <strong style="color: #38BDF8;">Trend: Declining (-4.2% QoQ)</strong> | 
                <strong style="color: #F59E0B;">Next Full Assessment: 2026-10-14</strong>
            </div>
        </div>
        """