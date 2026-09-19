"""
Audio router — /api/v1/audio

Endpoints:
  POST /classify          — single audio file → top species + probabilities
  POST /identify-all      — longer recording  → all detected species + counts

Model loading strategy
----------------------
The AudioSpeciesClassifier (ResNet18 + mel spectrogram pipeline) is loaded
lazily via ModelRegistry on the first request.  Subsequent calls reuse the
cached instance.  Classification runs in a FastAPI thread-pool executor to
avoid blocking the async event loop.
"""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from api.core.model_registry import ModelRegistry
from api.core.schemas import AudioClassificationResponse, MultiSpeciesAudioResponse

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = Path("uploads/audio")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_AUDIO_TYPES = {"audio/wav", "audio/mpeg", "audio/ogg", "audio/flac", "audio/x-wav"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _save_upload(file: UploadFile) -> Path:
    """Persist the uploaded file and return its local path."""
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported audio format: {file.content_type}. "
                   f"Accepted: {', '.join(ALLOWED_AUDIO_TYPES)}",
        )
    ext = Path(file.filename or "audio.wav").suffix or ".wav"
    dest = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
    content = await file.read()
    dest.write_bytes(content)
    return dest


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post(
    "/classify",
    response_model=AudioClassificationResponse,
    summary="Classify a single audio clip to the top species",
)
async def classify_audio(
    file: UploadFile = File(..., description="WAV / MP3 / OGG audio file (max 5 s recommended)")
) -> AudioClassificationResponse:
    """
    Upload an audio clip and receive:
    - `species`: top predicted species name
    - `confidence`: softmax probability of top class
    - `all_probabilities`: full 20-class softmax distribution
    - `processing_time_ms`: end-to-end latency

    The ResNet18 audio CNN is lazy-loaded on the first call (~2 s cold start).
    """
    audio_path = await _save_upload(file)

    t0 = time.perf_counter()
    try:
        classifier = ModelRegistry.get_audio_classifier()
        # Run CPU/GPU inference in thread pool — never block the event loop
        result: dict = await run_in_threadpool(classifier.predict, audio_path)
    except Exception as exc:
        logger.exception("Audio classification failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        # Clean up uploaded file after inference
        audio_path.unlink(missing_ok=True)

    elapsed_ms = (time.perf_counter() - t0) * 1000

    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])

    return AudioClassificationResponse(
        species=result["species"],
        confidence=result["confidence"],
        all_probabilities=result["all_probabilities"],
        processing_time_ms=round(elapsed_ms, 1),
    )


@router.post(
    "/identify-all",
    response_model=MultiSpeciesAudioResponse,
    summary="Identify all species present in a longer recording",
)
async def identify_all_species(
    file: UploadFile = File(..., description="Longer wildlife audio recording (any duration)")
) -> MultiSpeciesAudioResponse:
    """
    Segments the recording into 5-second windows, classifies each segment,
    and returns an aggregate species count dictionary.

    Useful for passive acoustic monitoring (PAM) deployments where a single
    recording may contain multiple species.
    """
    audio_path = await _save_upload(file)

    t0 = time.perf_counter()
    try:
        classifier = ModelRegistry.get_audio_classifier()
        result: dict = await run_in_threadpool(
            classifier.identify_species_in_recording, audio_path
        )
    except Exception as exc:
        logger.exception("Multi-species identification failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        audio_path.unlink(missing_ok=True)

    elapsed_ms = (time.perf_counter() - t0) * 1000

    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])

    return MultiSpeciesAudioResponse(
        detected_species=result["detected_species"],
        total_segments=result["total_segments"],
        unique_species=result["unique_species"],
        processing_time_ms=round(elapsed_ms, 1),
    )
