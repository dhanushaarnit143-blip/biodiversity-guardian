"""Audio preprocessing: noise reduction, segmentation, normalization."""
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AudioPreprocessor:
    """Preprocess wildlife audio recordings."""

    def __init__(self, sample_rate: int = 32000, duration: int = 5):
        self.sample_rate = sample_rate
        self.duration = duration

    def load_audio(self, filepath: str | Path) -> tuple[np.ndarray, int]:
        """Load and resample audio file."""
        y, sr = librosa.load(filepath, sr=self.sample_rate, mono=True)
        return y, sr

    def normalize(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio amplitude."""
        peak = np.max(np.abs(audio))
        if peak > 0:
            return audio / peak
        return audio

    def remove_silence(self, audio: np.ndarray, threshold_db: int = -40) -> np.ndarray:
        """Remove silent segments."""
        intervals = librosa.effects.split(audio, top_db=threshold_db)
        if len(intervals) == 0:
            return audio
        return np.concatenate([audio[start:end] for start, end in intervals])

    def segment_audio(self, audio: np.ndarray) -> list[np.ndarray]:
        """Split audio into fixed-length segments."""
        segment_length = self.sample_rate * self.duration
        segments = []
        for start in range(0, len(audio), segment_length):
            segment = audio[start:start + segment_length]
            if len(segment) < segment_length:
                segment = np.pad(segment, (0, segment_length - len(segment)))
            segments.append(segment)
        return segments

    def reduce_noise(self, audio: np.ndarray) -> np.ndarray:
        """Simple noise reduction using spectral gating."""
        noise_profile = np.mean(np.abs(librosa.stft(audio[:self.sample_rate])), axis=1)
        stft = librosa.stft(audio)
        magnitude = np.abs(stft)
        phase = np.angle(stft)

        noise_threshold = np.percentile(magnitude, 20, axis=1, keepdims=True)
        mask = magnitude > noise_threshold
        cleaned_magnitude = magnitude * mask

        cleaned_stft = cleaned_magnitude * np.exp(1j * phase)
        cleaned_audio = librosa.istft(cleaned_stft)
        return cleaned_audio

    def process_file(self, filepath: str | Path) -> list[np.ndarray]:
        """Full preprocessing pipeline for a single file."""
        try:
            audio, sr = self.load_audio(filepath)
            audio = self.normalize(audio)
            audio = self.reduce_noise(audio)
            segments = self.segment_audio(audio)
            return segments
        except Exception as e:
            logger.error(f"Preprocessing failed for {filepath}: {e}")
            return []

    def process_to_fixed_length(self, filepath: str | Path) -> Optional[np.ndarray]:
        """Process audio to a single fixed-length array."""
        try:
            audio, sr = self.load_audio(filepath)
            audio = self.normalize(audio)
            target_length = self.sample_rate * self.duration

            if len(audio) > target_length:
                start = (len(audio) - target_length) // 2
                audio = audio[start:start + target_length]
            elif len(audio) < target_length:
                audio = np.pad(audio, (0, target_length - len(audio)))

            return audio
        except Exception as e:
            logger.error(f"Processing failed for {filepath}: {e}")
            return None
