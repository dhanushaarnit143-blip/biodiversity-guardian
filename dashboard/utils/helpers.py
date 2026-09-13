"""Dashboard utility functions."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from database.models import init_db, SessionLocal, Observation, SpeciesDetection, BiodiversityMetric


def get_db_session():
    return SessionLocal()


def get_recent_observations(limit: int = 100) -> list:
    db = get_db_session()
    try:
        return db.query(Observation).order_by(Observation.timestamp.desc()).limit(limit).all()
    finally:
        db.close()


def get_biodiversity_metrics(limit: int = 50) -> list:
    db = get_db_session()
    try:
        return db.query(BiodiversityMetric).order_by(BiodiversityMetric.timestamp.desc()).limit(limit).all()
    finally:
        db.close()


def init_database():
    init_db()