@echo off
echo ====================================
echo    SIMPLE DIAGNOSTIC TEST
echo ====================================
echo.

REM Navigate to the project directory
cd /d "c:\Users\HP\clone git reprository"

echo Current directory: %CD%
echo.

echo Testing Python...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Python is not working!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python is working
echo.

echo Testing if app.py exists...
if exist app.py (
    echo ✅ app.py found
) else (
    echo ❌ app.py NOT found in current directory
    echo Please make sure you're in the right folder
    pause
    exit /b 1
)

echo.
echo Testing Flask...
python -c "import flask; print('✅ Flask is working')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Flask not installed
    echo Installing Flask...
    pip install flask
)

echo.
echo Testing dependencies...
python -c "import pandas, numpy, matplotlib; print('✅ Dependencies OK')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Some dependencies missing, installing...
    pip install -r requirements.txt
)

echo.
echo ====================================
echo    STARTING APP NOW
echo ====================================
echo.
echo If successful, go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python app.py

echo.
echo App stopped. Press any key to exit...
pause >nul
)

echo.
echo Installing dependencies (this may take a moment)...
pip install flask pandas numpy matplotlib seaborn scikit-learn plotly scipy

echo.
echo Starting the web application...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
