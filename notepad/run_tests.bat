@echo off
REM Test Runner Script for Notepad Plugin (Windows)
REM This script runs both the automated tests and provides an option to run the interactive interface

echo 🧪 Notepad Plugin Test Suite
echo ==============================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    pause
    exit /b 1
)

echo 🐍 Python found
python --version

echo.
echo Choose an option:
echo 1) Run automated tests
echo 2) Run interactive interface
echo 3) Run both
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🤖 Running automated tests...
    python test_plugin.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo 🎮 Starting interactive interface...
    python interactive_test.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo 🤖 Running automated tests first...
    python test_plugin.py
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ All tests passed! Starting interactive interface...
        pause
        python interactive_test.py
    ) else (
        echo.
        echo ❌ Some tests failed. Fix issues before using interactive interface.
        pause
        exit /b 1
    )
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
    exit /b 1
)
