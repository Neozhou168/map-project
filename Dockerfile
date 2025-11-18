# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Create directories for uploads and outputs
RUN mkdir -p downloads

# Expose port (Railway will set PORT env variable)
EXPOSE 5000

# Run the application using startup script
CMD ["/bin/sh", "./start.sh"]