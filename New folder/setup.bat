@echo off
title CampusSaathi AI - Automatic Setup
color 0B
echo =======================================================================
echo          CampusSaathi AI - One-Click Automatic Setup
echo =======================================================================
echo.
echo [1/3] Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python is not installed or not found in system PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check the box "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Installing required packages (streamlit, requests, pypdf)...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Retrying with --user flag...
    python -m pip install --user -r requirements.txt
)

echo.
echo [3/3] Ensuring Gemma 3:1B model is downloaded in Ollama...
where ollama >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Pulling gemma3:1b (if not already downloaded)...
    ollama pull gemma3:1b
) else (
    echo [NOTE] Ollama command not found in PATH.
    echo If Ollama is running in your taskbar, you can continue.
)

echo.
echo =======================================================================
echo   Setup Complete! Launching CampusSaathi AI Web Application...
echo =======================================================================
echo.
python -m streamlit run app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [INFO] If Streamlit encountered an issue, press any key to exit.
    pause
)
