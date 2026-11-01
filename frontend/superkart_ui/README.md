# SuperKart React component layer

This package contains Streamlit Components v2 built with React and TypeScript.

## Local development

From the `frontend` directory, build the component assets and install the Python package as a regular package so Streamlit can discover its component metadata:

```bash
cd superkart_ui/frontend
npm install
npm run build
cd ../..
python -m pip install .
streamlit run app.py
```

For active React development, keep the Streamlit app running in a second terminal and use the Vite watcher:

```bash
cd superkart_ui/frontend
npm run dev
```

Refresh the Streamlit page after Vite rebuilds the component.

## Production build

The Hugging Face Docker build installs Node 24, runs the Vite production build, then copies the compiled assets into the Python Streamlit image. The Streamlit app remains the entry point.

```bash
cd superkart_ui/frontend
npm install
npm run build
```

The React component receives prediction values from Python after the Flask API returns a successful response. It does not call the prediction API directly and does not contain model logic.
