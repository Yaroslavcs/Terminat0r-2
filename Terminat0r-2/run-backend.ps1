Set-Location $PSScriptRoot
if (-not (Test-Path venv)) { py -m venv venv }
& .\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt -q
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
