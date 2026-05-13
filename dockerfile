# Use a lightweight Python runtime image.
FROM python:3.14-slim

# Prevent Python from writing .pyc files and buffer logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container.
WORKDIR /app

# Copy dependency file first for better Docker layer caching.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and project files.
COPY src/ ./src/

# Run the ETL pipeline.
CMD ["python", "src/pipeline.py"]