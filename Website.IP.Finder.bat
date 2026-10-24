@echo off
title Website.IP.Finder
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py "Website.IP.Finder.py" %*
) else (
    python "Website.IP.Finder.py" %*
)

if %errorlevel% neq 0 (
    echo.
    echo [Program exited with error %errorlevel%]
    pause
)