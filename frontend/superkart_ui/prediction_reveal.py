"""React prediction card embedded as an inline Streamlit Components v2 bundle.

The bundle is read from the Vite production build at import time. Passing the
contents (rather than file paths) keeps component registration independent of
Streamlit's installed-package manifest discovery.
"""

from pathlib import Path

import streamlit as st


_ASSET_DIR = Path(__file__).resolve().parent / "frontend" / "build"


def _read_single(pattern: str) -> str:
    matches = list(_ASSET_DIR.glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one compiled component asset matching {pattern!r} "
            f"in {_ASSET_DIR}; found {len(matches)}. "
            "The React production build must run before Streamlit starts."
        )
    return matches[0].read_text(encoding="utf-8")


_JS_BUNDLE = _read_single("index-*.js")
_CSS_BUNDLE = _read_single("assets/*.css")

_component = st.components.v2.component(
    "superkart-ui.prediction_reveal",
    js=_JS_BUNDLE,
    css=_CSS_BUNDLE,
    html='<div class="superkart-react-root"></div>',
)


def prediction_reveal(prediction, mrp, product_id, run_id, key=None):
    """Render a result card using values returned by the Flask prediction API."""
    return _component(
        key=key,
        data={
            "prediction": float(prediction),
            "mrp": float(mrp),
            "product_id": str(product_id),
            "run_id": str(run_id),
        },
    )
