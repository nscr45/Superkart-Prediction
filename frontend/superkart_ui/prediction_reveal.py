"""React-based prediction result component registered as a package component."""

import streamlit as st


# Asset paths are resolved relative to asset_dir in superkart_ui/pyproject.toml.
# Streamlit expects paths/globs here, not filesystem Path objects or file contents.
_component = st.components.v2.component(
    "superkart-ui.prediction_reveal",
    js="index-*.js",
    css="assets/*.css",
    html='<div class="superkart-react-root"></div>',
)


def prediction_reveal(prediction, mrp, product_id, run_id, key=None):
    """Render the prediction result returned by the Flask API."""
    return _component(
        key=key,
        data={
            "prediction": float(prediction),
            "mrp": float(mrp),
            "product_id": str(product_id),
            "run_id": str(run_id),
        },
    )
