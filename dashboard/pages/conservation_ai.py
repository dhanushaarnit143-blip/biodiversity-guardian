"""Conservation AI — LLM-Powered Decision Support & Threat Mitigation Agent.

Fully compliant with the Global Design System:
- Panchang typography
- 60/30/10 color rule (Obsidian/Emerald)
- 8-point spacing system
- 12/8/4 column responsive grid
- Glassmorphism cards
- Consistent component patterns
"""
import streamlit as st
import sys
from pathlib import Path

from components.styles import (
    load_design_system,
    render_header,
    render_section_header,
    render_glass_panel,
    render_metric_card,
    render_alert,
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))


def render():
    load_design_system()
    
    render_header(
        sensors_online="72 / 72",
        satellite_status="LIVE SYNC"
    )

    # Current System Status Cards
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
    metrics = [
        ("Current Risk Level", "HIGH", "⚠️", "warning"),
        ("Shannon Diversity (H')", "3.28", "📊", "info"),
        ("Active Alerts", "7 Zones", "🚨", "danger"),
        ("Next Satellite Sync", "T-4h 23m", "🛰️", "info")
    ]
    
    for col, (title, val, icon, tone) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(render_metric_card(
                title=title,
                value=val,
                icon=icon,
                tone=tone
            ), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Input Section - Natural Language Query + Structured Inputs
    st.markdown(render_section_header(
        "Conservation Intelligence Agent",
        "Multimodal LLM reasoning over bioacoustic, camera trap, climate & satellite telemetry"
    ), unsafe_allow_html=True)
    
    query_type = st.radio(
        "Interaction Mode:",
        ["💬 Natural Language Query", "⚙️ Structured Scenario Builder"],
        horizontal=True,
        key="conservation_query_mode"
    )

    if query_type == "💬 Natural Language Query":
        user_question = st.text_area(
            "Enter your conservation question:",
            placeholder="e.g., 'Why is amphibian diversity collapsing in Wetland Zone A despite stable rainfall?' or 'Generate a 30-day intervention plan for Highland Plateau E recovery.'",
            height=100,
            key="conservation_question"
        )
        
        col_btn, col_ctx = st.columns([1, 3])
        with col_btn:
            if st.button("🚀 Generate Recommendation", type="primary", use_container_width=True, key="conservation_generate"):
                if user_question:
                    with st.spinner("Processing multimodal ecosystem context through conservation reasoning engine..."):
                        response = generate_mock_response(user_question)
                        st.session_state.conservation_response = response
                else:
                    st.warning("Please enter a question first.")
    
    else:
        st.markdown(
            render_section_header(
                "Build Custom Conservation Scenario",
                "Define parameters for targeted intervention planning"
            ), unsafe_allow_html=True
        )
        c1, c2 = st.columns(2)
        with c1:
            zone = st.selectbox("Target Sector", ["Wetland Zone A", "Forest Corridor B", "Savanna C", "Riparian D", "Highland E"], key="conservation_zone")
            intervention = st.selectbox("Intervention Type", ["Hydrological Restoration", "Fire Break Establishment", "Anti-Poaching Patrol", "Invasive Species Removal", "Corridor Reforestation"], key="conservation_intervention")
        with c2:
            budget = st.slider("Available Budget ($USD)", 10000, 1000000, 250000, step=10000, key="conservation_budget")
            timeline = st.selectbox("Timeline", ["Emergency (7 days)", "Short-term (30 days)", "Medium (90 days)", "Long-term (1 year)"], key="conservation_timeline")
        
        if st.button("📋 Generate Strategic Plan", type="primary", use_container_width=True, key="conservation_plan_btn"):
            with st.spinner("Synthesizing adaptive management plan..."):
                prompt = f"Create a {timeline} intervention plan for {intervention} in {zone} with ${budget:,} budget."
                response = generate_mock_response(prompt)
                st.session_state.conservation_response = response

    # Display Response
    if "conservation_response" in st.session_state:
        st.markdown(f"<div style='margin-top: {SPACING['lg']};'></div>", unsafe_allow_html=True)
        st.markdown(st.session_state.conservation_response, unsafe_allow_html=True)

    # Quick Action Buttons
    st.markdown(f"<div style='margin-top: {SPACING['2xl']};'></div>", unsafe_allow_html=True)
    st.markdown(
        render_section_header(
            "Rapid Assessment Protocols",
            "One-click execution of standardized conservation workflows"
        ), unsafe_allow_html=True
    )
    
    quick_cols = st.columns(4)
    quick_actions = [
        ("📊 Weekly Biodiversity Report", "Generate automated 7-day trend summary for all 5 sectors"),
        ("🔥 Fire Risk Forecast", "72-hour wildfire probability mapping from thermal + NDVI anomaly"),
        ("💧 Hydrological Stress Index", "Real-time water availability vs population demand model"),
        ("🛡️ Poaching Threat Score", "Camera trap + acoustic anomaly correlation for illegal activity")
    ]
    
    for i, (title, desc) in enumerate(quick_actions):
        with quick_cols[i]:
            if st.button(title, use_container_width=True, key=f"quick_action_{i}"):
                st.info(f"Executing: {desc}")

    # Knowledge Base
    st.markdown(f"<div style='margin-top: {SPACING['2xl']};'></div>", unsafe_allow_html=True)
    with st.expander("📚 Conservation Knowledge Base & Protocol Library", expanded=False):
        st.markdown(f"""
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
        <div class="glass-panel" style="border-left: 4px solid #EF4444; padding: 24px;">
            <div style="font-size: 12px; color: #EF4444; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                🚨 CRITICAL PRIORITY — Amphibian Hydrological Collapse
            </div>
            
            <h4 style="color: #F8FAFC; margin: 0 0 16px 0;">Diagnosis: Pantanal Treefrog (Dendropsophus) Population Decline</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0;">
                <div class="glass-panel" style="padding: 16px;">
                    <strong style="color: #34D399;">Confirmed Drivers:</strong>
                    <ul style="margin: 8px 0 0 0; padding-left: 20px; color: #CBD5E1; font-size: 13px; line-height: 1.8;">
                        <li>Surface water extent ↓ 18% (Sentinel-2, 90d)</li>
                        <li>Soil moisture ↓ to 24% (SMAP satellite)</li>
                        <li>Peak temp +2.4°C above 10yr mean</li>
                        <li>Chorus amplitude ↓ 42% (PAM, 90d)</li>
                    </ul>
                </div>
                <div class="glass-panel" style="padding: 16px;">
                    <strong style="color: #F59E0B;">Contributing Factors:</strong>
                    <ul style="margin: 8px 0 0 0; padding-left: 20px; color: #CBD5E1; font-size: 13px; line-height: 1.8;">
                        <li>Upstream cattle ranch drainage channels</li>
                        <li>Delayed wet season onset (ENSO transition)</li>
                        <li>Chytrid fungus eDNA detected (Seq: BR-PT-2024)</li>
                    </ul>
                </div>
            </div>

            <h4 style="color: #F8FAFC; margin: 16px 0 12px 0;">🛡️ Recommended Immediate Actions (T-0 to T+14 days):</h4>
            <ol style="color: #CBD5E1; line-height: 2; padding-left: 20px; font-size: 14px;">
                <li><strong>Emergency Hydrological Intervention:</strong> Deploy 3 solar pumps to maintain 40cm water depth in 5 core breeding pools (Cost: ~$18K).</li>
                <li><strong>Disease Surveillance:</strong> Immediate eDNA sampling + skin swab protocol across 15 sites for Bd/Bsal detection.</li>
                <li><strong>Temporary Exclusion Zones:</strong> Fence 2.5km perimeter around Zone A breeding nucleus; restrict cattle access.</li>
                <li><strong>Acoustic Monitoring Surge:</strong> Increase PAM sampling to 15-min intervals; enable real-time threshold alerts.</li>
                <li><strong>Stakeholder Coordination:</strong> Engage upstream ranchers for voluntary wetland retention (payment for ecosystem services).</li>
            </ol>

            <div style="margin-top: 16px; padding: 16px; background: rgba(16,185,129,0.1); border-radius: 8px; border: 1px solid rgba(16,185,129,0.3);">
                <strong style="color: #34D399;">Decision Confidence: 89%</strong> | <strong style="color: #38BDF8;">SHAP Primary Drivers:</strong> Soil Moisture (0.34) | Temp Anomaly (0.28) | NDVI Trend (0.18) | Chorus Index (0.12)
            </div>
        </div>
        """
    
    elif any(kw in q for kw in ['fire', 'wildfire', 'burn', 'highland', 'plateau']):
        return f"""
        <div class="glass-panel" style="border-left: 4px solid #F97316; padding: 24px;">
            <div style="font-size: 12px; color: #F97316; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                🔥 HIGH PRIORITY — Post-Fire Landscape Recovery
            </div>
            
            <h4 style="color: #F8FAFC; margin: 0 0 16px 0;">Scenario: Highland Plateau E (Serra do Amolar) Burn Scar Recovery</h4>
            
            <p style="color: #CBD5E1; font-size: 14px; line-height: 1.7; margin-bottom: 16px;">
            The 34.5% Shannon Index collapse is driven by canopy loss (>60% tree cover), 
            resulting in microclimate desiccation and predator release on ground-dwelling taxa.
            </p>

            <h4 style="color: #F8FAFC; margin: 16px 0 12px 0;">🌱 90-Day Adaptive Restoration Protocol:</h4>
            <ol style="color: #CBD5E1; line-height: 2; padding-left: 20px; font-size: 14px;">
                <li><strong>Phase 1 (Days 1-14):</strong> Establish 15km firebreaks using controlled mosaic burning; deploy drone seeding of fire-adapted native grasses (Paspalum, Andropogon).</li>
                <li><strong>Phase 2 (Days 15-45):</strong> Install 50 artificial water points; plant 2000 native saplings (Handroanthus, Tabebuia) in erosion gullies.</li>
                <li><strong>Phase 3 (Days 46-90):</strong> Camera trap grid reactivation; bioacoustic baseline re-establishment; predator exclusion fencing for recovering small mammal populations.</li>
            </ol>

            <div style="margin-top: 16px; padding: 16px; background: rgba(249,115,22,0.1); border-radius: 8px; border: 1px solid rgba(249,115,22,0.3);">
                <strong style="color: #FB923C;">Estimated Budget: $185,000</strong> | <strong style="color: #38BDF8;">Key Metric:</strong> Target H' ≥ 2.8 by Day 90
            </div>
        </div>
        """

    else:
        return f"""
        <div class="glass-panel" style="border-left: 4px solid #10B981; padding: 24px;">
            <div style="font-size: 12px; color: #10B981; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                📋 STRATEGIC ASSESSMENT — Multimodal Ecosystem Intelligence
            </div>
            
            <p style="color: #CBD5E1; font-size: 14px; line-height: 1.7; margin-bottom: 16px;">
            Based on your query: <em style="color: #38BDF8;">"{question}"</em>
            </p>

            <h4 style="color: #F8FAFC; margin: 16px 0 12px 0;">🔍 Cross-Modal Evidence Synthesis:</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin: 16px 0;">
                <div class="glass-panel" style="border-left: 3px solid #10B981; padding: 16px;">
                    <strong style="color: #34D399;">Bioacoustic (PAM)</strong><br/>
                    <span style="color: #CBD5E1; font-size: 13px;">142 hrs analyzed • 18 spp vocal • 3 declining chorus</span>
                </div>
                <div class="glass-panel" style="border-left: 3px solid #38BDF8; padding: 16px;">
                    <strong style="color: #38BDF8;">Camera Traps (CT)</strong><br/>
                    <span style="color: #CBD5E1; font-size: 13px;">2,840 trap-nights • 28 spp detected • 7 new records</span>
                </div>
                <div class="glass-panel" style="border-left: 3px solid #F59E0B; padding: 16px;">
                    <strong style="color: #F59E0B;">Climate Telemetry</strong><br/>
                    <span style="color: #CBD5E1; font-size: 13px;">Temp +1.8°C • Rainfall -12% • VPD +23%</span>
                </div>
                <div class="glass-panel" style="border-left: 3px solid #EF4444; padding: 16px;">
                    <strong style="color: #EF4444;">Satellite (Sentinel)</strong><br/>
                    <span style="color: #CBD5E1; font-size: 13px;">NDVI -0.08 • Water -18% • Fire alerts: 3 active</span>
                </div>
            </div>

            <h4 style="color: #F8FAFC; margin: 16px 0 12px 0;">🎯 Prioritized Conservation Actions:</h4>
            <ol style="color: #CBD5E1; line-height: 2; padding-left: 20px; font-size: 14px;">
                <li><strong>Zone A (Wetland):</strong> Emergency hydrological intervention — Priority 1 (Amphibian collapse)</li>
                <li><strong>Zone E (Highland):</strong> Post-fire restoration & predator exclusion — Priority 1 (Canopy loss)</li>
                <li><strong>Zone D (Riparian):</strong> Sediment trap installation upstream — Priority 2 (Water quality)</li>
                <li><strong>Zone C (Savanna):</strong> Grazing management agreement with landowners — Priority 2 (Habitat pressure)</li>
                <li><strong>Zone B (Forest):</strong> Maintain passive monitoring; no immediate intervention — Priority 3 (Stable)</li>
            </ol>

            <div style="margin-top: 16px; padding: 16px; background: rgba(16,185,129,0.1); border-radius: 8px; border: 1px solid rgba(16,185,129,0.3);">
                <strong style="color: #34D399;">Overall Ecosystem Health Score: 67/100</strong> | 
                <strong style="color: #38BDF8;">Trend: Declining (-4.2% QoQ)</strong> | 
                <strong style="color: #F59E0B;">Next Full Assessment: 2026-10-14</strong>
            </div>
        </div>
        """