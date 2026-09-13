"""Explainable AI for biodiversity risk predictions using SHAP."""
import json
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BiodiversityExplainer:
    def __init__(self):
        self.factor_descriptions = {
            "shannon_index": "Species diversity (Shannon Index)",
            "species_richness": "Number of unique species",
            "evenness": "Distribution balance across species",
            "temperature": "Ambient temperature",
            "humidity": "Relative humidity",
            "rainfall": "Precipitation levels",
            "vegetation_index": "Vegetation health (NDVI)",
            "soil_moisture": "Soil water content",
            "shannon_trend": "Trend in species diversity over time",
            "species_trend": "Trend in species count over time",
            "human_activity_index": "Human disturbance level",
            "habitat_fragmentation": "Habitat connectivity loss",
        }

    def format_explanation(self, shap_result: dict, risk_result: dict) -> dict:
        top_factors = shap_result.get("top_factors", [])
        risk_level = risk_result.get("risk_level", "UNKNOWN")
        confidence = risk_result.get("confidence", 0)

        human_readable = []
        for name, value in top_factors:
            desc = self.factor_descriptions.get(name, name)
            direction = "increasing risk" if value > 0 else "decreasing risk"
            strength = abs(value)
            bar = self._create_bar(strength)
            human_readable.append({
                "factor": desc,
                "impact": round(value, 4),
                "direction": direction,
                "bar": bar,
            })

        return {
            "risk_level": risk_level,
            "confidence": confidence,
            "explanations": human_readable,
            "summary": self._build_summary(risk_level, human_readable),
        }

    def _create_bar(self, strength: float) -> str:
        normalized = min(1.0, strength / 0.5)
        filled = int(normalized * 20)
        return "█" * filled + "░" * (20 - filled)

    def _build_summary(self, risk_level: str, explanations: list) -> str:
        if risk_level == "LOW":
            prefix = "Ecosystem health is stable."
        elif risk_level == "MODERATE":
            prefix = "Some concerning trends detected."
        elif risk_level == "HIGH":
            prefix = "Significant biodiversity risks identified."
        else:
            prefix = "Critical ecosystem degradation detected."

        top_3 = explanations[:3]
        factors = ", ".join([e["factor"].lower() for e in top_3])
        return f"{prefix} Primary contributing factors: {factors}."

    def generate_report(self, shap_result: dict, risk_result: dict, species_changes: Optional[dict] = None) -> str:
        explanation = self.format_explanation(shap_result, risk_result)
        lines = [
            f"BIODIVERSITY RISK: {explanation['risk_level']}",
            f"Confidence: {explanation['confidence']:.1%}",
            "",
            "Top contributing factors:",
        ]
        for exp in explanation["explanations"]:
            lines.append(f"  {exp['factor']:<30s} {exp['bar']} ({exp['direction']})")

        if species_changes:
            declining = [sp for sp, info in species_changes.items() if info.get("status") == "declining"]
            if declining:
                lines.extend(["", "Declining species:"])
                for sp in declining[:10]:
                    info = species_changes[sp]
                    lines.append(f"  - {sp}: {info['change_pct']}% change")

        lines.extend(["", explanation["summary"]])
        return "\n".join(lines)