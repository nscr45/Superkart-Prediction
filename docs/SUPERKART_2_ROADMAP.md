# SuperKart 2.0: Implementation Roadmap

## Product decision

- Frontend: React + TypeScript + Vite.
- Priority: complete, dependable product before decorative polish.
- Prediction engine: preserve the existing Flask application and trained scikit-learn pipeline at `backend/superkart_complete_pipeline.joblib`.
- Migration: build the React application alongside the existing Streamlit frontend. Retire Streamlit only after feature parity, deployment validation, and acceptance testing.
- UI rule: no emojis in interface copy, labels, charts, navigation, or status indicators.

## Target architecture

```text
SuperKart-Prediction/
├── backend/                 # Existing Flask API and trained pipeline
│   ├── app.py
│   ├── requirements.txt
│   └── tests/               # API contract and regression tests
├── frontend/                # Existing Streamlit app during migration
│   └── react-app/           # New React + TypeScript application
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   ├── features/
│       │   ├── lib/
│       │   ├── styles/
│       │   └── types/
│       ├── package.json
│       └── vite.config.ts
└── docs/
    └── SUPERKART_2_ROADMAP.md
```

The React client will communicate with Flask through a typed API client. The API base URL will be configured by environment variable, not hard-coded into components. Flask remains the source of prediction truth.

## Stage 1: Foundation and reliability

### Work
- Record the current repository structure, deployment assumptions, and prediction API contract.
- Add automated Flask API tests with a controlled test double for the model pipeline.
- Cover health status, valid prediction, missing input, and unavailable model behavior.
- Establish CI so backend contract tests run on pushes and pull requests.
- Audit feature names, required inputs, derived features, response shape, model artifact handling, dependency pins, and CORS/deployment requirements.
- Keep the production model artifact and prediction algorithm unchanged.

### Exit criteria
- API tests pass without requiring the production model binary.
- Tests prove the expected input and response contract.
- CI runs automatically.
- Any API changes are backward-compatible or explicitly versioned.
- The model artifact remains untouched.

## Stage 2: React application foundation

- Scaffold React + TypeScript + Vite under `frontend/react-app`.
- Establish typed API request/response models, environment configuration, routing, error boundaries, and reusable form controls.
- Build responsive navigation and the shared application shell.
- Define design tokens, typography, spacing, chart styling, focus states, and reduced-motion behavior.
- Add frontend unit and component tests.
- Keep Streamlit deployable until React reaches feature parity.

## Stage 3: Single prediction experience

- Recreate every supported model input with clear labels, units, defaults only where justified, and inline validation.
- Submit to the existing Flask `/predict` endpoint.
- Provide real loading and error states; do not simulate progress.
- Reveal result metrics and charts only after a successful response.
- Add prediction save/export behavior.
- Label the model output accurately; do not imply time-series forecasting or confidence intervals unless the model supports them.

## Stage 4: Batch prediction centre

- Support CSV, JSON, TXT, and PDF where extraction is reliable.
- Validate schema, types, missing values, duplicates, and row limits before sending requests.
- Show row-level success/failure, progress, retry options, and a downloadable error report.
- Avoid joining results on Product_Id alone where duplicate product IDs can occur.
- Provide sortable/filterable results and CSV export; add XLSX/PDF only after validating their output.

## Stage 5: Comparison workspace

- Compare 2–10 distinct records with stable row identifiers.
- Validate zero, null, and invalid values before ratio calculations.
- Distinguish predicted sales from MRP and clearly label Sales/MRP as a descriptive ratio, not profit or margin.
- Provide side-by-side metrics, charts, rankings, and exports.

## Stage 6: Analytics and intelligence

- Add prediction history with durable persistence only after selecting and securing a storage layer.
- Add store, product-type, and category breakdowns from actual prediction records.
- Add filters, anomaly flags, and scenario comparisons with transparent assumptions.
- Add explainability only if supported by the trained pipeline and validated methodology.
- Do not invent confidence scores, future sales trends, or causal recommendations.

## Stage 7: Production readiness

- Add integration and end-to-end tests for single, batch, comparison, and export workflows.
- Verify CORS, HTTPS, environment configuration, request limits, timeouts, logging, and secret handling.
- Test responsive layouts, keyboard navigation, screen-reader labels, and reduced-motion preferences.
- Verify deployment and health checks for the Flask API and React static frontend.
- Remove Streamlit only after parity and deployment acceptance.

## Product acceptance checklist

- Every visible action works and has a clear success, empty, loading, or error state.
- No fake progress, placeholder charts presented as real data, dead buttons, or misleading metrics.
- Predictions and charts are derived from actual Flask responses.
- Currency and units are consistent and explicit.
- Batch results preserve row identity, including duplicate Product_Id values.
- Data can be exported and reopened correctly.
- Layout works on desktop, tablet, and mobile.
- No emojis appear in the UI.
- The existing Flask model and model artifact remain intact.
