"""Ecosystem change detection module."""
from datetime import datetime, timedelta
from typing import Optional
import numpy as np
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class EcosystemChangeDetector:
    def __init__(self, lookback_months: int = 6):
        self.lookback_months = lookback_months

    def detect_species_changes(self, current: dict[str, int], historical: dict[str, int]) -> dict:
        all_species = set(list(current.keys()) + list(historical.keys()))
        changes = {}
        for sp in all_species:
            curr_count = current.get(sp, 0)
            hist_count = historical.get(sp, 0)
            if hist_count > 0:
                change_pct = ((curr_count - hist_count) / hist_count) * 100
            elif curr_count > 0:
                change_pct = 100.0
            else:
                change_pct = 0.0
            changes[sp] = {
                "current": curr_count,
                "historical": hist_count,
                "change_pct": round(change_pct, 2),
                "status": "declining" if change_pct < -10 else "stable" if abs(change_pct) <= 10 else "increasing"
            }
        return changes

    def detect_index_changes(self, current_metrics: dict, historical_metrics: list[dict]) -> list[dict]:
        changes = []
        if len(historical_metrics) < 3:
            return changes

        hist_shannon = [m.get("shannon_index", 0) for m in historical_metrics]
        curr_shannon = current_metrics.get("shannon_index", 0)

        mean_hist = np.mean(hist_shannon)
        std_hist = np.std(hist_shannon)
        z_score = (curr_shannon - mean_hist) / (std_hist + 1e-10)

        if abs(z_score) > 2:
            changes.append({
                "metric": "shannon_index",
                "current": curr_shannon,
                "historical_mean": round(mean_hist, 4),
                "z_score": round(z_score, 2),
                "direction": "declining" if z_score < 0 else "increasing",
                "severity": "high" if abs(z_score) > 3 else "moderate",
            })

        hist_richness = [m.get("species_richness", 0) for m in historical_metrics]
        curr_richness = current_metrics.get("species_richness", 0)
        mean_richness = np.mean(hist_richness)
        std_richness = np.std(hist_richness)
        z_rich = (curr_richness - mean_richness) / (std_richness + 1e-10)

        if abs(z_rich) > 2:
            changes.append({
                "metric": "species_richness",
                "current": curr_richness,
                "historical_mean": round(mean_richness, 2),
                "z_score": round(z_rich, 2),
                "direction": "declining" if z_rich < 0 else "increasing",
                "severity": "high" if abs(z_rich) > 3 else "moderate",
            })

        return changes

    def detect_environmental_changes(self, current_env: dict, historical_env: list[dict]) -> list[dict]:
        changes = []
        key_vars = ["temperature_mean", "precipitation_mm", "humidity_pct", "soil_moisture"]

        for var in key_vars:
            curr_val = current_env.get(var)
            hist_vals = [h.get(var) for h in historical_env if h.get(var) is not None]

            if curr_val is None or len(hist_vals) < 3:
                continue

            mean_hist = np.mean(hist_vals)
            std_hist = np.std(hist_vals)
            z = (curr_val - mean_hist) / (std_hist + 1e-10)

            if abs(z) > 2:
                changes.append({
                    "metric": var,
                    "current": round(curr_val, 2),
                    "historical_mean": round(mean_hist, 2),
                    "z_score": round(z, 2),
                    "direction": "above_normal" if z > 0 else "below_normal",
                    "severity": "high" if abs(z) > 3 else "moderate",
                })

        return changes

    def generate_change_summary(self, species_changes: dict, index_changes: list, env_changes: list) -> dict:
        declining_species = [sp for sp, info in species_changes.items() if info["status"] == "declining"]
        increasing_species = [sp for sp, info in species_changes.items() if info["status"] == "increasing"]

        high_severity = [c for c in index_changes + env_changes if c.get("severity") == "high"]

        return {
            "declining_species": declining_species,
            "increasing_species": increasing_species,
            "total_declining": len(declining_species),
            "total_increasing": len(increasing_species),
            "index_changes": index_changes,
            "environmental_changes": env_changes,
            "high_severity_alerts": len(high_severity),
            "summary_text": self._build_summary_text(declining_species, high_severity),
        }

    def _build_summary_text(self, declining: list, alerts: list) -> str:
        if not declining and not alerts:
            return "Ecosystem appears stable. No significant changes detected."
        parts = []
        if declining:
            parts.append(f"{len(declining)} species showing decline: {', '.join(declining[:5])}")
        if alerts:
            parts.append(f"{len(alerts)} high-severity changes detected in metrics")
        return ". ".join(parts) + "."