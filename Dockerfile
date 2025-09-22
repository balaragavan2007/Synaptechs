FROM python:3.11-slim

# System deps with cleaned cache in same layer
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install deps efficiently with limited workers and pip config
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --compile --no-deps -r requirements.txt \
    && pip install --no-cache-dir -r requirements.txt --no-deps \
    && rm -rf ~/.cache/pip/*

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]