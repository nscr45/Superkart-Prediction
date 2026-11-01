---
title: SuperKart Prediction API
sdk: docker
app_port: 7860
pinned: false
---

# SuperKart Prediction API

Flask API for the SuperKart trained sales prediction pipeline. This is the backend Space. The Streamlit frontend runs in a separate Space and sends server-to-server HTTP requests to this API.

## Required repository files

Keep these files at the root of this Space:

- `app.py`
- `Dockerfile`
- `requirements.txt`
- `superkart_complete_pipeline.joblib`

The model file must be the actual trained joblib binary, not a Git LFS pointer text file.

## API endpoints

- `GET /`: service information
- `GET /health`: API and model health
- `POST /predict`: returns the sales prediction

The Docker container listens on port 7860.
