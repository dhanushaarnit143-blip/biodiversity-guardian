"""Species identification and classification from detected wildlife."""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

TAXONOMY = {
    "bird": {"class": "Aves", "category": "birds"},
    "eagle": {"class": "Aves", "category": "birds"},
    "hawk": {"class": "Aves", "category": "birds"},
    "owl": {"class": "Aves", "category": "birds"},
    "parrot": {"class": "Aves", "category": "birds"},
    "deer": {"class": "Mammalia", "category": "mammals"},
    "elephant": {"class": "Mammalia", "category": "mammals"},
    "monkey": {"class": "Mammalia", "category": "mammals"},
    "leopard": {"class": "Mammalia", "category": "mammals"},
    "tiger": {"class": "Mammalia", "category": "mammals"},
    "bear": {"class": "Mammalia", "category": "mammals"},
    "cow": {"class": "Mammalia", "category": "mammals"},
    "frog": {"class": "Amphibia", "category": "amphibians"},
    "toad": {"class": "Amphibia", "category": "amphibians"},
    "snake": {"class": "Reptilia", "category": "reptiles"},
    "lizard": {"class": "Reptilia", "category": "reptiles"},
    "turtle": {"class": "Reptilia", "category": "reptiles"},
    "crocodile": {"class": "Reptilia", "category": "reptiles"},
}


class SpeciesIdentifier:
    """Identify and classify detected wildlife species."""

    def __init__(self):
        self.taxonomy = TAXONOMY

    def get_taxonomy(self, species_name: str) -> dict:
        """Get taxonomic info for a species."""
        lower = species_name.lower()
        return self.taxonomy.get(lower, {
            "class": "Unknown",
            "category": "unknown"
        })

    def classify_detections(self, detections: dict) -> dict:
        """Classify detected species into categories."""
        classified = {
            "birds": {},
            "mammals": {},
            "amphibians": {},
            "reptiles": {},
            "insects": {},
            "unknown": {},
        }

        for species, info in detections.get("species_counts", {}).items():
            taxon = self.get_taxonomy(species)
            category = taxon["category"]
            classified[category][species] = info

        return classified

    def get_summary(self, detections: dict) -> dict:
        """Generate summary of image detections."""
        classified = self.classify_detections(detections)

        summary = {
            "total_species": len(detections.get("species_counts", {})),
            "total_individuals": detections.get("total_detections", 0),
            "by_category": {},
        }

        for category, species_dict in classified.items():
            if species_dict:
                summary["by_category"][category] = {
                    "species_count": len(species_dict),
                    "individuals": sum(s["count"] for s in species_dict.values()),
                }

        return summary
