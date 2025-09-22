# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all dependency files first
COPY requirements.txt apt-get.txt ./

# Combine all installation steps into one layer to improve caching and speed
RUN apt-get update && \
    xargs -a apt-get.txt apt-get install -y --no-install-recommends && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of your application code
COPY . .

# Expose the correct port
EXPOSE 8501

# Command to run your Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false"]