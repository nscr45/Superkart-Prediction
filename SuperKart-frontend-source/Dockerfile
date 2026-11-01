FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip &&     pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . ./

# Expose Streamlit default port
EXPOSE 8501

# Health check for Hugging Face Spaces
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
