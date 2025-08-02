# Script to create a desktop shortcut for Data Analyzer Pro

$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Data Analyzer Pro.lnk")
$Shortcut.TargetPath = "c:\Users\HP\clone git reprository\launch_app.bat"
$Shortcut.WorkingDirectory = "c:\Users\HP\clone git reprository"
$Shortcut.Description = "Data Analyzer Pro - Auto-launching web app"
$Shortcut.IconLocation = "c:\Windows\System32\imageres.dll,100"
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: 'Data Analyzer Pro'" -ForegroundColor Green
Write-Host "🖱️ Double-click the shortcut to launch your app!" -ForegroundColor Blue
Read-Host "Press Enter to continue"
