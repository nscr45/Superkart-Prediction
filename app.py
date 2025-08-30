from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

print("Starting SuperKart API...")

# Load model and preprocessor
try:
    model = joblib.load('superkart_sales_model.joblib')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

try:
    preprocessor = joblib.load('feature_info.pkl')
    print("Preprocessor loaded successfully")
except Exception as e:
    print(f"Error loading preprocessor: {e}")
    preprocessor = None

@app.route('/')
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API",
        "status": "active",
        "version": "1.0",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None,
        "endpoints": {
            "predict": "/predict",
            "health": "/health"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None or preprocessor is None:
            return jsonify({
                "error": "Model or preprocessor not loaded",
                "status": "error"
            }), 500

        data = request.get_json()
        if not data:
            return jsonify({
                "error": "No input data provided",
                "status": "error"
            }), 400

        # Required fields for prediction
        required_fields = [
            'Product_Category_Code', 'Product_Weight', 'Product_Sugar_Content', 'Product_Allocated_Area',
            'Product_Type', 'Product_MRP', 'Store_Establishment_Year',
            'Store_Size', 'Store_Location_City_Type', 'Store_Type',
            'Store_Age'
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {missing_fields}",
                "status": "error"
            }), 400

        # Create DataFrame for prediction
        input_df = pd.DataFrame([data])
        print(f"Input data shape: {input_df.shape}")
        
        # Apply preprocessing
        processed_data = preprocessor.transform(input_df)
        print(f"Processed data shape: {processed_data.shape}")
        
        # Make prediction
        prediction = model.predict(processed_data)
        print(f"Prediction: {prediction[0]}")

        return jsonify({
            "prediction": float(prediction[0]),
            "status": "success",
            "input_summary": {
                "product_id": data.get('Product_Category_Code'),
                "product_weight": data.get('Product_Weight'),
                "product_type": data.get('Product_Type'),
                "store_type": data.get('Store_Type'),
                "mrp": data.get('Product_MRP'),
                "store_age": data.get('Store_Age')
            }
        })

    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    print("Starting Flask server on 0.0.0.0:7860")
    app.run(host='0.0.0.0', port=7860, debug=False)
