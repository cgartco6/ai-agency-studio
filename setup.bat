@echo off
title AI Studio - Setup & Deployment
echo Detecting OS and Environment...

REM Upgrade PIP
python -m pip install --upgrade pip

REM Create and Activate Virtual Environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate

REM Install/Upgrade Dependencies
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Look for software (Node.js/npm)
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js not found. Please install Node.js manually to run the frontend.
) else (
    echo Node.js found. Installing frontend dependencies...
    cd frontend && npm install
)

echo Starting AI Studio Platform...
cd ..
start cmd /k "call .venv\Scripts\activate && uvicorn backend.app.main:app --reload"
cd frontend && npm start
pause
