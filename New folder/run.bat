@echo off
title CampusSaathi AI Launcher
color 0A
echo =======================================================================
echo          CampusSaathi AI - Local AI College Companion
echo =======================================================================
echo.
echo Launching CampusSaathi AI on http://localhost:8501 ...
echo.
python -m streamlit run app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Could not start Streamlit.
    echo Tip: If you haven't run setup yet, please double-click "setup.bat".
    echo.
    pause
)
