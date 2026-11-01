import streamlit as st
import datetime
import requests
import time
import json
from config.settings import PRODUCT_OPTIONS, VALIDATION_LIMITS, BACKEND_URL
from utils.helpers import format_currency, get_business_insights
from utils.backend import check_backend_health

def render_single_item_prediction():
 """Render the single item prediction interface"""
 st.markdown("## **Product & Store Configuration**")
 
 col1, col2 = st.columns(2, gap="large")
 
 with col1:
 st.markdown("### **Product Details**")
 
 product_id = st.text_input(
 "Product ID", 
 value="",
 placeholder="Enter Product ID (e.g., DR123, FD456)",
 help="Format: 2 letters + numbers"
 )
 
 product_weight_input = st.text_input(
 "Product Weight (kg)", 
 value="",
 placeholder="Enter weight (e.g., 12.5)",
 help="Weight of the product in kilograms"
 )
 
 product_sugar_content = st.selectbox(
 "Sugar Content",
 options=PRODUCT_OPTIONS["sugar_content"],
 index=0,
 help="Select sugar/fat content level"
 )
 
 product_allocated_area_input = st.text_input(
 "Product Allocated Area",
 value="",
 placeholder="Enter area (e.g., 0.045)",
 help="Ratio of display area (0.001-0.200)"
 )
 
 product_type = st.selectbox(
 "Product Type",
 options=PRODUCT_OPTIONS["product_types"],
 index=0,
 help="Select primary category of the product"
 )
 
 product_mrp_input = st.text_input(
 "Product MRP (₹)",
 value="",
 placeholder="Enter price (e.g., 145.50)",
 help="Maximum Retail Price in Indian Rupees"
 )
 
 with col2:
 st.markdown("### **Store Information**")
 
 current_year = datetime.datetime.now().year
 
 store_establishment_year_input = st.text_input(
 "Store Establishment Year",
 value="",
 placeholder="Enter year (e.g., 2010)",
 help="Year when the store was established"
 )
 
 store_size = st.selectbox(
 "Store Size",
 options=PRODUCT_OPTIONS["store_sizes"],
 index=0,
 help="Select physical size category of the store"
 )
 
 store_location_city_type = st.selectbox(
 "Store Location City Type",
 options=PRODUCT_OPTIONS["city_types"],
 index=0,
 help="Select city classification"
 )
 
 store_type = st.selectbox(
 "Store Type",
 options=PRODUCT_OPTIONS["store_types"],
 index=0,
 help="Select store format and operational model"
 )
 
 # Input Validation Section
 st.markdown("---")
 
 validation_errors = []
 validated_data = {}
 
 # Validate Product ID
 if not product_id.strip():
 validation_errors.append("Product ID is required")
 else:
 validated_data['product_id'] = product_id.strip()
 
 # Validate Product Weight
 try:
 if not product_weight_input.strip():
 validation_errors.append("Product Weight is required")
 else:
 product_weight = float(product_weight_input)
 if product_weight <= VALIDATION_LIMITS["product_weight"]["min"] or product_weight > VALIDATION_LIMITS["product_weight"]["max"]:
 validation_errors.append(f"Product Weight must be between {VALIDATION_LIMITS['product_weight']['min']} and {VALIDATION_LIMITS['product_weight']['max']} kg")
 else:
 validated_data['product_weight'] = product_weight
 except ValueError:
 validation_errors.append("Product Weight must be a valid number")
 
 # Validate Sugar Content
 if not product_sugar_content:
 validation_errors.append("Sugar Content selection is required")
 else:
 validated_data['product_sugar_content'] = product_sugar_content
 
 # Validate Allocated Area
 try:
 if not product_allocated_area_input.strip():
 validation_errors.append("Product Allocated Area is required")
 else:
 product_allocated_area = float(product_allocated_area_input)
 if product_allocated_area <= VALIDATION_LIMITS["allocated_area"]["min"] or product_allocated_area > VALIDATION_LIMITS["allocated_area"]["max"]:
 validation_errors.append(f"Allocated Area must be between {VALIDATION_LIMITS['allocated_area']['min']} and {VALIDATION_LIMITS['allocated_area']['max']}")
 else:
 validated_data['product_allocated_area'] = product_allocated_area
 except ValueError:
 validation_errors.append("Allocated Area must be a valid number")
 
 # Validate Product Type
 if not product_type:
 validation_errors.append("Product Type selection is required")
 else:
 validated_data['product_type'] = product_type
 
 # Validate Product MRP
 try:
 if not product_mrp_input.strip():
 validation_errors.append("Product MRP is required")
 else:
 product_mrp = float(product_mrp_input)
 if product_mrp <= VALIDATION_LIMITS["product_mrp"]["min"] or product_mrp > VALIDATION_LIMITS["product_mrp"]["max"]:
 validation_errors.append(f"Product MRP must be between ₹{VALIDATION_LIMITS['product_mrp']['min']} and ₹{VALIDATION_LIMITS['product_mrp']['max']}")
 else:
 validated_data['product_mrp'] = product_mrp
 except ValueError:
 validation_errors.append("Product MRP must be a valid number")
 
 # Validate Store Establishment Year
 try:
 if not store_establishment_year_input.strip():
 validation_errors.append("Store Establishment Year is required")
 else:
 store_establishment_year = int(store_establishment_year_input)
 if store_establishment_year < VALIDATION_LIMITS["store_year"]["min"] or store_establishment_year > VALIDATION_LIMITS["store_year"]["max"]:
 validation_errors.append(f"Store Year must be between {VALIDATION_LIMITS['store_year']['min']} and {VALIDATION_LIMITS['store_year']['max']}")
 else:
 validated_data['store_establishment_year'] = store_establishment_year
 except ValueError:
 validation_errors.append("Store Year must be a valid 4-digit year")
 
 # Validate Store Size
 if not store_size:
 validation_errors.append("Store Size selection is required")
 else:
 validated_data['store_size'] = store_size
 
 # Validate Location Type
 if not store_location_city_type:
 validation_errors.append("Store Location Type selection is required")
 else:
 validated_data['store_location_city_type'] = store_location_city_type
 
 # Validate Store Type
 if not store_type:
 validation_errors.append("Store Type selection is required")
 else:
 validated_data['store_type'] = store_type
 
 # Display Validation Status
 if validation_errors:
 st.error("**Please complete all required fields:**")
 for error in validation_errors:
 st.write(f"• {error}")
 
 completed_fields = len(validated_data)
 total_fields = 10
 progress_pct = (completed_fields / total_fields) * 100
 
 st.progress(completed_fields / total_fields)
 st.info(f"**Form Progress**: {completed_fields}/{total_fields} fields completed ({progress_pct:.0f}%)")
 
 else:
 st.success("**All fields completed successfully!**")
 
 store_age = current_year - validated_data['store_establishment_year']
 product_category_code = validated_data['product_id'][:2] if validated_data['product_id'] else "N/A"
 
 st.markdown("####**Derived Features**")
 col_age, col_code = st.columns(2)
 with col_age:
 st.metric("Store Age", f"{store_age} years")
 with col_code:
 st.metric("Category Code", product_category_code)
 
 # Prediction Section
 st.markdown("---")
 st.markdown("## **Sales Prediction**")
 
 prediction_col1, prediction_col2, prediction_col3 = st.columns([1, 2, 1])
 
 with prediction_col2:
 predict_button = st.button(
 "**Predict Quarterly Sales**",
 type="primary",
 disabled=bool(validation_errors),
 use_container_width=True,
 help="Complete all fields above to enable prediction"
 )
 
 if predict_button:
 if validation_errors:
 st.error("**Cannot predict**: Please complete all required fields above")
 else:
 backend_healthy = check_backend_health()
 
 if not backend_healthy:
 st.error("**Service temporarily unavailable**. Please try again in a moment.")
 else:
 input_data = {
 "Product_Id": validated_data['product_id'],
 "Product_Weight": validated_data['product_weight'],
 "Product_Sugar_Content": validated_data['product_sugar_content'],
 "Product_Allocated_Area": validated_data['product_allocated_area'],
 "Product_Type": validated_data['product_type'],
 "Product_MRP": validated_data['product_mrp'],
 "Store_Establishment_Year": validated_data['store_establishment_year'],
 "Store_Size": validated_data['store_size'],
 "Store_Location_City_Type": validated_data['store_location_city_type'],
 "Store_Type": validated_data['store_type']
 }
 
 try:
 with st.spinner(" **Analyzing data and generating prediction...**"):
 progress_bar = st.progress(0)
 for i in range(100):
 time.sleep(0.01)
 progress_bar.progress(i + 1)
 
 response = requests.post(f"{BACKEND_URL}/predict", json=input_data, timeout=30)
 progress_bar.empty()
 
 if response.status_code == 200:
 result = response.json()
 prediction = result.get("prediction")
 derived_features = result.get("derived_features", {})
 
 # Enhanced Performance-Based Animation
 from config.settings import PERFORMANCE_THRESHOLDS
 
 if prediction < PERFORMANCE_THRESHOLDS["low"]:
 st.error(" **Low Sales Prediction Alert**")
 st.warning("Consider optimization strategies to improve performance")
 elif prediction >= PERFORMANCE_THRESHOLDS["high"]:
 # Celebration animation intentionally omitted for a restrained interface.
 st.success(" **Excellent Sales Prediction!**")
 st.info("Outstanding performance expected - ensure adequate inventory")
 else:
 st.success("**Prediction Generated Successfully!**")
 
 # Save prediction data to session state for comparison
 if 'saved_predictions' not in st.session_state:
 st.session_state.saved_predictions = []
 
 # Create prediction record
 prediction_record = input_data.copy()
 prediction_record['Predicted_Sales'] = prediction
 prediction_record['Timestamp'] = datetime.datetime.now().isoformat()
 prediction_record['Prediction_Source'] = 'Single Item'
 
 # Check if this combination already exists and update or add
 existing_index = None
 for i, existing in enumerate(st.session_state.saved_predictions):
 if (existing['Product_Id'] == prediction_record['Product_Id'] and 
 existing['Store_Type'] == prediction_record['Store_Type']):
 existing_index = i
 break
 
 if existing_index is not None:
 st.session_state.saved_predictions[existing_index] = prediction_record
 st.info(" Prediction updated in comparison database")
 else:
 st.session_state.saved_predictions.append(prediction_record)
 st.info(" Prediction saved to comparison database")
 
 # Main Result Display
 st.markdown("### **Revenue Forecast**")
 
 metric_col1, metric_col2, metric_col3 = st.columns(3)
 
 with metric_col1:
 st.metric(
 "Predicted Sales",
 format_currency(prediction),
 delta=f"+{prediction/validated_data['product_mrp']:.1f}x MRP"
 )
 
 with metric_col2:
 st.metric(
 "Revenue Multiple",
 f"{prediction/validated_data['product_mrp']:.1f}x",
 delta="vs Product MRP"
 )
 
 with metric_col3:
 weekly_avg = prediction / 12
 st.metric(
 "Weekly Average",
 format_currency(weekly_avg),
 delta="Per week estimate"
 )
 
 # Detailed Analysis
 st.markdown("---")
 st.markdown("### **Prediction Analysis**")
 
 insights = get_business_insights(prediction, validated_data['product_mrp'])
 st.markdown(f"**Business Insight**: {insights}")
 
 analysis_col1, analysis_col2 = st.columns(2)
 
 with analysis_col1:
 st.markdown("#### **Product Profile**")
 st.info(f"""
 - **ID**: {validated_data['product_id']}
 - **Category**: {validated_data['product_type']}
 - **Weight**: {validated_data['product_weight']}kg
 - **MRP**: {format_currency(validated_data['product_mrp'])}
 - **Sugar Content**: {validated_data['product_sugar_content']}
 - **Display Area**: {validated_data['product_allocated_area']:.3f}
 """)
 
 with analysis_col2:
 st.markdown("#### **Store Profile**")
 store_age = current_year - validated_data['store_establishment_year']
 st.info(f"""
 - **Type**: {validated_data['store_type']}
 - **Size**: {validated_data['store_size']}
 - **Location**: {validated_data['store_location_city_type']} City
 - **Age**: {store_age} years
 - **Established**: {validated_data['store_establishment_year']}
 - **Category Code**: {derived_features.get('product_category_code', 'N/A')}
 """)
 
 # Revenue Breakdown
 st.markdown("#### **Revenue Breakdown**")
 breakdown_data = {
 "Metric": [
 "Quarterly Revenue",
 "Monthly Average", 
 "Weekly Average",
 "Daily Average",
 "Revenue per MRP Unit"
 ],
 "Amount": [
 format_currency(prediction),
 format_currency(prediction/3),
 format_currency(prediction/12),
 format_currency(prediction/90),
 f"{prediction/validated_data['product_mrp']:.2f}x"
 ]
 }
 
 st.table(breakdown_data)
 
 # Action Items
 st.markdown("---")
 st.markdown("#### **Recommended Actions**")
 
 if prediction > 3000:
 st.success("""
 **High Revenue Product**
 - Ensure adequate inventory levels
 - Consider premium shelf placement
 - Monitor stock levels closely
 - Replicate this combination in similar stores
 """)
 elif prediction > 1500:
 st.info("""
 **Moderate Performance**
 - Standard inventory planning
 - Regular performance monitoring
 - Consider promotional activities
 """)
 else:
 st.warning("""
 **Performance Review Needed**
 - Analyze pricing strategy
 - Review product placement
 - Consider alternative suppliers
 - Monitor competitor pricing
 """)
 
 # Export Options
 st.markdown("---")
 prediction_summary = {
 "prediction_id": f"{validated_data['product_id']}_{validated_data['store_type']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
 "timestamp": datetime.datetime.now().isoformat(),
 "input_data": input_data,
 "prediction": prediction,
 "derived_features": derived_features,
 "business_insight": insights
 }
 
 col_export1, col_export2 = st.columns(2)
 with col_export1:
 st.download_button(
 "Download Prediction (JSON)",
 data=json.dumps(prediction_summary, indent=2),
 file_name=f"superkart_prediction_{validated_data['product_id']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
 mime="application/json"
 )
 
 with col_export2:
 st.info(" **Tip**: Save predictions for trend analysis and model validation")
 
 else:
 st.error(f"**Prediction Failed**: Server returned an error")
 if response.text:
 with st.expander(" Error Details"):
 st.code(response.text)
 
 except requests.exceptions.Timeout:
 st.error(" **Request Timed Out** - Service may be busy. Please try again.")
 except requests.exceptions.ConnectionError:
 st.error(" **Connection Error** - Unable to reach prediction service.")
 except Exception as e:
 st.error(f" **Unexpected Error**: Something went wrong. Please try again.")

