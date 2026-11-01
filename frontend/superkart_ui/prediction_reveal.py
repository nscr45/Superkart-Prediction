"""React-based animated prediction result component."""

import streamlit as st


_component = st.components.v2.component(
    "superkart-ui.prediction_reveal",
    js="index-*.js",
    css="*.css",
    html='<div class="superkart-react-root"></div>',
)


def prediction_reveal(prediction, mrp, product_id, key=None):
    """Render an animated result card using values returned by the Flask API."""
    return _component(
        key=key,
        data={
            "prediction": float(prediction),
            "mrp": float(mrp),
            "product_id": str(product_id),
        },
    )
