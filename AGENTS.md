# AGENTS.md — Biodiversity Guardian AI

## Quick Start
```bash
pip install -e ".[dev]"
python scripts/download_datasets.py   # generates synthetic data + SQLite DB
streamlit run dashboard/app.py        # runs on localhost:8501
```

## Key Commands
| Task | Command |
|------|---------|
| Install (dev) | `pip install -e ".[dev]"` |
| Lint | `ruff check .` |
| Typecheck | (no mypy configured) |
| Test | `pytest tests/` |
| Format | `ruff format .` |
| Generate data | `python scripts/download_datasets.py` |
| Run dashboard | `streamlit run dashboard/app.py` |

## Architecture (Non-Obvious)
- **Entry**: `dashboard/app.py` → loads design system, routes to 5 pages
- **Modules**: 8 core packages under `src/` (audio, vision, biodiversity, change, risk, explainability, conservation_agent, data_collection, database)
- **DB**: SQLite at `data/biodiversity.db` (auto-created by download script)
- **Models**: Pre-trained weights expected in `models/` (not in repo)
- **LLM**: TinyLlama loaded via transformers (local inference, no API key)

## Critical Gotchas
1. **config.toml BOM**: Must be UTF-8 **without BOM** or Streamlit fails to parse. Fix: `[System.IO.File]::WriteAllText(path, content, [System.Text.Encoding]::UTF8)`
2. **Module cache**: Streamlit caches modules; restart server after changes to `components/styles.py`
3. **Design system**: Load `load_design_system()` **before** any UI rendering (see `app.py:26`)
3. **Panchang font**: Loaded via `@import` in `dashboard/assets/design-system.css` (not system font)
4. **Port**: Default 8501; use `--server.port 8502` if busy

## Project Structure (High-Signal)
```
src/                    # 8 core packages (pure Python, no Streamlit)
  audio_processing/     # CNN + mel spectrogram classification
  image_detection/      # YOLOv8 wrapper
  biodiversity/         # Shannon/Simpson/evenness metrics
  change_detection/     # Mann-Kendall trend tests
  risk_prediction/      # XGBoost + SHAP
  explainability/       # SHAP formatting
  conservation_agent/   # TinyLlama prompt templates
  data_collection/      # Xeno-Canto, iNaturalist, Open-Meteo
  database/             # SQLAlchemy models + SessionLocal
dashboard/
  app.py                # Main entry; loads design system, sidebar, routing
  components/styles.py  # Python helpers (render_metric_card, etc.)
  assets/design-system.css  # 1000+ lines: tokens, glassmorphism, Plotly theme
  pages/                # 5 pages: overview, map, sound, wildlife, conservation
scripts/download_datasets.py  # Synthetic data generator (run once)
data/                   # SQLite DB + sample audio/images
```

## Testing
- Only `tests/test_biodiversity.py` exists (unit tests for metrics)
- No integration tests, no fixtures
- Run: `pytest tests/ -v`

## Style / Conventions
- **Lint**: Ruff (line-length 88, pyproject.toml)
- **Imports**: Absolute from `src` (sys.path hack in app.py)
- **CSS**: Design tokens as CSS custom properties; glassmorphism via `backdrop-filter`
- **Charts**: Plotly dark eco template via `apply_plotly_theme()`
- **Spacing**: 8pt system via CSS vars (`--space-1`..`--space-16`)

## Environment
- Python ≥3.11 (tested on 3.14)
- GPU optional (PyTorch CUDA auto-detected)
- No external API keys needed (all local models)

## Debugging Checklist
- [ ] config.toml has no BOM
- [ ] Streamlit server restarted after styles.py changes
- [ ] `load_design_system()` called before any `st.*` calls
- [ ] `python scripts/download_datasets.py` run if DB missing
- [ ] Port 8501 free (or use `--server.port`)