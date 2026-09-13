# 🌿 Biodiversity Guardian AI

AI-powered ecosystem monitoring platform for biodiversity conservation.

## What It Does

Biodiversity Guardian uses AI to listen to ecosystems, identify wildlife, monitor environmental changes, detect biodiversity decline, and provide early conservation recommendations.

### Key Features

- **Audio Species Identification** - CNN-based classification of bird, amphibian, and insect sounds
- **Wildlife Image Detection** - YOLO-powered camera trap analysis
- **Biodiversity Index** - Shannon, Simpson, and evenness metrics
- **Change Detection** - Statistical comparison with historical baselines
- **Risk Prediction** - XGBoost model for ecosystem risk assessment
- **Explainable AI** - SHAP-based risk factor explanations
- **Conservation Agent** - Local LLM for actionable recommendations
- **Interactive Dashboard** - Streamlit-based monitoring interface

## Quick Start

`ash
# Install dependencies
pip install -e "."

# Generate synthetic data
python scripts/download_datasets.py

# Run dashboard
streamlit run dashboard/app.py
`

## Architecture

`
Audio Data ──── Audio Model ────┐
                                ├── Biodiversity Fusion ── Risk Prediction ── Conservation AI
Image Data ──── Vision Model ───┘
Environmental Data ─────────────
`

## Tech Stack

- **Audio**: Librosa, PyTorch, ResNet
- **Vision**: YOLOv8, OpenCV
- **ML**: XGBoost, SHAP
- **LLM**: TinyLlama (local inference)
- **Dashboard**: Streamlit, Plotly, Folium
- **Database**: SQLite + SQLAlchemy

## Project Structure

`
biodiversity-guardian/
├── src/                    # Core modules
│   ├── audio_processing/   # Audio classification
│   ├── image_detection/    # Wildlife detection
│   ├── biodiversity/       # Metrics calculation
│   ├── change_detection/   # Trend analysis
│   ├── risk_prediction/    # Risk assessment
│   ├── explainability/     # SHAP explanations
│   └── conservation_agent/ # LLM recommendations
├── dashboard/              # Streamlit app
├── data/                   # Datasets
├── models/                 # Trained models
└── scripts/                # Data preparation
`

## License

MIT