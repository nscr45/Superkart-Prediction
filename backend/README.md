# SuperKart Prediction API

Flask API for the SuperKart trained sales prediction pipeline.

## API endpoints

- `GET /`: service information
- `GET /health`: API and model health
- `POST /predict`: returns the sales prediction

## Required runtime files

- `app.py`
- `Dockerfile`
- `requirements.txt`
- `superkart_complete_pipeline.joblib`

The model file must be the actual trained joblib binary, not a Git LFS pointer text file.

The API listens on port 7860 when run in its container. The Streamlit frontend is maintained and deployed separately.
