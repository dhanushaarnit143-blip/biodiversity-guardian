"""Ecological biodiversity metrics."""
import numpy as np
from scipy import stats
from typing import Optional


def shannon_diversity(species_counts: dict[str, int]) -> float:
    total = sum(species_counts.values())
    if total == 0:
        return 0.0
    proportions = np.array(list(species_counts.values())) / total
    proportions = proportions[proportions > 0]
    return float(-np.sum(proportions * np.log(proportions)))


def simpson_diversity(species_counts: dict[str, int]) -> float:
    total = sum(species_counts.values())
    if total == 0:
        return 0.0
    proportions = np.array(list(species_counts.values())) / total
    return float(1 - np.sum(proportions ** 2))


def evenness(shannon_h: float, species_count: int) -> float:
    if species_count <= 1:
        return 0.0
    return float(shannon_h / np.log(species_count))


def species_richness(species_counts: dict[str, int]) -> int:
    return len([k for k, v in species_counts.items() if v > 0])


def calculate_biodiversity_score(species_counts: dict[str, int], shannon_max: float = 3.91) -> dict:
    sh = shannon_diversity(species_counts)
    si = simpson_diversity(species_counts)
    rich = species_richness(species_counts)
    ev = evenness(sh, rich)
    score = min(100.0, (sh / shannon_max) * 100) if shannon_max > 0 else 0.0
    return {
        "shannon_index": round(sh, 4),
        "simpson_index": round(si, 4),
        "species_richness": rich,
        "evenness": round(ev, 4),
        "biodiversity_score": round(score, 1),
    }


def calculate_all_metrics(species_counts: dict[str, int], baseline: Optional[dict[str, int]] = None, shannon_max: float = 3.91) -> dict:
    metrics = calculate_biodiversity_score(species_counts, shannon_max)
    if baseline:
        baseline_metrics = calculate_biodiversity_score(baseline, shannon_max)
        shannon_change = (metrics["shannon_index"] - baseline_metrics["shannon_index"]) / max(baseline_metrics["shannon_index"], 1e-10) * 100
        richness_change = (metrics["species_richness"] - baseline_metrics["species_richness"]) / max(baseline_metrics["species_richness"], 1) * 100
        metrics["baseline"] = baseline_metrics
        metrics["shannon_change_pct"] = round(shannon_change, 2)
        metrics["richness_change_pct"] = round(richness_change, 2)
        metrics["is_declining"] = shannon_change < -10
    return metrics


def mann_kendall_test(data: list[float]) -> dict:
    n = len(data)
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(data[j] - data[k])
    var_s = n * (n - 1) * (2 * n + 5) / 18
    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:
        z = 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return {
        "significant": p_value < 0.05,
        "direction": "increasing" if z > 0 else "decreasing",
        "p_value": round(p_value, 4),
        "z_score": round(z, 2),
        "s_statistic": s,
    }