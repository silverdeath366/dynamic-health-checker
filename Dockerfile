# Dockerfile

# Base image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY monitor.py .

# Set entrypoint
ENTRYPOINT ["python", "monitor.py"]
