"""
Vision router — /api/v1/vision

Endpoints:
  POST /detect  — upload a camera-trap image → bounding boxes + species

YOLO inference is run in a thread-pool executor to avoid blocking the event loop.
The annotated image (with bounding boxes drawn by Ultralytics) is saved to
/uploads/vision/ and served as a static URL the frontend can display directly.
"""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from api.core.model_registry import ModelRegistry
from api.core.schemas import BoundingBox, DetectionResult, WildlifeDetectionResponse

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = Path("uploads/vision")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg", "image/png", "image/webp", "image/tiff",
}

# Species → taxonomic class mapping (extend as needed)
SPECIES_CLASS_MAP: dict[str, str] = {
    "bird": "bird", "eagle": "bird", "owl": "bird",
    "deer": "mammal", "tiger": "mammal", "bear": "mammal", "fox": "mammal",
    "frog": "amphibian", "toad": "amphibian",
    "snake": "reptile", "lizard": "reptile",
}


def _resolve_class(species_name: str) -> str:
    lower = species_name.lower()
    for keyword, taxon in SPECIES_CLASS_MAP.items():
        if keyword in lower:
            return taxon
    return "unknown"


async def _save_image(file: UploadFile) -> Path:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported image format: {file.content_type}",
        )
    ext = Path(file.filename or "image.jpg").suffix or ".jpg"
    dest = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
    dest.write_bytes(await file.read())
    return dest


@router.post(
    "/detect",
    response_model=WildlifeDetectionResponse,
    summary="Detect wildlife in a camera-trap image",
)
async def detect_wildlife(
    file: UploadFile = File(..., description="JPEG / PNG camera-trap image"),
) -> WildlifeDetectionResponse:
    """
    Runs YOLOv8 on the uploaded image and returns:
    - `detections`: list of {species, confidence, bbox, species_class}
    - `image_url`: URL to the annotated image (served from /uploads)
    - `processing_time_ms`: end-to-end latency

    YOLOv8m is lazy-loaded on first request (~3–5 s cold start).
    """
    image_path = await _save_image(file)
    annotated_path = UPLOAD_DIR / f"{image_path.stem}_annotated{image_path.suffix}"

    t0 = time.perf_counter()
    try:
        detector = ModelRegistry.get_wildlife_detector()

        def _run_detection() -> list[dict]:
            return detector.detect(str(image_path), save_path=str(annotated_path))

        raw_detections: list[dict] = await run_in_threadpool(_run_detection)
    except Exception as exc:
        logger.exception("Wildlife detection failed")
        image_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        image_path.unlink(missing_ok=True)  # remove original; keep annotated

    elapsed_ms = (time.perf_counter() - t0) * 1000

    detections = [
        DetectionResult(
            species=d.get("species", d.get("label", "Unknown")),
            confidence=round(float(d.get("confidence", 0.0)), 4),
            bbox=BoundingBox(
                x1=d["bbox"][0], y1=d["bbox"][1],
                x2=d["bbox"][2], y2=d["bbox"][3],
            ),
            species_class=_resolve_class(d.get("species", d.get("label", ""))),
        )
        for d in raw_detections
    ]

    image_url = f"/uploads/vision/{annotated_path.name}" if annotated_path.exists() else ""

    return WildlifeDetectionResponse(
        detections=detections,
        detection_count=len(detections),
        image_url=image_url,
        processing_time_ms=round(elapsed_ms, 1),
    )
