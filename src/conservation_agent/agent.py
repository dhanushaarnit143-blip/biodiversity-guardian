"""AI Conservation Agent using local LLM for recommendations."""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a biodiversity conservation expert AI assistant.
Your role is to analyze ecosystem data and provide actionable conservation recommendations.
Always be specific about which species or habitats are affected.
Frame recommendations as decision-support suggestions, not authoritative decisions.
Format responses with clear priority levels and actionable steps.
Keep responses concise (under 200 words)."""


class ConservationAgent:
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_name = model_name
        self._pipe = None

    @property
    def pipe(self):
        if self._pipe is None:
            try:
                from transformers import pipeline
                import torch
                self._pipe = pipeline(
                    "text-generation",
                    model=self.model_name,
                    torch_dtype=torch.float16,
                    device_map="auto",
                )
                logger.info(f"Loaded LLM: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to load LLM: {e}")
                return None
        return self._pipe

    def build_context(self, risk: dict, biodiversity: dict, env: dict, changes: list) -> str:
        changes_text = "\n".join([
            f"- {c.get('metric', 'unknown')}: {c.get('direction', 'changing')} "
            f"(severity: {c.get('severity', 'unknown')})"
            for c in changes
        ]) or "No significant changes detected."

        return f"""Analyze this ecosystem data and provide conservation recommendations:

RISK ASSESSMENT:
- Risk Level: {risk.get('risk_level', 'UNKNOWN')}
- Confidence: {risk.get('confidence', 0):.1%}

BIODIVERSITY METRICS:
- Shannon Index: {biodiversity.get('shannon_index', 'N/A')}
- Species Richness: {biodiversity.get('species_richness', 'N/A')}
- Evenness: {biodiversity.get('evenness', 'N/A')}

ENVIRONMENTAL CONDITIONS:
- Temperature: {env.get('temperature', 'N/A')}°C
- Rainfall: {env.get('rainfall', 'N/A')} mm
- Vegetation Index: {env.get('vegetation_index', 'N/A')}

DETECTED CHANGES:
{changes_text}

Provide:
1. Priority (HIGH/MEDIUM/LOW)
2. Primary concerns
3. Specific actionable recommendations
4. Monitoring suggestions"""

    def generate_recommendation(self, risk: dict, biodiversity: dict, env: dict, changes: list) -> str:
        context = self.build_context(risk, biodiversity, env, changes)

        if self.pipe is None:
            return self._fallback_recommendation(risk, biodiversity, changes)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context},
        ]

        try:
            response = self.pipe(messages, max_new_tokens=512, temperature=0.7, do_sample=True)
            return response[0]["generated_text"][-1]["content"]
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return self._fallback_recommendation(risk, biodiversity, changes)

    def _fallback_recommendation(self, risk: dict, biodiversity: dict, changes: list) -> str:
        risk_level = risk.get("risk_level", "UNKNOWN")
        shannon = biodiversity.get("shannon_index", 0)

        lines = [f"Priority: {'HIGH' if risk_level in ('HIGH', 'CRITICAL') else 'MEDIUM' if risk_level == 'MODERATE' else 'LOW'}"]
        lines.append(f"\nCurrent Risk Level: {risk_level}")
        lines.append(f"Biodiversity Score: {shannon:.2f}")

        declining = [c for c in changes if c.get("direction") in ("declining", "below_normal")]
        if declining:
            lines.append("\nKey Concerns:")
            for c in declining[:3]:
                lines.append(f"- {c.get('metric', 'unknown')}: {c.get('direction')} (z-score: {c.get('z_score', 'N/A')})")

        lines.append("\nRecommendations:")
        if risk_level in ("HIGH", "CRITICAL"):
            lines.append("- Increase monitoring frequency to weekly")
            lines.append("- Conduct ground-truth surveys in affected areas")
            lines.append("- Review habitat management practices")
        elif risk_level == "MODERATE":
            lines.append("- Continue regular monitoring")
            lines.append("- Investigate potential causes of decline")
            lines.append("- Consider protective measures for vulnerable species")
        else:
            lines.append("- Maintain current conservation practices")
            lines.append("- Continue baseline monitoring")

        return "\n".join(lines)