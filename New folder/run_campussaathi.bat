@echo off
title CampusSaathi AI Launcher
echo ========================================================
echo   CampusSaathi AI - Local AI College Companion
echo   Powered by Python, Streamlit, Ollama and Gemma 3:1B
echo ========================================================
echo.
echo Checking dependencies and starting the application...
echo.

python -m streamlit run app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application encountered an error.
    echo Please ensure Python and required packages are installed.
    echo.
    pause
)
