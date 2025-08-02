@echo off
echo ====================================
echo    Data Analyzer Pro - Smart Start
echo ====================================
echo.

REM Navigate to the project directory
cd /d "c:\Users\HP\clone git reprository"

REM Check if VS Code is running
tasklist /fi "imagename eq Code.exe" 2>NUL | find /i "Code.exe" >NUL
if %errorlevel% equ 0 (
    echo ⚠️ VS Code is currently running
    echo Please close VS Code first to avoid conflicts
    echo.
    choice /c YN /m "Continue anyway? (Y/N)"
    if errorlevel 2 exit /b 0
)

echo ✅ VS Code not detected, proceeding...
echo.

REM Kill any existing Python processes to avoid port conflicts
taskkill /f /im python.exe >nul 2>&1

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

echo Installing/updating dependencies...
pip install -r requirements.txt >nul 2>&1

echo ✅ Dependencies ready
echo.

echo Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "static\plots" mkdir static\plots

echo ✅ Directories ready
echo.

echo ====================================
echo    🚀 STARTING DATA ANALYZER PRO
echo ====================================
echo.

REM Start the app and capture the process ID
echo Starting Flask server...
start /B python app.py

REM Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Check if server is responding
python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Server is running!
    echo.
    echo 🌐 Opening browser to http://localhost:5000
    start http://localhost:5000
    echo.
    echo ====================================
    echo    🎉 SUCCESS!
    echo ====================================
    echo.
    echo ✅ Data Analyzer Pro is running
    echo ✅ Browser opened automatically
    echo 📊 Access your app at: http://localhost:5000
    echo.
    echo Keep this window open while using the app
    echo Press any key to stop the server...
    echo ====================================
    pause >nul
    
    REM Stop the server when user presses a key
    taskkill /f /im python.exe >nul 2>&1
    echo.
    echo 🛑 Server stopped. You can close this window.
    timeout /t 3 >nul
) else (
    echo ❌ Failed to start server
    echo Please check for errors above
    pause
)
