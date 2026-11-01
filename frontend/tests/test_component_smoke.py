from streamlit.testing.v1 import AppTest


def app():
    import streamlit as st
    from superkart_ui import prediction_reveal

    st.title("SuperKart component smoke test")
    prediction_reveal(
        prediction=2500.0,
        mrp=125.0,
        product_id="CI-TEST",
        run_id="component-smoke-test",
        key="component-smoke-test",
    )


def test_prediction_component_registers_and_mounts():
    app_test = AppTest.from_function(app).run()
    assert len(app_test.exception) == 0, app_test.exception
