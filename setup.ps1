Write-Host "Detecting OS and Environment..."
# Upgrade PIP
python -m pip install --upgrade pip

# Create and Activate Virtual Environment
if (-Not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}
.venv\Scripts\Activate.ps1

# Install Dependencies
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
}

# Look for software
if ((Get-Command "npm" -ErrorAction SilentlyContinue) -eq $null) {
    Write-Host "Node.js not found. Please install Node.js."
} else {
    Write-Host "Node.js found. Installing frontend..."
    Set-Location frontend
    npm install
}

Write-Host "Launching platform..."
Set-Location ..
Start-Process powershell -ArgumentList "-NoExit", "-Command", ". .venv\Scripts\Activate.ps1; uvicorn backend.app.main:app --reload"
Set-Location frontend
npm start
