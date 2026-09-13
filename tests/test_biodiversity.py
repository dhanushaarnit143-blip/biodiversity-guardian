"""Tests for biodiversity metrics."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from biodiversity.metrics import (
    shannon_diversity, simpson_diversity, evenness,
    calculate_biodiversity_score, mann_kendall_test
)


def test_shannon_diversity():
    counts = {"bird_a": 10, "bird_b": 10, "frog": 5}
    result = shannon_diversity(counts)
    assert result > 0
    assert result < 2


def test_shannon_single_species():
    counts = {"bird": 10}
    result = shannon_diversity(counts)
    assert result == 0.0


def test_simpson_diversity():
    counts = {"bird_a": 10, "bird_b": 10, "frog": 5}
    result = simpson_diversity(counts)
    assert 0 < result < 1


def test_evenness():
    counts = {"a": 10, "b": 10, "c": 10}
    result = evenness(1.0986, 3)
    assert 0 < result <= 1


def test_biodiversity_score():
    counts = {"bird_a": 10, "bird_b": 5, "frog": 3}
    result = calculate_biodiversity_score(counts)
    assert "shannon_index" in result
    assert "simpson_index" in result
    assert "biodiversity_score" in result
    assert 0 <= result["biodiversity_score"] <= 100


def test_mann_kendall_increasing():
    data = [1.0, 1.5, 2.0, 2.5, 3.0]
    result = mann_kendall_test(data)
    assert result["direction"] == "increasing"


def test_mann_kendall_decreasing():
    data = [3.0, 2.5, 2.0, 1.5, 1.0]
    result = mann_kendall_test(data)
    assert result["direction"] == "decreasing"


if __name__ == "__main__":
    test_shannon_diversity()
    test_shannon_single_species()
    test_simpson_diversity()
    test_evenness()
    test_biodiversity_score()
    test_mann_kendall_increasing()
    test_mann_kendall_decreasing()
    print("All tests passed!")