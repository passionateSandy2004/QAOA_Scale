#!/bin/bash

# Railway startup script for QAOA Portfolio Optimizer
echo "Starting QAOA Portfolio Optimizer..."
echo "PORT: $PORT"
echo "Environment: $FLASK_ENV"

# Use Railway's PORT or default to 8000
export PORT=${PORT:-8000}

echo "Binding to port: $PORT"

# Start Gunicorn with Railway-specific configuration
exec gunicorn \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --worker-class sync \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    "api:create_app()"