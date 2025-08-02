@echo off
title Data Analyzer Pro

REM Set colors for better visibility
color 0A

echo.
echo ████████████████████████████████████████
echo          DATA ANALYZER PRO
echo        🚀 Starting Application...
echo ████████████████████████████████████████
echo.

REM Navigate to project directory
cd /d "c:\Users\HP\clone git reprository"

REM Quick check and cleanup
taskkill /f /im python.exe >nul 2>&1
python --version >nul 2>&1 || (
    echo ❌ Python not found! Install from python.org
    pause & exit /b 1
)

REM Install dependencies if needed
if not exist "venv" (
    echo 📦 Setting up virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat >nul 2>&1
pip install -r requirements.txt >nul 2>&1

REM Create directories
md uploads 2>nul
md outputs 2>nul
md static\plots 2>nul

echo ✅ Environment ready
echo 🚀 Starting server...

REM Start Flask app in background
start /min python app.py

REM Wait and test connection
timeout /t 4 /nobreak >nul

REM Test if server is running
python -c "import requests; requests.get('http://localhost:5000')" >nul 2>&1 || (
    python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" >nul 2>&1
)

if %errorlevel% equ 0 (
    cls
    echo.
    echo ████████████████████████████████████████
    echo          DATA ANALYZER PRO
    echo           🎉 READY TO USE!
    echo ████████████████████████████████████████
    echo.
    echo ✅ Server Running: http://localhost:5000
    echo 🌐 Opening browser automatically...
    echo.
    
    REM Open browser
    start http://localhost:5000
    
    echo 📊 Your Data Analysis App is now live!
    echo.
    echo ▶️ Upload data, analyze, and predict
    echo ▶️ Create beautiful visualizations  
    echo ▶️ Build machine learning models
    echo.
    echo Keep this window open while using the app
    echo ====================================
    echo Press any key to stop the server...
    pause >nul
    
    REM Cleanup
    taskkill /f /im python.exe >nul 2>&1
    echo 🛑 Server stopped. Safe to close.
    timeout /t 2 >nul
) else (
    echo ❌ Server failed to start
    echo Check the error messages above
    pause
)
