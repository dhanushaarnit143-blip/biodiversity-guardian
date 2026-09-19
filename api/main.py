"""
Biodiversity Guardian AI — FastAPI Backend Entry Point.

Startup order:
  1. App-wide lifespan: initialises ML models lazily via ModelRegistry.
  2. CORS: allows the Vite dev server (localhost:5173) and production origin.
  3. Routers: one router per domain (overview, audio, vision, risk, conservation, map, db).
  4. Static: serves uploaded files (audio/images) from /uploads.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.core.model_registry import ModelRegistry
from api.routers import audio, conservation, overview, risk, vision, biodiversity_map

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Upload directory
# ---------------------------------------------------------------------------
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Lifespan (replaces deprecated on_event)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm up lightweight resources on startup; release on shutdown."""
    logger.info("🌿 Biodiversity Guardian API starting…")
    # ModelRegistry uses lazy-loading; nothing heavy is loaded here.
    # To pre-warm a specific model, call ModelRegistry.get_risk_predictor() here.
    yield
    logger.info("🌿 Biodiversity Guardian API shutting down.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Biodiversity Guardian AI",
    description="FastAPI backend exposing ML pipelines, DB queries, and the conservation LLM agent.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow Vite dev server + any deployed frontend origin
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # Alternative dev port
        "https://biodiversity-guardian.app",  # Production (update as needed)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Static file serving (uploaded audio / images returned to frontend)
# ---------------------------------------------------------------------------
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(overview.router,        prefix="/api/v1/overview",      tags=["Overview"])
app.include_router(audio.router,           prefix="/api/v1/audio",         tags=["Audio"])
app.include_router(vision.router,          prefix="/api/v1/vision",        tags=["Vision"])
app.include_router(risk.router,            prefix="/api/v1/risk",          tags=["Risk"])
app.include_router(conservation.router,    prefix="/api/v1/conservation",  tags=["Conservation AI"])
app.include_router(biodiversity_map.router,prefix="/api/v1/map",           tags=["Biodiversity Map"])


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    return {"status": "ok", "service": "Biodiversity Guardian AI"}
