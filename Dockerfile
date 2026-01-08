# VERITAS Command Center - Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_upgraded.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_upgraded.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm || true

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/processed data/mock reports

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command (can be overridden)
CMD ["python", "api/main.py"]
