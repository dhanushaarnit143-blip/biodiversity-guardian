"""Biodiversity index calculator for ecosystem monitoring."""
from datetime import datetime
from typing import Optional
import logging
from .metrics import calculate_biodiversity_score, calculate_all_metrics, mann_kendall_test

logger = logging.getLogger(__name__)


class BiodiversityIndexCalculator:
    def __init__(self, shannon_max: float = 3.91):
        self.shannon_max = shannon_max
        self.history: list[dict] = []

    def calculate(self, species_counts: dict[str, int]) -> dict:
        metrics = calculate_biodiversity_score(species_counts, self.shannon_max)
        metrics["timestamp"] = datetime.utcnow().isoformat()
        self.history.append(metrics)
        return metrics

    def calculate_with_baseline(self, species_counts: dict[str, int], baseline: dict[str, int]) -> dict:
        metrics = calculate_all_metrics(species_counts, baseline, self.shannon_max)
        metrics["timestamp"] = datetime.utcnow().isoformat()
        self.history.append(metrics)
        return metrics

    def detect_trend(self, min_data_points: int = 5) -> Optional[dict]:
        if len(self.history) < min_data_points:
            return None
        shannon_values = [h["shannon_index"] for h in self.history]
        richness_values = [h["species_richness"] for h in self.history]
        shannon_trend = mann_kendall_test(shannon_values)
        richness_trend = mann_kendall_test(richness_values)
        return {
            "shannon_trend": shannon_trend,
            "richness_trend": richness_trend,
            "data_points": len(self.history),
            "latest_shannon": shannon_values[-1],
            "latest_richness": richness_values[-1],
            "mean_shannon": round(sum(shannon_values) / len(shannon_values), 4),
        }

    def get_risk_level(self, shannon_index: float) -> str:
        if shannon_index >= 3.5:
            return "LOW"
        elif shannon_index >= 2.5:
            return "MODERATE"
        elif shannon_index >= 1.5:
            return "HIGH"
        return "CRITICAL"