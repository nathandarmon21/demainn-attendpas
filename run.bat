@echo off
REM Run script for Demain N'Attend Pas Multi-Agent System (Windows)

echo Starting Demain N'Attend Pas Multi-Agent System...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Streamlit app
streamlit run app.py
