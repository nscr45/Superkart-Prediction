# SuperKart React component layer

This package contains Streamlit Components v2 built with React and TypeScript.

## Local development

From the `frontend` directory:

```bash
python -m pip install -e .
cd superkart_ui/frontend
npm install
npm run dev
```

In a second terminal, run Streamlit from the `frontend` directory:

```bash
streamlit run app.py
```

## Production build

The Hugging Face Docker build installs Node 24, runs the Vite production build, then copies the compiled assets into the Python Streamlit image. The Streamlit app remains the entry point.

```bash
cd superkart_ui/frontend
npm ci
npm run build
```

The React component receives prediction values from Python after the Flask API returns a successful response. It does not call the prediction API directly and does not contain model logic.
