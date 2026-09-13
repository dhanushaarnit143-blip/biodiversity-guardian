"""Configuration management for Biodiversity Guardian."""
from pathlib import Path
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DB_PATH = DATA_DIR / "biodiversity.db"


class AudioConfig(BaseModel):
    sample_rate: int = 32000
    duration: int = 5
    n_mels: int = 128
    n_fft: int = 2048
    hop_length: int = 512
    model_path: Path = MODELS_DIR / "audio_model"


class ImageConfig(BaseModel):
    yolo_model: str = "yolov8m.pt"
    confidence_threshold: float = 0.5
    model_path: Path = MODELS_DIR / "yolo_model"


class BiodiversityConfig(BaseModel):
    max_species: int = 100
    shannon_max_reference: float = 3.91
    risk_levels: list[str] = ["LOW", "MODERATE", "HIGH", "CRITICAL"]


class LLMConfig(BaseModel):
    model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    max_new_tokens: int = 512
    temperature: float = 0.7


class AppConfig(BaseModel):
    audio: AudioConfig = AudioConfig()
    image: ImageConfig = ImageConfig()
    biodiversity: BiodiversityConfig = BiodiversityConfig()
    llm: LLMConfig = LLMConfig()
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    open_meteo_base: str = "https://archive-api.open-meteo.com/v1"


config = AppConfig()
