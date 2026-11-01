from datetime import datetime
import math

from flask import Flask, jsonify, request
import joblib
import pandas as pd

app = Flask(__name__)

print("Starting SuperKart API...")

try:
    pipeline = joblib.load("superkart_complete_pipeline.joblib")
    print("Complete pipeline loaded successfully")
except Exception as exc:
    print(f"Error loading pipeline: {exc}")
    pipeline = None


MODEL_FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_Type",
    "Product_MRP",
    "Store_Establishment_Year",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
]

NUMERIC_FEATURES = {
    "Product_Weight",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Establishment_Year",
}


@app.route("/")
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API",
        "status": "active",
        "model_loaded": pipeline is not None,
        "endpoints": {"predict": "/predict", "health": "/health"},
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": pipeline is not None,
        "timestamp": datetime.now().isoformat(),
    })


@app.route("/predict", methods=["POST"])
def predict():
    if pipeline is None:
        return jsonify({"error": "Pipeline not loaded", "status": "error"}), 500

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Request body must be a non-empty JSON object",
            "status": "error",
        }), 400

    missing_fields = [field for field in MODEL_FEATURES if field not in data]
    if missing_fields:
        return jsonify({
            "error": f"Missing required fields: {missing_fields}",
            "status": "error",
        }), 400

    normalized = dict(data)
    for field in NUMERIC_FEATURES:
        try:
            value = float(normalized[field])
        except (TypeError, ValueError):
            return jsonify({
                "error": f"{field} must be a valid number",
                "status": "error",
            }), 400

        if not math.isfinite(value):
            return jsonify({
                "error": f"{field} must be a finite number",
                "status": "error",
            }), 400

        if field == "Store_Establishment_Year" and not value.is_integer():
            return jsonify({
                "error": "Store_Establishment_Year must be a whole number",
                "status": "error",
            }), 400

        normalized[field] = int(value) if field == "Store_Establishment_Year" else value

    for field in ("Product_Sugar_Content", "Product_Type", "Store_Size",
                  "Store_Location_City_Type", "Store_Type"):
        if not isinstance(normalized[field], str) or not normalized[field].strip():
            return jsonify({
                "error": f"{field} must be a non-empty string",
                "status": "error",
            }), 400

    product_id = normalized.get("Product_Id")
    if product_id is not None and not isinstance(product_id, str):
        return jsonify({
            "error": "Product_Id must be a string when provided",
            "status": "error",
        }), 400

    current_year = datetime.now().year
    normalized["Store_Age"] = current_year - normalized["Store_Establishment_Year"]

    if product_id:
        normalized["Product_Category_Code"] = product_id[:2]

    input_df = pd.DataFrame([{field: normalized[field] for field in MODEL_FEATURES}])

    try:
        prediction = pipeline.predict(input_df)
        prediction_value = float(prediction[0])
        if not math.isfinite(prediction_value):
            raise ValueError("Model returned a non-finite prediction")

        print(f"Prediction: {prediction_value:.2f}")
        return jsonify({
            "prediction": prediction_value,
            "status": "success",
            "derived_features": {
                "store_age": normalized.get("Store_Age"),
                "product_category_code": normalized.get("Product_Category_Code"),
            },
            "input_summary": {
                "product_type": normalized.get("Product_Type"),
                "store_type": normalized.get("Store_Type"),
                "mrp": normalized.get("Product_MRP"),
            },
        })
    except Exception as exc:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction could not be completed",
            "status": "error",
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
