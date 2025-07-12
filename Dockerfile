# Use official Python 3.12 base image
FROM python:3.12.3-slim

# Avoid writing .pyc files and enable instant stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install basic build dependencies (for torch/transformers/peft)
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Pre-download the model during build (optional but recommended for production)
# This makes startup faster but increases image size
ENV TRANSFORMERS_CACHE=/app/model_cache
RUN mkdir -p /app/model_cache

# Download the model during build
RUN python -c "from transformers import pipeline; pipeline('sentiment-analysis', model='cardiffnlp/twitter-roberta-base-sentiment', cache_dir='/app/model_cache')"


# Simple health check for Docker/ECR - no model warmup required
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8095/health || exit 1

# Expose the service port
EXPOSE 8095

# Run the FastAPI app via uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8095", "--workers", "1"]
