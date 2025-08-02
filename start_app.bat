@echo off
echo ====================================
echo    Data Analyzer Pro - Local Setup
echo ====================================
echo.

REM Navigate to the project directory
cd /d "c:\Users\HP\clone git reprository"

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo.
echo Checking if virtual environment exists...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Setting environment variables...
set FLASK_ENV=development
set FLASK_DEBUG=1

echo.
echo ====================================
echo    Starting Data Analyzer Pro
echo ====================================
echo.
echo Your app will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python app.py
