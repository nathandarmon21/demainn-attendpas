@echo off
REM Setup script for Demain N'Attend Pas Multi-Agent System (Windows)

echo ================================================
echo   Demain N'Attend Pas - Multi-Agent Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed. Please install Python 3.8 or higher first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo OK Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt

REM Check for .env file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo WARNING: You need to add your API keys to the .env file
    echo.
)

echo.
echo ================================================
echo Setup complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit the .env file and add your API keys:
echo    - ANTHROPIC_API_KEY (get from: https://console.anthropic.com/settings/keys)
echo    - OPENAI_API_KEY (get from: https://platform.openai.com/api-keys)
echo.
echo 2. Run the application:
echo    run.bat
echo.
echo Or manually:
echo    venv\Scripts\activate.bat
echo    streamlit run app.py
echo.
pause
