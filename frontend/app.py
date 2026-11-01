
import streamlit as st
import pandas as pd

# Import from organized modules
from config.settings import PAGE_CONFIG, PRODUCT_OPTIONS
from styles.css import get_custom_css
from utils.backend import start_health_monitoring
from components.single_item import render_single_item_prediction
from components.batch_prediction import render_batch_prediction
from components.compare_items import render_compare_items

# Page Configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize backend monitoring
start_health_monitoring()

# Header Section
st.markdown("""
<div class="main-header">
    <h1>🛒 SuperKart Sales Predictor</h1>
    <h3>AI-Powered Retail Revenue Forecasting</h3>
    <p>Predict quarterly sales for any product-store combination</p>
</div>
""", unsafe_allow_html=True)

# Initialize uploaded_file variable
uploaded_file = None

#Chain Reaction Setup
prediction_options = ["Single Item", "Batch Prediction", "Compare Items"]

# Initialize session state for prediction mode if not exists
if 'prediction_mode' not in st.session_state:
    st.session_state.prediction_mode = "Single Item"

# Enhanced Sidebar with Chain Reaction
with st.sidebar:
    st.markdown("## **Prediction Options**")
    
    #Radio button fully bound to session state
    try:
        current_index = prediction_options.index(st.session_state.prediction_mode)
    except ValueError:
        current_index = 0
        st.session_state.prediction_mode = prediction_options[0]
    
    #Radio button that responds to session state changes
    prediction_mode = st.radio(
        "Choose Prediction Mode:",
        prediction_options,
        index=current_index,
        key="prediction_mode_radio"
    )
    
    #Bidirectional synchronization
    if prediction_mode != st.session_state.prediction_mode:
        st.session_state.prediction_mode = prediction_mode
        # Clear batch comparison data when switching modes manually
        if 'batch_comparison_data' in st.session_state:
            del st.session_state.batch_comparison_data
        st.rerun()
    
    # Show different content based on current mode
    current_mode = st.session_state.prediction_mode
    
    if current_mode == "Single Item":
        st.info("Fill the form and click predict for single item forecasting")
    
    elif current_mode == "Batch Prediction":
        st.markdown("### 📁 **Multi-Format Batch Upload**")
        st.info("**Supported:** CSV, JSON, TXT, PDF")
        
        uploaded_file = st.file_uploader(
            "Upload your data file",
            type=['csv', 'json', 'txt', 'pdf']
        )
    
    elif current_mode == "Compare Items":
        st.markdown("### ⚖️ **Item Comparison**")
        st.info("Compare predictions with Sales-to-MRP ratio analysis")
        
        # Debug info for Compare Items
        if 'batch_comparison_data' in st.session_state:
            batch_count = len(st.session_state.batch_comparison_data) if st.session_state.batch_comparison_data is not None else 0
            if batch_count > 0:
                st.success(f"{batch_count} items ready for comparison")
            else:
                st.info("No batch data available")
        
        # Add option to switch back to batch prediction
        if st.button("🔙 Back to Batch Prediction", key="back_to_batch"):
            st.session_state.prediction_mode = "Batch Prediction"
            st.rerun()
    
    # Enhanced Data Management Section with View Data
    st.markdown("---")
    st.markdown("## **Saved Data**")
    
    if 'saved_predictions' in st.session_state and st.session_state.saved_predictions:
        total_saved = len(st.session_state.saved_predictions)
        st.success(f"{total_saved} predictions saved")
        
        # Show breakdown
        saved_df = pd.DataFrame(st.session_state.saved_predictions)
        single_count = len(saved_df[saved_df['Prediction_Source'] == 'Single Item'])
        batch_count = len(saved_df[saved_df['Prediction_Source'] == 'Batch Upload'])
        
        st.write(f"🔍 Single: {single_count}")
        st.write(f"📁 Batch: {batch_count}")
        
        # View Data Expander
        with st.expander("👁️ **View Saved Data**", expanded=False):
            # Display options
            view_option = st.selectbox(
                "Choose view:",
                ["All Predictions", "Single Item Only", "Batch Upload Only"],
                key="data_view_option"
            )
            
            # Filter data based on selection
            if view_option == "Single Item Only":
                filtered_df = saved_df[saved_df['Prediction_Source'] == 'Single Item']
            elif view_option == "Batch Upload Only":
                filtered_df = saved_df[saved_df['Prediction_Source'] == 'Batch Upload']
            else:
                filtered_df = saved_df
            
            if not filtered_df.empty:
                # Select columns to display
                display_columns = ['Product_Id', 'Product_Type', 'Product_MRP', 'Predicted_Sales', 
                                 'Store_Type', 'Prediction_Source', 'Timestamp']
                available_columns = [col for col in display_columns if col in filtered_df.columns]
                
                # Sort by timestamp (most recent first)
                if 'Timestamp' in filtered_df.columns:
                    filtered_df = filtered_df.sort_values('Timestamp', ascending=False)
                
                st.dataframe(
                    filtered_df[available_columns], 
                    use_container_width=True,
                    height=300
                )
                
                # Show summary stats
                if len(filtered_df) > 0:
                    avg_sales = filtered_df['Predicted_Sales'].mean()
                    total_sales = filtered_df['Predicted_Sales'].sum()
                    max_sales = filtered_df['Predicted_Sales'].max()
                    min_sales = filtered_df['Predicted_Sales'].min()
                    
                    st.markdown("**📈 Summary Statistics:**")
                    stats_col1, stats_col2 = st.columns(2)
                    with stats_col1:
                        st.metric("Average Sales", f"₹{avg_sales:,.0f}")
                        st.metric("Total Revenue", f"₹{total_sales:,.0f}")
                    with stats_col2:
                        st.metric("Highest", f"₹{max_sales:,.0f}")
                        st.metric("Lowest", f"₹{min_sales:,.0f}")
                
                # Export filtered data
                st.markdown("**Export Options:**")
                timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
                
                export_col1, export_col2 = st.columns(2)
                with export_col1:
                    st.download_button(
                        "Download CSV",
                        data=filtered_df.to_csv(index=False),
                        file_name=f"saved_predictions_{view_option.lower().replace(' ', '_')}_{timestamp}.csv",
                        mime="text/csv",
                        key="export_csv_sidebar"
                    )
                
                with export_col2:
                    st.download_button(
                        "Download JSON", 
                        data=filtered_df.to_json(orient='records', indent=2),
                        file_name=f"saved_predictions_{view_option.lower().replace(' ', '_')}_{timestamp}.json",
                        mime="application/json",
                        key="export_json_sidebar"
                    )
            else:
                st.info(f"No {view_option.lower()} found.")
        
        # Clear data button
        if st.button("🗑️ Clear All Data", key="sidebar_clear"):
            if st.button("⚠️ Confirm Clear", key="confirm_clear"):
                st.session_state.saved_predictions = []
                st.success("All predictions cleared!")
                st.rerun()
    else:
        st.info("No saved predictions yet")
        
        # Empty state expander
        with st.expander("👁️ **View Saved Data**", expanded=False):
            st.info("""
            **No predictions saved yet**
            
            **To save predictions:**
            - Use Single Item prediction
            - Run Batch Prediction
            - Data will appear here automatically
            """)
    
    st.markdown("---")
    st.markdown("## **Quick Guide**")
    if current_mode == "Single Item":
        st.markdown("""
        **Steps:**
        1. Fill product and store details
        2. Click 'Predict Quarterly Sales'
        3. View detailed analysis
        """)
    elif current_mode == "Batch Prediction":
        st.markdown("""
        **Steps:**
        1. Upload file in anyone of the mentioned formats
        2. Run predictions
        3. View detailed analysis
        """)
    else:
        st.markdown("""
        **Steps:**
        1. Run batch predictions first or upload a file with predictions
        2. Click 'Compare Items' button
        3. Select items to analyze
        4. View efficiency insights
        """)
    
    st.markdown("---")
    st.markdown("## ℹ️ **About**")
    st.markdown("""
    **SuperKart Sales Predictor** uses advanced machine learning to forecast quarterly revenue.
    
    **Powered by:**
    - 🤖 Scikit-learn ML Pipeline
    - 🚀 Streamlit Frontend  
    - 🐍 Flask Backend API
    - ☁️ Hugging Face Spaces
    """)

# Main Content Router using session state value
current_mode = st.session_state.prediction_mode

if current_mode == "Single Item":
    render_single_item_prediction()
elif current_mode == "Batch Prediction":
    render_batch_prediction(uploaded_file)
elif current_mode == "Compare Items":
    render_compare_items()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>SuperKart Sales Predictor</strong></p>
    <p>Built with using Streamlit • Powered by Hugging Face Spaces</p>
    <p>🔒 Secure • 🚀 Fast • 📊 Accurate</p>
</div>
""", unsafe_allow_html=True)
