---
title: SuperKart Sales Predictor
sdk: docker
app_port: 7860
pinned: false
---

# SuperKart Sales Predictor

Streamlit frontend for SuperKart retail sales forecasting. This Space is the user-facing application and connects to a separate Flask backend Space.

## Space configuration

In **Settings → Variables and secrets**, add this variable:

- `BACKEND_URL`: `https://sricharan451706-superkart-api-backend.hf.space`

Use the actual public URL of your backend Space if its owner or Space slug differs.

Do not put the model file in this frontend Space. The trained model belongs in the backend Space only.

## Runtime

This Space uses the Docker SDK. The Docker build compiles the React + TypeScript component bundle and starts Streamlit on port 7860. No separate React server is required at runtime.

The React component is embedded in Streamlit through Components v2. Prediction requests are sent from Python to the backend Space.
