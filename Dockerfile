# Dockerfile

# Use an official Python image as a starting point
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency files into the container
COPY requirements.txt apt-get.txt ./

# Install system dependencies from apt-get.txt
RUN apt-get update && xargs -a apt-get.txt apt-get install -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Python libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . .

# Command to run your Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port", "80", "--server.enableCORS", "false"]