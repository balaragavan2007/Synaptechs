# Use a pre-built image that already has many data science libraries
FROM anask/streamlit-plus:1.0

# Set the working directory
WORKDIR /app

# Copy your dependency files
COPY requirements.txt apt-get.txt ./

# Install system dependencies (Tesseract)
RUN apt-get update && xargs -a apt-get.txt apt-get install -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install your specific Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set the healthcheck to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit application
CMD ["streamlit", "run", "app.py"]