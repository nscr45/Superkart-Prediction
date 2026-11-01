"""React-based animated prediction result component."""

from pathlib import Path

import streamlit as st


_ASSET_DIR = Path(__file__).parent / "frontend" / "build"


def _load_inline_asset(pattern):
    """Load exactly one Vite asset as inline component content."""
    matches = list(_ASSET_DIR.glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one built asset matching {pattern!r}; found {len(matches)}."
        )
    # The leading newline makes Streamlit treat the bundle as inline content,
    # avoiding a runtime dependency on file-backed component asset discovery.
    return "\n" + matches[0].read_text(encoding="utf-8")


_component = st.components.v2.component(
    "superkart-ui.prediction_reveal",
    js=_load_inline_asset("index-*.js"),
    css=_load_inline_asset("*.css"),
    html='<div class="superkart-react-root"></div>',
)


def prediction_reveal(prediction, mrp, product_id, run_id, key=None):
    """Render an animated result card using values returned by the Flask API."""
    return _component(
        key=key,
        data={
            "prediction": float(prediction),
            "mrp": float(mrp),
            "product_id": str(product_id),
            "run_id": str(run_id),
        },
    )
