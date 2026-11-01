import streamlit as st
import requests
import threading
import time
from config.settings import BACKEND_URL

def check_backend_health():
    """Silent backend health check"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            st.session_state.backend_status = "up"
            return True
        else:
            st.session_state.backend_status = "down"
            return False
    except:
        st.session_state.backend_status = "down"
        return False

def background_health_monitor():
    """Background thread to monitor health"""
    while True:
        check_backend_health()
        time.sleep(60)  # Check every minute

def start_health_monitoring():
    """Initialize backend health monitoring"""
    if 'backend_status' not in st.session_state:
        st.session_state.backend_status = "unknown"
    
    if 'health_monitor_started' not in st.session_state:
        threading.Thread(target=background_health_monitor, daemon=True).start()
        st.session_state.health_monitor_started = True
