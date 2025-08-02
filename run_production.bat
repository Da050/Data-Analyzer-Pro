@echo off
REM Production test script for Windows

echo Setting up production environment...

REM Set environment variables
set FLASK_ENV=production
set SECRET_KEY=dev-secret-key-change-in-production

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt
pip install waitress

echo.
echo Starting application with Waitress (Windows-compatible WSGI server)...
echo Access the app at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

waitress-serve --host=0.0.0.0 --port=8000 wsgi:app
