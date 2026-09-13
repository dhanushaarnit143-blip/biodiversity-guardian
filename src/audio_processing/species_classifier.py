"""CNN-based audio species classifier."""
import numpy as np
import torch
import torch.nn as nn
from torchvision import models
from pathlib import Path
from typing import Optional
import logging

from .preprocessor import AudioPreprocessor
from .feature_extractor import MelSpectrogramExtractor

logger = logging.getLogger(__name__)

TROPICAL_SPECIES = [
    "Asian Koel", "Indian Peafowl", "Hornbill", "Kingfisher",
    "Woodpecker", "Crow", "Indian Frog", "Tree Frog",
    "Bullfrog", "Cicada", "Cricket", "Grasshopper",
    "Indian Bat", "Langur", "Monkey", "Unknown Bird",
    "Insect Chorus", "Frog Call", "Ambient Forest", "Silence"
]


class AudioCNN(nn.Module):
    """CNN for audio species classification from mel spectrograms."""

    def __init__(self, num_classes: int = len(TROPICAL_SPECIES)):
        super().__init__()
        self.backbone = models.resnet18(pretrained=True)
        self.backbone.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)


class AudioSpeciesClassifier:
    """Classify wildlife species from audio recordings."""

    def __init__(
        self,
        model_path: Optional[Path] = None,
        device: Optional[str] = None,
        species_list: Optional[list[str]] = None,
    ):
        self.species_list = species_list or TROPICAL_SPECIES
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.preprocessor = AudioPreprocessor()
        self.feature_extractor = MelSpectrogramExtractor()

        self.model = AudioCNN(num_classes=len(self.species_list))
        self.model.to(self.device)

        if model_path and model_path.exists():
            self.load_model(model_path)
        else:
            logger.info("No pretrained model loaded, using random weights")

    def load_model(self, model_path: Path):
        """Load trained model weights."""
        try:
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            logger.info(f"Loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")

    def save_model(self, model_path: Path):
        """Save model weights."""
        model_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.model.state_dict(), model_path)
        logger.info(f"Saved model to {model_path}")

    def predict(self, audio_path: str | Path) -> dict:
        """Predict species from an audio file."""
        audio = self.preprocessor.process_to_fixed_length(audio_path)
        if audio is None:
            return {"error": "Failed to process audio"}

        features = self.feature_extractor.extract_to_tensor(audio).to(self.device)

        with torch.no_grad():
            logits = self.model(features)
            probs = torch.softmax(logits, dim=-1)
            confidence, idx = probs.max(dim=-1)

        return {
            "species": self.species_list[idx.item()],
            "confidence": round(confidence.item(), 4),
            "all_probabilities": {
                self.species_list[i]: round(p, 4)
                for i, p in enumerate(probs[0].tolist())
            },
        }

    def predict_batch(self, audio_paths: list[str | Path]) -> list[dict]:
        """Predict species for multiple audio files."""
        return [self.predict(path) for path in audio_paths]

    def identify_species_in_recording(self, audio_path: str | Path) -> dict:
        """Identify all species present in a longer recording."""
        audio = self.preprocessor.process_to_fixed_length(audio_path)
        if audio is None:
            return {"error": "Failed to process audio"}

        segments = self.preprocessor.segment_audio(audio)
        species_counts = {}
        total_segments = len(segments)

        for segment in segments:
            features = self.feature_extractor.extract_to_tensor(segment).to(self.device)
            with torch.no_grad():
                logits = self.model(features)
                probs = torch.softmax(logits, dim=-1)
                confidence, idx = probs.max(dim=-1)

            if confidence.item() > 0.3:
                species = self.species_list[idx.item()]
                if species not in ["Silence", "Unknown Bird"]:
                    species_counts[species] = species_counts.get(species, 0) + 1

        return {
            "detected_species": species_counts,
            "total_segments": total_segments,
            "unique_species": len(species_counts),
        }
