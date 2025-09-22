# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency files first
COPY requirements.txt ./

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (including Streamlit)
RUN pip install --no-cache-dir -r requirements.txt streamlit

# Copy the rest of your application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Command to run Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
