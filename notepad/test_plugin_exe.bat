@echo off
REM Master Test Script for Built Notepad Plugin Executable
REM Provides access to all testing options for the compiled plugin

echo 🎯 Notepad Plugin Executable Testing Suite
echo ============================================
echo.

REM Check if build exists
if not exist "dist\notepad\g-assist-plugin-notepad.exe" (
    echo ❌ Built executable not found!
    echo.
    echo Please run these steps first:
    echo 1. Run setup.bat to install dependencies
    echo 2. Run build.bat to create the executable
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo ✅ Found executable: dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Show build info
echo 📋 Build Information:
echo ---------------------
for %%f in (dist\notepad\g-assist-plugin-notepad.exe) do (
    echo Executable size: %%~zf bytes
    echo Build date: %%~tf
)
echo.

echo Choose testing option:
echo =====================
echo 1) Quick Test          - Basic functionality (recommended first test)
echo 2) Full Test           - All plugin commands and features  
echo 3) Stress Test         - Edge cases, error handling, multiple games
echo 4) Interactive Test    - Manual JSON command entry
echo 5) Show Plugin Info    - Display manifest and file details
echo 6) Clean Test Data     - Remove all test notes and files
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Running Quick Test...
    call quick_test_exe.bat
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Running Full Test...
    call test_exe.bat
    set /p continue="Press Enter to continue..."
    call test_exe.bat
) else if "%choice%"=="3" (
    echo.
    echo 🔥 Running Stress Test...
    call stress_test_exe.bat
) else if "%choice%"=="4" (
    echo.
    echo 🎮 Starting Interactive Test...
    call test_exe.bat
) else if "%choice%"=="5" (
    echo.
    echo 📋 Showing Plugin Information...
    echo.
    echo Manifest Content:
    echo -----------------
    type dist\notepad\manifest.json
    echo.
    echo.
    echo Files in dist\notepad\:
    echo ----------------------
    dir dist\notepad\
    pause
) else if "%choice%"=="6" (
    call :clean_test_data
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
    exit /b 1
)

goto :end

:clean_test_data
echo.
echo 🧹 Cleaning Test Data
echo =====================
echo.
echo This will remove:
echo - All test notes in %USERPROFILE%\Documents\G-Assist-Notes\
echo - All export files from Desktop (G-Assist_Export_*)
echo - Plugin log file
echo.
set /p confirm="Are you sure you want to clean all test data? (y/N): "

if /i "!confirm!"=="y" (
    echo.
    echo 🔄 Cleaning test data...
    
    REM Remove test notes
    if exist "%USERPROFILE%\Documents\G-Assist-Notes\" (
        echo Removing notes directory...
        rmdir /s /q "%USERPROFILE%\Documents\G-Assist-Notes\"
        echo ✅ Notes directory removed
    )
    
    REM Remove export files from Desktop
    if exist "%USERPROFILE%\Desktop\G-Assist_Export_*" (
        echo Removing export files from Desktop...
        del /q "%USERPROFILE%\Desktop\G-Assist_Export_*"
        echo ✅ Export files removed
    )
    
    REM Remove log file
    if exist "%USERPROFILE%\notepad-plugin.log" (
        echo Removing log file...
        del /q "%USERPROFILE%\notepad-plugin.log"
        echo ✅ Log file removed
    )
    
    echo.
    echo ✅ Test data cleanup completed!
) else (
    echo 🚫 Cleanup cancelled
)
pause
goto :end

:end
echo.
echo 💡 Testing Tips:
echo - Always run Quick Test first to verify basic functionality
echo - Use Stress Test to verify stability with complex scenarios
echo - Check log file for detailed operation history
echo - Export files are saved to your Desktop
echo.
echo 📁 Important Locations:
echo - Notes: %USERPROFILE%\Documents\G-Assist-Notes\
echo - Logs: %USERPROFILE%\notepad-plugin.log  
echo - Exports: %USERPROFILE%\Desktop\G-Assist_Export_*
