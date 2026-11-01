# SuperKart 2.0: Implementation Roadmap

## Product decisions

- Hosting and application framework: Streamlit on Hugging Face Spaces (Docker SDK).
- Interactive frontend layer: React + TypeScript using Streamlit Components v2.
- Backend: preserve the existing Flask API and trained scikit-learn pipeline at `backend/superkart_complete_pipeline.joblib`.
- Priority: complete, dependable product before decorative polish.
- Migration: progressively replace Streamlit-rendered UI sections with React components. Keep Streamlit responsible for navigation, Python workflows, session state, uploads, and deployment.
- UI rule: no emojis in interface copy, labels, charts, navigation, or status indicators.

## Target architecture

```text
SuperKart-Prediction/
├── backend/                         # Existing Flask API and model
│   ├── app.py
│   ├── requirements.txt
│   └── tests/
├── frontend/                        # Hugging Face Streamlit Space root
│   ├── app.py                        # Streamlit shell and workflows
│   ├── components/                   # Existing Python workflows
│   ├── superkart_ui/                 # Streamlit Components v2 package
│   │   ├── __init__.py
│   │   ├── pyproject.toml
│   │   └── frontend/
│   │       ├── src/                  # React + TypeScript source
│   │       ├── package.json
│   │       ├── tsconfig.json
│   │       └── vite.config.ts
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── Dockerfile
└── docs/
    └── SUPERKART_2_ROADMAP.md
```

The Streamlit Python app mounts React components and exchanges JSON state with them. The Flask API remains the sole prediction source. The React layer does not load or duplicate the model.

## Stage 1: Foundation and reliability

### Work
- Record repository structure, deployment assumptions, and prediction API contract.
- Add Flask API tests with a controlled model test double.
- Cover health status, valid prediction, missing input, invalid numeric input, malformed request, and unavailable model.
- Establish GitHub Actions for backend contract tests.
- Audit model feature names, derived features, response shape, model artifact handling, dependency pins, CORS, and deployment requirements.
- Preserve the production model artifact and prediction algorithm.

### Exit criteria
- API tests pass without requiring the production model binary.
- Tests prove the expected request and response contract.
- CI runs automatically.
- The model artifact remains untouched.
- Hugging Face deployment assumptions are documented.

## Stage 2: Streamlit + React foundation

- Upgrade the frontend runtime to Python 3.10+ and Streamlit 1.51+ for Components v2.
- Build the React + TypeScript component package with Vite and the official Streamlit component-v2 library.
- Compile the React bundle during the Hugging Face Docker build using Node 24; serve the built assets through Streamlit's component package.
- Keep Streamlit as the app shell, navigation, session-state owner, file upload handler, and Python orchestration layer.
- Add typed component data/state contracts, lifecycle cleanup, accessible controls, responsive styling, and reduced-motion support.
- Add CI checks for TypeScript typechecking and production component build.
- Integrate a first React prediction-result component without changing the Flask API.
- Keep existing Python workflows available as fallback until each React-enhanced workflow is verified.

## Stage 3: Single prediction experience

- Preserve the existing Python form validation and Flask request workflow initially.
- Replace the static result presentation with React result cards and meaningful reveal animation after a successful API response.
- Use only actual API response values; never simulate progress or fabricate chart data.
- Keep arithmetic breakdowns clearly labelled as derived estimates, not observed time series.
- Add accessible loading, success, empty, and error states.
- Preserve save-to-session and JSON export behavior.

## Stage 4: Batch prediction centre

- Support CSV, JSON, TXT, and PDF where extraction is reliable.
- Validate schema, types, missing values, duplicates, and row limits before requests.
- Show row-level success/failure, progress based on completed requests, retry options, and a downloadable error report.
- Preserve row identity even when Product_Id values repeat.
- Add sortable/filterable results and CSV export; add XLSX/PDF only after validating their output.

## Stage 5: Comparison workspace

- Compare 2–10 distinct records with stable row identifiers.
- Validate zero, null, and invalid values before ratio calculations.
- Clearly label Sales/MRP as a descriptive ratio, not profit or margin.
- Provide side-by-side metrics, interactive charts, rankings, and exports.

## Stage 6: Analytics and intelligence

- Add prediction history with durable persistence only after selecting and securing a storage layer.
- Add store, product-type, and category breakdowns from actual prediction records.
- Add filters, anomaly flags, and scenario comparisons with transparent assumptions.
- Add explainability only if supported by the trained pipeline and validated methodology.
- Do not invent confidence scores, future sales trends, or causal recommendations.

## Stage 7: Production readiness

- Add integration and end-to-end tests for single, batch, comparison, and export workflows.
- Verify Hugging Face Docker builds, CORS, HTTPS, environment configuration, request limits, timeouts, logging, and secret handling.
- Test responsive layouts, keyboard navigation, screen-reader labels, and reduced-motion preferences.
- Verify Flask API health and Streamlit component asset loading in the deployed Space.
- Remove obsolete UI code only after feature parity and deployment acceptance.

## Product acceptance checklist

- Every visible action works and has a clear success, empty, loading, or error state.
- No fake progress, placeholder charts presented as real data, dead buttons, or misleading metrics.
- Predictions and visualisations are derived from actual Flask responses or clearly labelled calculations.
- Currency and units are consistent and explicit.
- Batch results preserve row identity, including duplicate Product_Id values.
- Data can be exported and reopened correctly.
- Layout works on desktop, tablet, and mobile.
- Motion respects reduced-motion preferences.
- No emojis appear in the UI.
- The existing Flask model and model artifact remain intact.
- The application deploys as a Hugging Face Docker Space with Streamlit as its entry point.
