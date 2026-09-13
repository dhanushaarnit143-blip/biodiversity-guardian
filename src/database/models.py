"""SQLAlchemy database models for biodiversity observations."""
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, Float, String, DateTime,
    ForeignKey, Text, JSON, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "biodiversity.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_lat = Column(Float, nullable=False)
    location_lon = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50), nullable=False)  # audio, image, environmental
    ecosystem_zone = Column(String(100))
    file_path = Column(Text)
    metadata_json = Column(JSON, default={})

    species_detections = relationship("SpeciesDetection", back_populates="observation")
    environmental_data = relationship("EnvironmentalData", back_populates="observation", uselist=False)


class SpeciesDetection(Base):
    __tablename__ = "species_detections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    observation_id = Column(Integer, ForeignKey("observations.id"), nullable=False)
    species_name = Column(String(200), nullable=False)
    species_class = Column(String(50))  # bird, mammal, amphibian, insect, reptile
    confidence = Column(Float)
    count = Column(Integer, default=1)
    bbox = Column(JSON)  # [x1, y1, x2, y2] for image detections
    timestamp = Column(DateTime, default=datetime.utcnow)

    observation = relationship("Observation", back_populates="species_detections")


class EnvironmentalData(Base):
    __tablename__ = "environmental_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    observation_id = Column(Integer, ForeignKey("observations.id"), nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    rainfall_mm = Column(Float)
    wind_speed = Column(Float)
    vegetation_index = Column(Float)  # NDVI
    soil_moisture = Column(Float)
    pressure = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    observation = relationship("Observation", back_populates="environmental_data")


class BiodiversityMetric(Base):
    __tablename__ = "biodiversity_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_lat = Column(Float, nullable=False)
    location_lon = Column(Float, nullable=False)
    ecosystem_zone = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    shannon_index = Column(Float)
    simpson_index = Column(Float)
    species_richness = Column(Integer)
    evenness = Column(Float)
    biodiversity_score = Column(Float)
    risk_level = Column(String(20))
    risk_confidence = Column(Float)
    metadata_json = Column(JSON, default={})


class HistoricalBaseline(Base):
    __tablename__ = "historical_baselines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_lat = Column(Float, nullable=False)
    location_lon = Column(Float, nullable=False)
    ecosystem_zone = Column(String(100))
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    species_counts = Column(JSON)  # {"species_name": count}
    shannon_index = Column(Float)
    simpson_index = Column(Float)
    species_richness = Column(Integer)
    evenness = Column(Float)
    notes = Column(Text)


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_id = Column(Integer, ForeignKey("biodiversity_metrics.id"))
    risk_level = Column(String(20), nullable=False)
    risk_confidence = Column(Float)
    contributing_factors = Column(JSON)
    shap_values = Column(JSON)
    recommendation = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create all tables."""
    Base.metadata.create_all(engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
