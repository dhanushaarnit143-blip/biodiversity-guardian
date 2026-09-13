"""Mel spectrogram feature extraction for audio classification."""
import numpy as np
import librosa
import torch
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MelSpectrogramExtractor:
    """Extract mel spectrogram features from audio."""

    def __init__(
        self,
        sample_rate: int = 32000,
        n_mels: int = 128,
        n_fft: int = 2048,
        hop_length: int = 512,
    ):
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length

    def extract(self, audio: np.ndarray) -> np.ndarray:
        """Extract mel spectrogram from audio array."""
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
            n_mels=self.n_mels,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
        )
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        return mel_spec_db

    def extract_to_tensor(self, audio: np.ndarray) -> torch.Tensor:
        """Extract mel spectrogram and return as PyTorch tensor."""
        mel_spec = self.extract(audio)
        return torch.tensor(mel_spec, dtype=torch.float32).unsqueeze(0)

    def extract_batch(self, audio_batch: list[np.ndarray]) -> torch.Tensor:
        """Extract mel spectrograms for a batch of audio arrays."""
        specs = []
        for audio in audio_batch:
            tensor = self.extract_to_tensor(audio)
            specs.append(tensor)
        return torch.stack(specs)

    def augment(self, audio: np.ndarray) -> list[np.ndarray]:
        """Apply data augmentation to audio."""
        augmented = [audio]

        noise = np.random.normal(0, 0.005, len(audio))
        augmented.append(audio + noise)

        rate = np.random.uniform(0.9, 1.1)
        stretched = librosa.effects.time_stretch(audio, rate=rate)
        if len(stretched) != len(audio):
            stretched = np.resize(stretched, len(audio))
        augmented.append(stretched)

        shift = np.random.randint(-self.sample_rate, self.sample_rate)
        shifted = np.roll(audio, shift)
        augmented.append(shifted)

        return augmented
