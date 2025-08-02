@echo off
echo ====================================
echo    Data Analyzer Pro - Auto Start
echo ====================================
echo.

REM Navigate to the project directory
cd /d "c:\Users\HP\clone git reprository"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Flask...
    pip install flask
)

python -c "import pandas, numpy, matplotlib, seaborn, sklearn" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

echo ✅ Dependencies ready
echo.

echo Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "static\plots" mkdir static\plots

echo.
echo ====================================
echo    🚀 STARTING DATA ANALYZER PRO
echo ====================================
echo.
echo 📊 Your app will be available at: http://localhost:5000
echo 🌐 Browser will open automatically in 3 seconds...
echo 🛑 Press Ctrl+C to stop the server
echo ====================================
echo.

REM Start the Flask app in background
start /B python app.py

REM Wait 3 seconds for the server to start
timeout /t 3 /nobreak >nul

REM Open the browser automatically
start http://localhost:5000

REM Keep the window open to show server status
echo.
echo ✅ App started successfully!
echo ✅ Browser opened to http://localhost:5000
echo.
echo Server is running... Press Ctrl+C to stop
echo ====================================

REM Wait for user to stop the server
pause >nul
