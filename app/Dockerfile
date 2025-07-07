# Use slim base image for Python 3.12.3
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required for transformers
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app ./app

# Expose FastAPI port
EXPOSE 8002

# Run the FastAPI app with preloaded model
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
