# SuperKart Prediction

A retail sales prediction application built around the existing trained scikit-learn pipeline, a Flask prediction API, and a Streamlit application deployed on Hugging Face Spaces.

## SuperKart 2.0 architecture

The deployment uses **two separate Hugging Face Spaces**:

1. **Backend Space:** Flask + Gunicorn + the trained `superkart_complete_pipeline.joblib` model. It exposes the prediction API on port 7860.
2. **Frontend Space:** Streamlit application on port 7860. It embeds the React + TypeScript UI components and calls the backend Space through Python requests.

React is not deployed as a third Space or as a separate web server. Its production bundle is compiled during the frontend Docker build and rendered inside Streamlit using Components v2.

## Repository structure

```text
SuperKart-Prediction/
├── backend/                 # Copy contents into the backend HF Space
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   └── superkart_complete_pipeline.joblib
├── frontend/                # Copy contents into the frontend HF Space
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   ├── components/
│   ├── config/
│   ├── styles/
│   ├── utils/
│   └── superkart_ui/
└── docs/
```

## Deploy the backend Space first

Create or use a Hugging Face Space with **Docker** as its SDK. Copy the contents of the repository's `backend/` directory into the root of that Space. Ensure the actual trained model binary is present at the Space root as `superkart_complete_pipeline.joblib`.

The backend Space URL should look like:

```text
https://<your-backend-space-subdomain>.hf.space
```

Its health endpoint is `/health` and prediction endpoint is `/predict`.

## Deploy the frontend Space

Create or use a second Hugging Face Space with **Docker** as its SDK. Copy the contents of the repository's `frontend/` directory into the root of that Space. The Docker build installs Node, builds the React component bundle, installs the Python app, and starts Streamlit on port 7860.

In the frontend Space, open **Settings → Variables and secrets** and add:

- Name: `BACKEND_URL`
- Value: the full public URL of the backend Space, without a trailing slash

For the currently configured backend Space, the value is:

```text
https://sricharan451706-superkart-api-backend.hf.space
```

If the backend Space has a different URL, use that exact URL instead.

## Existing workflows

1. Single-item prediction
2. Batch prediction from CSV, JSON, TXT, and PDF
3. Product/store comparison

## Local development

### Backend

From `backend/`:

```bash
pip install -r requirements.txt
python app.py
```

### Frontend

From `frontend/`:

```bash
pip install -r requirements.txt
cd superkart_ui/frontend
npm install
npm run build
cd ../..
pip install .
streamlit run app.py
```

## Model and data integrity

- The existing trained pipeline remains the prediction source.
- The React component layer contains presentation logic only.
- The frontend does not need a copy of the model.
- Sales/MRP is a descriptive ratio, not profit margin or model confidence.
- No emojis are used in the application UI.
