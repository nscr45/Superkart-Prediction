import streamlit as st
import datetime
import pandas as pd
from utils.file_processor import process_uploaded_file, validate_prediction_data, run_batch_predictions
from utils.helpers import format_currency
from utils.backend import check_backend_health
from config.settings import BACKEND_URL

def render_batch_prediction(uploaded_file):
    """Render the batch prediction interface"""
    st.markdown("##  **Multi-Format Batch Processing**")
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.1f} KB",
            "File type": uploaded_file.type or "Unknown"
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File", file_details["Filename"])
        with col2:
            st.metric("Size", file_details["File size"])
        with col3:
            st.metric("Type", file_details["File type"])
        
        # Process the uploaded file
        with st.spinner(f" Processing {uploaded_file.name}..."):
            batch_df, status_message = process_uploaded_file(uploaded_file)
        
        if batch_df is not None:
            st.success(status_message)
            
            # Validate required columns
            is_valid, validation_message = validate_prediction_data(batch_df)
            
            if not is_valid:
                st.error(f"**Data Validation Failed:** {validation_message}")
                st.info("Please ensure your file contains all required columns for predictions.")
            else:
                st.success(f"**Data validated successfully!** {validation_message}")
                
                # Show data preview
                st.markdown("###**Data Preview**")
                st.dataframe(batch_df.head(10), use_container_width=True)
                
                if len(batch_df) > 10:
                    st.info(f"Showing first 10 of {len(batch_df)} total rows")
                
                # Run batch predictions
                if st.button("**Run Batch Predictions**", type="primary"):
                    backend_healthy = check_backend_health()
                    
                    if not backend_healthy:
                        st.error("**Backend service unavailable.** Please try again later.")
                    else:
                        st.markdown("###  **Processing Batch Predictions...**")
                        
                        # Run predictions with progress tracking
                        results_df = run_batch_predictions(batch_df, BACKEND_URL)
                        
                        # Display comprehensive results
                        display_batch_results(batch_df, results_df)
        else:
            st.error(f"**File Processing Failed:** {status_message}")
            st.info("Please check your file format and try again.")
    else:
        st.info(" **Please upload a file to begin batch prediction**")
        
        # Show supported formats
        st.markdown("###**Supported File Formats**")
        
        format_col1, format_col2 = st.columns(2)
        
        with format_col1:
            st.markdown("""
            ** Text-Based Formats:**
            - **CSV**: Comma-separated values (most common)
            - **JSON**: JavaScript Object Notation
            - **TXT**: Plain text (CSV, JSON, or TSV)
            """)
        
        with format_col2:
            st.markdown("""
            ** Document Formats:**
            - **PDF**: Portable Document Format (with tables)
            
            ** Upload Requirements:**
            - Maximum file size: 200MB
            - Must contain all required columns
            """)

def display_batch_results(original_df, results_df):
    """Display comprehensive batch prediction results"""
    st.markdown("###**Batch Prediction Results**")
    
    # Success metrics
    successful_predictions = len(results_df[results_df['Status'] == 'Success'])
    total_items = len(results_df)
    success_rate = (successful_predictions / total_items) * 100 if total_items > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Items", total_items)
    with col2:
        st.metric("Successful", successful_predictions)
    with col3:
        st.metric("Failed", total_items - successful_predictions)
    with col4:
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    # Results table
    st.dataframe(results_df, use_container_width=True)
    
    # Summary statistics
    successful_results = results_df[results_df['Status'] == 'Success']
    if len(successful_results) > 0:
        st.markdown("###**Summary Statistics**")
        
        sales_data = successful_results['Predicted_Sales'].dropna()
        if len(sales_data) > 0:
            avg_sales = sales_data.mean()
            max_sales = sales_data.max()
            min_sales = sales_data.min()
            total_revenue = sales_data.sum()
            
            summary_col1, summary_col2 = st.columns(2)
            with summary_col1:
                st.metric("Average Sales", format_currency(avg_sales))
                st.metric("Maximum Sales", format_currency(max_sales))
            with summary_col2:
                st.metric("Minimum Sales", format_currency(min_sales))
                st.metric("Total Revenue", format_currency(total_revenue))
        
        # Save batch predictions to session state
        if 'saved_predictions' not in st.session_state:
            st.session_state.saved_predictions = []
        
        # Merge original data with results for complete records
        complete_results = original_df.merge(
            successful_results[['Product_Id', 'Predicted_Sales']], 
            on='Product_Id', 
            how='inner'
        )
        
        if not complete_results.empty:
            new_predictions = []
            for _, row in complete_results.iterrows():
                prediction_record = {
                    'Product_Id': row['Product_Id'],
                    'Product_Weight': row['Product_Weight'],
                    'Product_Sugar_Content': row['Product_Sugar_Content'],
                    'Product_Allocated_Area': row['Product_Allocated_Area'],
                    'Product_Type': row['Product_Type'],
                    'Product_MRP': row['Product_MRP'],
                    'Store_Establishment_Year': row['Store_Establishment_Year'],
                    'Store_Size': row['Store_Size'],
                    'Store_Location_City_Type': row['Store_Location_City_Type'],
                    'Store_Type': row['Store_Type'],
                    'Predicted_Sales': row['Predicted_Sales'],
                    'Timestamp': datetime.datetime.now().isoformat(),
                    'Prediction_Source': 'Batch Upload'
                }
                new_predictions.append(prediction_record)
            
            # Remove existing predictions with same Product_Id + Store_Type combinations
            existing_predictions = []
            for existing in st.session_state.saved_predictions:
                should_keep = True
                for new_pred in new_predictions:
                    if (existing['Product_Id'] == new_pred['Product_Id'] and 
                        existing['Store_Type'] == new_pred['Store_Type']):
                        should_keep = False
                        break
                if should_keep:
                    existing_predictions.append(existing)
            
            # Add new predictions
            st.session_state.saved_predictions = existing_predictions + new_predictions
            st.success(f" {len(new_predictions)} predictions saved to comparison database")
    
    # Download results
    st.markdown("###**Download Results**")
    final_results = original_df.merge(
        results_df[['Product_Id', 'Predicted_Sales', 'Status']], 
        on='Product_Id', 
        how='left'
    )
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    st.download_button(
        "Download Complete Results (CSV)",
        data=final_results.to_csv(index=False),
        file_name=f"superkart_batch_predictions_{timestamp}.csv",
        mime="text/csv"
    )
    
    #Compare Items Button
    if 'saved_predictions' in st.session_state and len(st.session_state.saved_predictions) >= 2:
        st.markdown("---")
        st.markdown("###  **Next Steps**")
        
        col_compare, col_info = st.columns([1, 2])
        
        with col_compare:
            #This button triggers sidebar radio change
            if st.button(" **Compare Items from This Batch**", type="secondary", use_container_width=True, key="batch_compare_button"):
                # Prepare comparison data from saved predictions
                saved_df = pd.DataFrame(st.session_state.saved_predictions)
                
                # Set session state for comparison
                st.session_state.batch_comparison_data = saved_df
                st.session_state.show_batch_comparison = True
                
                # Queue navigation for app.py to apply before the radio widget
                # is created on the next rerun.
                st.session_state.pending_workspace_mode = "Compare Items"
                st.rerun()
        
        with col_info:
            saved_count = len(st.session_state.saved_predictions)
            st.info(f" **{saved_count} predictions** available for comparison. Click the button to analyze efficiency with Sales-to-MRP ratio analysis.")
    
    elif 'saved_predictions' in st.session_state and len(st.session_state.saved_predictions) == 1:
        st.info("Only 1 prediction saved - need at least 2 items for comparison.")
    else:
        st.warning(" No predictions saved for comparison.")
