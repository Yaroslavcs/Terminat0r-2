# Run backend and app in parallel (two terminals)
# Or run manually: .\run-backend.ps1 in one terminal, .\run-app.ps1 in another

Write-Host "Start backend: .\run-backend.ps1" -ForegroundColor Cyan
Write-Host "Start app:     .\run-app.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run each in a separate terminal" -ForegroundColor Gray

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; .\run-backend.ps1"
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; .\run-app.ps1"
