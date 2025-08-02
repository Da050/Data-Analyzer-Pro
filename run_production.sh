#!/bin/bash
# Production test script for Unix/Linux/Mac

echo "Setting up production environment..."

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=dev-secret-key-change-in-production

echo ""
echo "Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting application with Gunicorn..."
echo "Access the app at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

gunicorn --bind 0.0.0.0:8000 wsgi:app
