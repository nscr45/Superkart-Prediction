import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from utils.file_processor import process_uploaded_file
from utils.helpers import format_currency

def render_compare_items():
    """Render the compare items interface"""
    st.markdown("## ⚖️ **Item Comparison Analysis**")
    
    # Debug session state
    debug_session_state()
    
    # FIXED: Simplified check - just look for batch_comparison_data
    if ('batch_comparison_data' in st.session_state and 
        st.session_state.batch_comparison_data is not None and 
        not st.session_state.batch_comparison_data.empty):
        
        batch_data = st.session_state.batch_comparison_data
        st.success(f"✅ **Ready to compare {len(batch_data)} predictions**")
        
        # Show comparison interface
        render_batch_comparison(batch_data)
        
    else:
        # FIXED: Also check saved_predictions as fallback
        if 'saved_predictions' in st.session_state and len(st.session_state.saved_predictions) >= 2:
            st.info("📊 **Using your saved predictions for comparison**")
            
            # Convert saved predictions to DataFrame
            saved_df = pd.DataFrame(st.session_state.saved_predictions)
            st.session_state.batch_comparison_data = saved_df
            render_batch_comparison(saved_df)
        else:
            # No data available
            st.info("👆 **No prediction data available.** Please run batch predictions first, or upload a file.")
            render_file_upload_comparison()

def debug_session_state():
    """Enhanced debug session state contents"""
    if st.checkbox("🔍 **Debug Mode**", key="debug_compare_enhanced"):
        st.write("**🔧 Session State Debug:**")
        
        keys_to_check = ['batch_comparison_data', 'saved_predictions', 'prediction_mode']
        
        for key in keys_to_check:
            if key in st.session_state:
                value = st.session_state[key]
                if key == 'batch_comparison_data':
                    if value is not None:
                        st.write(f"**{key}**: DataFrame with {len(value)} rows")
                    else:
                        st.write(f"**{key}**: None")
                elif key == 'saved_predictions':
                    st.write(f"**{key}**: {len(value)} items")
                else:
                    st.write(f"**{key}**: {value}")
            else:
                st.write(f"**{key}**: Not found")

def render_batch_comparison(batch_data):
    """Render comparison interface for batch data"""
    
    # Item selection for comparison
    st.markdown("### 🔍 **Select Items to Compare**")
    
    # Create product options
    try:
        product_options = []
        for _, row in batch_data.iterrows():
            product_type = row.get('Product_Type', 'N/A')
            predicted_sales = row.get('Predicted_Sales', 0)
            product_options.append(f"{row['Product_Id']} - {product_type} (₹{predicted_sales:,.2f})")
    except Exception as e:
        st.error(f"Error creating product options: {str(e)}")
        return
    
    selected_items = st.multiselect(
        "**Choose products to compare** (select 2-10 items):",
        options=product_options,
        default=product_options[:min(3, len(product_options))]
    )
    
    if len(selected_items) >= 2:
        # Extract Product_IDs from selected items
        selected_product_ids = [item.split(' - ')[0] for item in selected_items]
        comparison_df = batch_data[batch_data['Product_Id'].isin(selected_product_ids)].copy()
        
        # Calculate Sales-to-MRP Ratio
        try:
            comparison_df['Sales_to_MRP_Ratio'] = comparison_df['Predicted_Sales'] / comparison_df['Product_MRP']
            comparison_df_sorted = comparison_df.sort_values(by='Sales_to_MRP_Ratio', ascending=False)
            
            # Display comparison results
            display_comparison_results(comparison_df_sorted)
            
        except Exception as e:
            st.error(f"Error calculating ratios: {str(e)}")
            
    elif len(selected_items) == 1:
        st.warning("⚠️ Please select at least 2 items for comparison")
    else:
        st.info("👆 Select items from the dropdown above to compare")

def display_comparison_results(comparison_df_sorted):
    """Display the comparison results with visualizations"""
    # Comparison table with ratio
    st.markdown("### **Comparison Results (Sorted by Efficiency)**")
    
    # Format display table
    comparison_display = comparison_df_sorted[['Product_Id', 'Product_Type', 'Product_MRP', 
                                             'Store_Type', 'Predicted_Sales', 'Sales_to_MRP_Ratio']].copy()
    
    comparison_display['Product_MRP'] = comparison_display['Product_MRP'].apply(lambda x: f"₹{x:.2f}")
    comparison_display['Predicted_Sales'] = comparison_display['Predicted_Sales'].apply(lambda x: f"₹{x:,.2f}")
    comparison_display['Sales_to_MRP_Ratio'] = comparison_display['Sales_to_MRP_Ratio'].apply(lambda x: f"{x:.2f}x")
    
    comparison_display.columns = ['Product ID', 'Type', 'MRP', 'Store Type', 'Predicted Sales', 'Sales/MRP Ratio']
    
    st.dataframe(comparison_display, use_container_width=True)
    
    # Dual visualization
    st.markdown("### 📊 **Comparison Charts**")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.markdown("#### 💰 **Sales Comparison**")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        
        bars1 = ax1.bar(comparison_df_sorted['Product_Id'], comparison_df_sorted['Predicted_Sales'], 
                       color='#667eea', alpha=0.8)
        ax1.set_xlabel('Product ID')
        ax1.set_ylabel('Predicted Sales (₹)')
        ax1.set_title('Sales Prediction Comparison')
        ax1.tick_params(axis='x', rotation=45)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                   f'₹{height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        st.pyplot(fig1)
    
    with viz_col2:
        st.markdown("#### 🎯 **Efficiency Comparison**")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        bars2 = ax2.bar(comparison_df_sorted['Product_Id'], comparison_df_sorted['Sales_to_MRP_Ratio'], 
                       color='#56ab2f', alpha=0.8)
        ax2.set_xlabel('Product ID')
        ax2.set_ylabel('Sales/MRP Ratio')
        ax2.set_title('Efficiency Comparison')
        ax2.tick_params(axis='x', rotation=45)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}x', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        st.pyplot(fig2)
    
    # Performance insights
    st.markdown("### 💡 **Performance Analysis**")
    
    best_performer = comparison_df_sorted.iloc[0]
    worst_performer = comparison_df_sorted.iloc[-1]
    best_sales = comparison_df_sorted.loc[comparison_df_sorted['Predicted_Sales'].idxmax()]
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.success(f"""
        **🏆 Most Efficient**
        - **Product**: {best_performer['Product_Id']}
        - **Efficiency**: {best_performer['Sales_to_MRP_Ratio']:.2f}x
        - **Sales**: ₹{best_performer['Predicted_Sales']:,.2f}
        - **MRP**: ₹{best_performer['Product_MRP']:.2f}
        """)
    
    with insight_col2:
        st.info(f"""
        **💰 Highest Sales**
        - **Product**: {best_sales['Product_Id']}
        - **Sales**: ₹{best_sales['Predicted_Sales']:,.2f}
        - **Efficiency**: {best_sales['Sales_to_MRP_Ratio']:.2f}x
        - **MRP**: ₹{best_sales['Product_MRP']:.2f}
        """)
    
    with insight_col3:
        st.warning(f"""
        **📉 Least Efficient**
        - **Product**: {worst_performer['Product_Id']}
        - **Efficiency**: {worst_performer['Sales_to_MRP_Ratio']:.2f}x
        - **Sales**: ₹{worst_performer['Predicted_Sales']:,.2f}
        - **MRP**: ₹{worst_performer['Product_MRP']:.2f}
        """)
    
    # Performance metrics
    st.markdown("#### **Key Metrics**")
    
    average_ratio = comparison_df_sorted['Sales_to_MRP_Ratio'].mean()
    performance_gap = best_performer['Sales_to_MRP_Ratio'] - worst_performer['Sales_to_MRP_Ratio']
    
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        st.info(f"""
        **📈 Efficiency Stats**
        - **Best Ratio**: {best_performer['Sales_to_MRP_Ratio']:.2f}x
        - **Worst Ratio**: {worst_performer['Sales_to_MRP_Ratio']:.2f}x
        - **Average Ratio**: {average_ratio:.2f}x
        - **Efficiency Gap**: {performance_gap:.2f}x
        """)
    
    with metric_col2:
        high_efficiency = len(comparison_df_sorted[comparison_df_sorted['Sales_to_MRP_Ratio'] > average_ratio * 1.2])
        low_efficiency = len(comparison_df_sorted[comparison_df_sorted['Sales_to_MRP_Ratio'] < average_ratio * 0.8])
        
        st.info(f"""
        **🎯 Performance Categories**
        - **High Efficiency**: {high_efficiency} items
        - **Average Efficiency**: {len(comparison_df_sorted) - high_efficiency - low_efficiency} items
        - **Low Efficiency**: {low_efficiency} items
        - **Total Compared**: {len(comparison_df_sorted)} items
        """)
    
    # Export option
    st.markdown("###**Export Results**")
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        st.download_button(
            "Download Comparison (CSV)",
            data=comparison_df_sorted.to_csv(index=False),
            file_name=f"comparison_analysis_{timestamp}.csv",
            mime="text/csv"
        )
    
    with col_export2:
        if st.button("🗑️ Clear Comparison Data"):
            if 'batch_comparison_data' in st.session_state:
                del st.session_state.batch_comparison_data
            st.rerun()

def render_file_upload_comparison():
    """Render file upload comparison interface"""
    st.markdown("### 📁 **Upload Comparison File**")
    compare_file = st.file_uploader(
        "Upload predictions file for comparison",
        type=['csv', 'json', 'txt', 'pdf'],
        key="compare_uploader"
    )
    
    if compare_file is not None:
        try:
            comparison_df, status_message = process_uploaded_file(compare_file)
            
            if comparison_df is not None:
                if 'Predicted_Sales' not in comparison_df.columns:
                    st.error("File must contain 'Predicted_Sales' column.")
                else:
                    st.success(f"Loaded {len(comparison_df)} items for comparison.")
                    render_batch_comparison(comparison_df)
            else:
                st.error(f"**File Processing Failed:** {status_message}")
                        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        st.markdown("""
        ### 📋 **Instructions**
        1. **Option 1**: Run batch predictions first, then click "Compare Items from This Batch"
        2. **Option 2**: Upload a CSV/JSON file with prediction results
        """)

