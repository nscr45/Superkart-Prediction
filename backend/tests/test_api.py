import numpy as np

import app as backend


class StubPipeline:
    def __init__(self, value=2750.5):
        self.value = value
        self.last_frame = None

    def predict(self, frame):
        self.last_frame = frame.copy()
        return np.array([self.value])


def valid_payload():
    return {
        "Product_Id": "FDX01",
        "Product_Weight": 12.5,
        "Product_Sugar_Content": "Low Fat",
        "Product_Allocated_Area": 0.04,
        "Product_Type": "Dairy",
        "Product_MRP": 125.0,
        "Store_Establishment_Year": 2005,
        "Store_Size": "Medium",
        "Store_Location_City_Type": "Tier 2",
        "Store_Type": "Supermarket Type1",
    }


def test_health_reports_model_state(monkeypatch):
    monkeypatch.setattr(backend, "pipeline", StubPipeline())
    response = backend.app.test_client().get("/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "healthy"
    assert payload["model_loaded"] is True


def test_predict_returns_numeric_prediction_and_summary(monkeypatch):
    model = StubPipeline()
    monkeypatch.setattr(backend, "pipeline", model)
    response = backend.app.test_client().post("/predict", json=valid_payload())

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "success"
    assert payload["prediction"] == 2750.5
    assert payload["input_summary"]["product_type"] == "Dairy"
    assert payload["input_summary"]["store_type"] == "Supermarket Type1"
    assert "Product_Id" not in model.last_frame.columns
    assert "Store_Age" not in model.last_frame.columns


def test_predict_rejects_missing_required_fields(monkeypatch):
    monkeypatch.setattr(backend, "pipeline", StubPipeline())
    response = backend.app.test_client().post(
        "/predict",
        json={"Product_Id": "FDX01"},
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["status"] == "error"
    assert "Missing required fields" in payload["error"]


def test_predict_reports_unavailable_model(monkeypatch):
    monkeypatch.setattr(backend, "pipeline", None)
    response = backend.app.test_client().post("/predict", json=valid_payload())

    assert response.status_code == 500
    assert response.get_json()["error"] == "Pipeline not loaded"


def test_predict_rejects_non_numeric_features(monkeypatch):
    monkeypatch.setattr(backend, "pipeline", StubPipeline())
    payload = valid_payload()
    payload["Product_MRP"] = "not-a-number"
    response = backend.app.test_client().post("/predict", json=payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Product_MRP must be a valid number"


def test_predict_rejects_non_object_json(monkeypatch):
    monkeypatch.setattr(backend, "pipeline", StubPipeline())
    response = backend.app.test_client().post("/predict", json=[valid_payload()])

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"
