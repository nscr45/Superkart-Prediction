import requests
import streamlit as st

from config.settings import BACKEND_URL


def check_backend_health():
    """Check the prediction API from the active Streamlit run."""
    try:
        response = requests.get(f"{BACKEND_URL.rstrip('/')}/health", timeout=5)
        response.raise_for_status()
        payload = response.json()
        healthy = payload.get("status") == "healthy" and payload.get("model_loaded", False)
    except (requests.RequestException, ValueError):
        healthy = False

    # This function is called only from Streamlit's main script execution.
    st.session_state.backend_is_healthy = healthy
    return healthy


def start_health_monitoring():
    """Backward-compatible entry point; no background thread is started."""
    if "backend_is_healthy" not in st.session_state:
        check_backend_health()
