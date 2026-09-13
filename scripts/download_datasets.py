"""Download and prepare datasets for training."""
from pathlib import Path
import sys
import json
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def download_sample_audio():
    print("Downloading sample audio from Xeno-Canto...")
    from data_collection import AudioCollector
    collector = AudioCollector(DATA_DIR)
    species = ["Asian Koel", "Indian Peafowl", "Cicada"]
    for sp in species:
        data = collector.collect_species_audio(sp, max_recordings=3)
        print(f"  {sp}: {len(data)} recordings")
    return True


def download_sample_images():
    print("Downloading sample images from iNaturalist...")
    from data_collection import ImageCollector
    collector = ImageCollector(DATA_DIR)
    data = collector.collect_wildlife_images("Aves", (-16.5, -56.5), max_images=10)
    print(f"  Downloaded {len(data)} bird images")
    return True


def download_environmental_data():
    print("Downloading environmental data from Open-Meteo...")
    from data_collection import EnvironmentalCollector
    collector = EnvironmentalCollector(DATA_DIR)
    data = collector.collect_ecosystem_environmental_data(-16.5, -56.5, months_back=6)
    filepath = collector.save_environmental_data(data)
    print(f"  Saved {len(data)} data points to {filepath}")
    return True


def generate_synthetic_data():
    print("Generating synthetic biodiversity data...")
    import numpy as np
    from database.models import init_db, SessionLocal, Observation, SpeciesDetection, BiodiversityMetric

    init_db()
    db = SessionLocal()

    np.random.seed(42)
    zones = [
        ("Wetland Zone A", -16.8, -56.2),
        ("Forest Zone B", -17.1, -56.8),
        ("Grassland Zone C", -16.3, -57.0),
    ]

    species_list = [
        ("Asian Koel", "bird"), ("Indian Peafowl", "bird"), ("Kingfisher", "bird"),
        ("Woodpecker", "bird"), ("Crow", "bird"), ("Hornbill", "bird"),
        ("Langur", "mammal"), ("Monkey", "mammal"), ("Deer", "mammal"),
        ("Indian Frog", "amphibian"), ("Tree Frog", "amphibian"),
        ("Cicada", "insect"), ("Cricket", "insect"),
    ]

    for zone_name, lat, lon in zones:
        for month in range(12):
            obs = Observation(
                location_lat=lat + np.random.uniform(-0.1, 0.1),
                location_lon=lon + np.random.uniform(-0.1, 0.1),
                source="synthetic",
                ecosystem_zone=zone_name,
            )
            db.add(obs)
            db.flush()

            decline_factor = 1.0 - (month * 0.03)
            for sp_name, sp_class in species_list:
                count = max(1, int(np.random.poisson(5) * decline_factor))
                sd = SpeciesDetection(
                    observation_id=obs.id,
                    species_name=sp_name,
                    species_class=sp_class,
                    confidence=round(np.random.uniform(0.7, 0.99), 2),
                    count=count,
                )
                db.add(sd)

            metric = BiodiversityMetric(
                location_lat=lat,
                location_lon=lon,
                ecosystem_zone=zone_name,
                shannon_index=round(4.2 - month * 0.08 + np.random.uniform(-0.1, 0.1), 4),
                simpson_index=round(0.85 - month * 0.01, 4),
                species_richness=max(5, int(15 - month * 0.8 + np.random.randint(-2, 3))),
                evenness=round(0.9 - month * 0.005, 4),
                biodiversity_score=round(max(20, 84 - month * 5 + np.random.uniform(-5, 5)), 1),
                risk_level="CRITICAL" if month > 9 else "HIGH" if month > 6 else "MODERATE" if month > 3 else "LOW",
            )
            db.add(metric)

    db.commit()
    db.close()
    print("  Generated 36 observations with species and metrics")


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    generate_synthetic_data()
    print("\nDataset preparation complete!")