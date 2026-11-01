
import pandas as pd
import json
import io
import pdfplumber
from config.settings import REQUIRED_COLUMNS

def process_uploaded_file(uploaded_file):
    """Process uploaded file based on its extension"""
    if uploaded_file is None:
        return None, "No file uploaded"
    
    filename = uploaded_file.name.lower()
    file_extension = filename.split('.')[-1]
    
    try:
        if file_extension == 'csv':
            return process_csv_file(uploaded_file)
        elif file_extension == 'json':
            return process_json_file(uploaded_file)
        elif file_extension == 'txt':
            return process_txt_file(uploaded_file)
        elif file_extension == 'pdf':
            return process_pdf_file(uploaded_file)
        else:
            return None, f"Unsupported file format: .{file_extension}"
    except Exception as e:
        return None, f"Error processing {file_extension.upper()} file: {str(e)}"

def process_csv_file(uploaded_file):
    """Process CSV file"""
    try:
        df = pd.read_csv(uploaded_file)
        return df, f"CSV file processed successfully ({len(df)} rows)"
    except Exception as e:
        return None, f"Error reading CSV: {str(e)}"

def process_json_file(uploaded_file):
    """Process JSON file - supports both array format and nested objects"""
    try:
        uploaded_file.seek(0)  # Reset file pointer
        df = pd.read_json(uploaded_file)
        return df, f"JSON file processed successfully ({len(df)} rows)"
    except:
        try:
            uploaded_file.seek(0)
            content = uploaded_file.read().decode('utf-8')
            data = json.loads(content)
            
            if isinstance(data, list):
                df = pd.json_normalize(data)
            elif isinstance(data, dict):
                df = pd.json_normalize([data])
            else:
                return None, "JSON format not supported. Expected array of objects or single object."
            
            return df, f"JSON file processed successfully ({len(df)} rows)"
        except Exception as e:
            return None, f"Error parsing JSON: {str(e)}"

def process_txt_file(uploaded_file):
    """Process TXT file - attempts to parse as CSV or JSON"""
    try:
        content = uploaded_file.read().decode('utf-8')
        
        # Try CSV format first
        try:
            df = pd.read_csv(io.StringIO(content))
            return df, f"TXT file parsed as CSV ({len(df)} rows)"
        except:
            pass
        
        # Try JSON format
        try:
            data = json.loads(content)
            if isinstance(data, list):
                df = pd.json_normalize(data)
            else:
                df = pd.json_normalize([data])
            return df, f"TXT file parsed as JSON ({len(df)} rows)"
        except:
            pass
        
        # Try tab-separated values
        try:
            df = pd.read_csv(io.StringIO(content), sep='	')
            return df, f"TXT file parsed as TSV ({len(df)} rows)"
        except:
            pass
        
        return None, "Could not parse TXT file as CSV, JSON, or TSV format"
        
    except Exception as e:
        return None, f"Error reading TXT file: {str(e)}"

def process_pdf_file(uploaded_file):
    """Process PDF file - extract tables or structured text"""
    try:
        all_tables = []
        text_content = ""
        
        with pdfplumber.open(uploaded_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Try to extract tables first
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        if len(table) > 1:  # Ensure there's a header and data
                            df_table = pd.DataFrame(table[1:], columns=table[0])
                            all_tables.append(df_table)
                
                # Extract text content
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
        
        # If tables were found, use the first one
        if all_tables:
            df = all_tables[0]
            return df, f"PDF table extracted successfully ({len(df)} rows from {len(all_tables)} tables)"
        
        # If no tables, try to parse text as CSV or JSON
        if text_content.strip():
            try:
                df = pd.read_csv(io.StringIO(text_content))
                return df, f"PDF text parsed as CSV ({len(df)} rows)"
            except:
                pass
            
            try:
                data = json.loads(text_content)
                if isinstance(data, list):
                    df = pd.json_normalize(data)
                else:
                    df = pd.json_normalize([data])
                return df, f"PDF text parsed as JSON ({len(df)} rows)"
            except:
                pass
        
        return None, "No structured data found in PDF. Please ensure the PDF contains tables or structured text."
        
    except Exception as e:
        return None, f"Error processing PDF: {str(e)}"

def validate_prediction_data(df):
    """Validate that DataFrame has required columns for prediction"""
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, "All required columns present"

def run_batch_predictions(df, backend_url):
    """Run batch predictions on uploaded DataFrame"""
    import streamlit as st
    import requests
    
    predictions = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, (_, row) in enumerate(df.iterrows()):
        status_text.text(f'Processing item {i+1} of {len(df)}: {row["Product_Id"]}')
        progress_bar.progress((i + 1) / len(df))
        
        try:
            input_data = row.to_dict()
            response = requests.post(f"{backend_url}/predict", json=input_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                predictions.append({
                    'Product_Id': row['Product_Id'],
                    'Predicted_Sales': result.get('prediction'),
                    'Status': 'Success',
                    'Store_Age': result.get('derived_features', {}).get('store_age'),
                    'Category_Code': result.get('derived_features', {}).get('product_category_code')
                })
            else:
                predictions.append({
                    'Product_Id': row['Product_Id'],
                    'Predicted_Sales': None,
                    'Status': f'Error: {response.status_code}',
                    'Store_Age': None,
                    'Category_Code': None
                })
                
        except Exception as e:
            predictions.append({
                'Product_Id': row['Product_Id'],
                'Predicted_Sales': None,
                'Status': f'Error: {str(e)}',
                'Store_Age': None,
                'Category_Code': None
            })
    
    progress_bar.empty()
    status_text.empty()
    
    return pd.DataFrame(predictions)
