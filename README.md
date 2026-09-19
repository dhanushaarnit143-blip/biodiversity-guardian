# 🌿 Biodiversity Guardian AI

AI-powered ecosystem monitoring platform for biodiversity conservation.

## What It Does

Biodiversity Guardian uses AI to listen to ecosystems, identify wildlife, monitor environmental changes, detect biodiversity decline, and provide early conservation recommendations.

### 🌟 Current Features

- **Audio Species Identification**: CNN-based classification of bird, amphibian, and insect calls using mel-spectrograms.
- **Wildlife Image Detection**: YOLOv8-powered camera trap analysis to automatically detect and count species.
- **Biodiversity Analytics**: Computes complex ecological metrics including Shannon, Simpson, and evenness indices.
- **Risk Prediction & Explainability**: XGBoost model for ecosystem risk assessment, paired with SHAP to provide transparent, explainable risk factor insights.
- **Conservation AI Agent**: A local LLM (TinyLlama) provides actionable, step-by-step conservation recommendations based on the analyzed data.
- **100% Offline Capability**: All inference (vision, audio, LLM) runs completely locally, ensuring data privacy and making it viable for remote nature reserves without internet access.
- **Multi-modal Dashboard**: An interactive Streamlit interface featuring a custom glassmorphism design system, Plotly charts, and Folium maps to visualize ecosystem health cohesively.

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