from flask import Flask, request, jsonify
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

print("Starting SuperKart API...")

# Load complete pipeline
try:
    pipeline = joblib.load('superkart_complete_pipeline.joblib')
    print("Complete pipeline loaded successfully")
except Exception as e:
    print(f"Error loading pipeline: {e}")
    pipeline = None

@app.route('/')
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API",
        "status": "active",
        "model_loaded": pipeline is not None,
        "endpoints": {
            "predict": "/predict",
            "health": "/health"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": pipeline is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if pipeline is None:
            return jsonify({
                "error": "Pipeline not loaded",
                "status": "error"
            }), 500
            
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "No input data provided",
                "status": "error"
            }), 400
        
        # Dynamic feature engineering in backend
        current_year = datetime.now().year
        
        # Calculate Store_Age dynamically
        if 'Store_Establishment_Year' in data:
            data['Store_Age'] = current_year - data['Store_Establishment_Year']
        
        # Extract Product_Category_Code from Product_Id
        if 'Product_Id' in data:
            data['Product_Category_Code'] = data['Product_Id'][:2]
            # Remove Product_Id as it's not needed for model input
            data.pop('Product_Id')
        
        # Required fields for model input (including derived features)
        required_fields = [
            'Product_Weight', 'Product_Sugar_Content', 'Product_Allocated_Area',
            'Product_Type', 'Product_MRP', 'Store_Establishment_Year',
            'Store_Size', 'Store_Location_City_Type', 'Store_Type'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {missing_fields}",
                "status": "error"
            }), 400
        
        # Create DataFrame for prediction (using only base features for model)
        model_features = [
            'Product_Weight', 'Product_Sugar_Content', 'Product_Allocated_Area',
            'Product_Type', 'Product_MRP', 'Store_Establishment_Year',
            'Store_Size', 'Store_Location_City_Type', 'Store_Type'
        ]
        
        input_dict = {k: data[k] for k in model_features if k in data}
        input_df = pd.DataFrame([input_dict])
        
        print(f"Input data: {input_dict}")
        
        # Make prediction using complete pipeline
        prediction = pipeline.predict(input_df)
        
        print(f"Prediction: ${prediction[0]:.2f}")
        
        return jsonify({
            "prediction": float(prediction[0]),
            "status": "success",
            "derived_features": {
                "store_age": data.get('Store_Age'),
                "product_category_code": data.get('Product_Category_Code')
            },
            "input_summary": {
                "product_type": data.get('Product_Type'),
                "store_type": data.get('Store_Type'),
                "mrp": data.get('Product_MRP')
            }
        })
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=False)
