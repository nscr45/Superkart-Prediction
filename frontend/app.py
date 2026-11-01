import streamlit as st
import pandas as pd

from config.settings import PAGE_CONFIG
from styles.css import get_custom_css
from utils.backend import check_backend_health
from components.single_item import render_single_item_prediction
from components.batch_prediction import render_batch_prediction
from components.compare_items import render_compare_items

st.set_page_config(**PAGE_CONFIG)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Keep UI state in Streamlit's main execution thread.
if "prediction_mode" not in st.session_state:
    st.session_state.prediction_mode = "Single Item"
if "saved_predictions" not in st.session_state:
    st.session_state.saved_predictions = []

MODES = ["Single Item", "Batch Prediction", "Compare Items"]
MODE_DETAILS = {
    "Single Item": ("01 / FORECAST", "Configure one product and store to estimate quarterly sales."),
    "Batch Prediction": ("02 / BATCH ANALYSIS", "Upload a dataset and generate predictions at scale."),
    "Compare Items": ("03 / COMPARISON", "Compare predicted sales and identify stronger performers."),
}

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div class="sk-brand">
            <div class="sk-brand-mark">S</div>
            <div>
                <div class="sk-brand-name">SuperKart</div>
                <div class="sk-brand-caption">Retail intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("#### WORKSPACE")
    selected_mode = st.radio(
        "Choose a workspace",
        MODES,
        index=MODES.index(st.session_state.prediction_mode),
        key="workspace_mode",
        label_visibility="collapsed",
    )
    if selected_mode != st.session_state.prediction_mode:
        st.session_state.prediction_mode = selected_mode
        st.rerun()

    st.markdown("---")
    st.markdown("#### SYSTEM STATUS")
    if st.button("↻ Check backend connection", use_container_width=True):
        st.session_state.backend_checked = True
        st.session_state.backend_is_healthy = check_backend_health()
    if "backend_is_healthy" not in st.session_state:
        st.session_state.backend_is_healthy = check_backend_health()
        st.session_state.backend_checked = True

    if st.session_state.backend_is_healthy:
        st.success("Backend reachable")
    else:
        st.error("Backend unavailable")
    st.caption("Prediction requests are served by the Flask API.")

    st.markdown("---")
    st.markdown("#### SESSION")
    saved = st.session_state.saved_predictions
    st.metric("Saved predictions", len(saved))
    if saved:
        saved_df = pd.DataFrame(saved)
        with st.expander("View saved results"):
            st.dataframe(saved_df, use_container_width=True, hide_index=True)
            st.download_button(
                "Export saved results",
                data=saved_df.to_csv(index=False),
                file_name="superkart_saved_predictions.csv",
                mime="text/csv",
                use_container_width=True,
            )
        if st.button("Clear saved results", use_container_width=True):
            st.session_state.saved_predictions = []
            st.rerun()
    else:
        st.caption("Your completed predictions will appear here when saved.")

    st.markdown("---")
    st.caption("SUPERKART · SALES INTELLIGENCE")
    st.caption("Machine learning • Flask • Streamlit")

# Main workspace
mode = st.session_state.prediction_mode
eyebrow, description = MODE_DETAILS[mode]
st.markdown(
    f"""
    <section class="sk-hero">
        <div class="sk-eyebrow">AI-POWERED RETAIL FORECASTING</div>
        <h1>Make every product decision count.</h1>
        <p>Turn product and store information into actionable sales forecasts.
        Explore predictions, analyse batches, and compare performance in one workspace.</p>
        <div class="sk-hero-tag">● &nbsp; {eyebrow} &nbsp; / &nbsp; {mode}</div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<div class="sk-section-kicker">{eyebrow}</div>', unsafe_allow_html=True)
st.markdown(f"## {mode}")
st.markdown(f'<p class="sk-muted">{description}</p>', unsafe_allow_html=True)

if mode == "Single Item":
    render_single_item_prediction()
elif mode == "Batch Prediction":
    uploaded_file = st.file_uploader(
        "Upload your prediction dataset",
        type=["csv", "json", "txt", "pdf"],
        help="Supported formats: CSV, JSON, TXT and PDF.",
        key="batch_dataset_uploader",
    )
    render_batch_prediction(uploaded_file)
else:
    render_compare_items()

st.markdown(
    """
    <div class="sk-footer">
        SUPERKART SALES PREDICTOR &nbsp;·&nbsp; Built with Streamlit and Flask
        <br>Forecast responsibly. Validate decisions with real-world performance.
    </div>
    """,
    unsafe_allow_html=True,
)
