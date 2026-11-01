# SuperKart Prediction

A retail sales prediction application built around a trained scikit-learn pipeline, a Flask prediction API, and a Streamlit application deployed on Hugging Face Spaces.

## SuperKart 2.0 architecture

- **Streamlit:** primary application framework, navigation, Python workflows, file handling, and session state.
- **React + TypeScript:** interactive UI components embedded through Streamlit Components v2 and built with Vite.
- **Flask:** prediction API serving the existing trained model pipeline.
- **Hugging Face Spaces:** Docker-based hosting for the Streamlit frontend and Flask backend as separate services.

React is not deployed as a separate application. The frontend component bundle is compiled during the Streamlit Docker build and served by Streamlit. Python passes prediction results into React components; the React layer does not load or modify the model.

## Repository structure

```text
SuperKart-Prediction/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── tests/
│   └── superkart_complete_pipeline.joblib
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── components/
│   ├── config/
│   ├── styles/
│   ├── utils/
│   └── superkart_ui/
│       ├── prediction_reveal.py
│       └── frontend/              # React + TypeScript component source
└── docs/
    └── SUPERKART_2_ROADMAP.md
```

## Existing workflows

1. Single-item prediction
2. Batch prediction from CSV, JSON, TXT, and PDF
3. Product/store comparison

## Development

### Backend

From the `backend` directory:

```bash
pip install -r requirements.txt
python app.py
```

Run API contract tests:

```bash
cd backend
pip install pytest
pytest -q
```

### Streamlit + React frontend

The frontend requires Python 3.10+ and Node.js 24+.

From the `frontend` directory:

```bash
pip install -r requirements.txt
pip install -e .
cd superkart_ui/frontend
npm install
npm run build
cd ../..
streamlit run app.py
```

For component development, run `npm run dev` in the component frontend directory while Streamlit runs in a second terminal.

## Hugging Face deployment

The frontend Space uses the Docker SDK and listens on port 8501. Its Docker build compiles the React component bundle with Node 24, installs the Python component package, and starts Streamlit. The backend Space remains a separate Flask/Gunicorn service on port 7860.

Configure the backend URL through the frontend configuration and keep it aligned with the deployed Flask Space.

## Project plan

See [SuperKart 2.0 Implementation Roadmap](docs/SUPERKART_2_ROADMAP.md) for the staged implementation and release acceptance criteria.

## Model and data integrity

- The existing trained pipeline remains the prediction source.
- The React component layer contains presentation logic only.
- Charts and metrics must use real prediction outputs or clearly labelled calculations.
- Do not present Sales/MRP as profit margin or model confidence.
- No emojis are used in the application UI.
