# SuperKart Prediction

An AI-powered retail sales forecasting application with a Flask prediction API and a Streamlit user interface.

## Repository structure

```text
SuperKart-Prediction/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   └── superkart_complete_pipeline.joblib
└── frontend/
    ├── app.py
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    ├── components/
    ├── config/
    ├── src/
    ├── styles/
    └── utils/
```

## Applications

- **Backend:** Flask API serving the trained scikit-learn pipeline. Exposes `/`, `/health`, and `/predict`.
- **Frontend:** Streamlit application for single-item predictions, batch uploads, and item comparisons. It calls the backend API configured in `frontend/config/settings.py`.

## Deployment

The backend and frontend are deployed as separate Hugging Face Docker Spaces. Each application has its own Dockerfile, requirements file, and Space README metadata in its respective directory.

Deploy each directory from its own Space repository root, or configure the Space repository to use the matching subdirectory as its build context where supported.

## Notes

- The trained model is tracked with Git LFS.
- Do not commit access tokens or other secrets.
- Keep the backend API URL in the frontend configuration aligned with the active backend Space.
