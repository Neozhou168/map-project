#!/bin/sh
# Startup script for Railway deployment

# Get PORT from environment, default to 5000 if not set
PORT=${PORT:-5000}

echo "Starting gunicorn on port $PORT"

# Start gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app