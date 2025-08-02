# Data Analyzer Pro - PowerShell Launcher
# Automatically opens browser when VS Code is not running

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        DATA ANALYZER PRO" -ForegroundColor Green
Write-Host "     🚀 Smart Auto-Launcher" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set location
Set-Location "c:\Users\HP\clone git reprository"

# Check if VS Code is running
$vscode = Get-Process "Code" -ErrorAction SilentlyContinue
if ($vscode) {
    Write-Host "⚠️ VS Code is currently running" -ForegroundColor Yellow
    $choice = Read-Host "Close VS Code for best results. Continue anyway? (y/n)"
    if ($choice -ne "y") { exit }
}

# Kill any existing Python processes
Get-Process "python" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Install from python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host "📦 Checking dependencies..." -ForegroundColor Blue
pip install -r requirements.txt | Out-Null

# Create directories
New-Item -ItemType Directory -Force -Path "uploads", "outputs", "static/plots" | Out-Null

Write-Host "✅ Environment ready" -ForegroundColor Green
Write-Host ""

# Start the server
Write-Host "🚀 Starting Flask server..." -ForegroundColor Blue
$job = Start-Job -ScriptBlock { 
    Set-Location "c:\Users\HP\clone git reprository"
    python app.py 
}

# Wait for server to start
Start-Sleep -Seconds 5

# Test if server is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 5 -ErrorAction Stop
    
    Clear-Host
    Write-Host "████████████████████████████████████████" -ForegroundColor Green
    Write-Host "          DATA ANALYZER PRO" -ForegroundColor White
    Write-Host "           🎉 READY TO USE!" -ForegroundColor Yellow
    Write-Host "████████████████████████████████████████" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ Server Running: http://localhost:5000" -ForegroundColor Green
    Write-Host "🌐 Opening browser automatically..." -ForegroundColor Blue
    Write-Host ""
    
    # Open browser
    Start-Process "http://localhost:5000"
    
    Write-Host "📊 Your Data Analysis App is now live!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "▶️ Upload data, analyze, and predict" -ForegroundColor White
    Write-Host "▶️ Create beautiful visualizations" -ForegroundColor White  
    Write-Host "▶️ Build machine learning models" -ForegroundColor White
    Write-Host ""
    Write-Host "Keep this window open while using the app" -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Cyan
    Read-Host "Press Enter to stop the server"
    
    # Cleanup
    Stop-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job -ErrorAction SilentlyContinue
    Get-Process "python" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "🛑 Server stopped. Safe to close." -ForegroundColor Red
    Start-Sleep -Seconds 2
    
} catch {
    Write-Host "❌ Server failed to start" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Stop-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job -ErrorAction SilentlyContinue
    Read-Host "Press Enter to exit"
}
