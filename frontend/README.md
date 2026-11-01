# SuperKart Frontend

Streamlit frontend for the SuperKart retail sales prediction application.

## Architecture

- Streamlit provides the application shell, navigation, Python workflows, uploads, and session state.
- React and TypeScript provide embedded interactive components through Streamlit Components v2.
- The frontend sends prediction requests to the separately deployed Flask backend.
- The trained model is not stored or loaded by this frontend.

## Configuration

Set the backend service URL using the `BACKEND_URL` environment variable. The default is the current SuperKart backend URL.

## Development

From this directory:

```bash
pip install -r requirements.txt
cd superkart_ui/frontend
npm install
npm run build
cd ../..
pip install .
streamlit run app.py
```

The React production bundle is generated during the Docker build. A separate React server is not required at runtime.
