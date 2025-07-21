@echo off
REM Test Script for Built Notepad Plugin Executable (Windows)
REM This script tests the compiled .exe file in dist/notepad folder

setlocal enabledelayedexpansion

echo 🧪 Notepad Plugin Executable Test Suite
echo ==========================================

REM Check if dist/notepad directory exists
if not exist "dist\notepad" (
    echo ❌ dist\notepad directory not found. Please run build.bat first.
    pause
    exit /b 1
)

REM Check if the executable exists
if not exist "dist\notepad\g-assist-plugin-notepad.exe" (
    echo ❌ g-assist-plugin-notepad.exe not found in dist\notepad\.
    echo Please run build.bat to create the executable first.
    pause
    exit /b 1
)

echo ✅ Found executable: dist\notepad\g-assist-plugin-notepad.exe

REM Check if manifest.json exists
if not exist "dist\notepad\manifest.json" (
    echo ❌ manifest.json not found in dist\notepad\.
    pause
    exit /b 1
)

echo ✅ Found manifest: dist\notepad\manifest.json

echo.
echo Choose test option:
echo 1) Basic connectivity test (initialize + shutdown)
echo 2) Full command test (test all plugin functions)
echo 3) Interactive JSON command test
echo 4) Show plugin info
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    call :test_basic
) else if "%choice%"=="2" (
    call :test_full
) else if "%choice%"=="3" (
    call :test_interactive
) else if "%choice%"=="4" (
    call :show_info
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
    exit /b 1
)

goto :end

:test_basic
echo.
echo 🔄 Running basic connectivity test...
echo.

REM Create input commands file
echo {"tool_calls":[{"func":"initialize","params":{}}]} > temp_input.txt
echo {"tool_calls":[{"func":"shutdown","params":{}}]} >> temp_input.txt

echo Testing plugin initialization and shutdown...
echo.

REM Run plugin with input redirection (synchronous)
dist\notepad\g-assist-plugin-notepad.exe < temp_input.txt > temp_output.txt 2>&1

REM Show results
echo Plugin output:
echo --------------
if exist temp_output.txt (
    type temp_output.txt
) else (
    echo No output file generated
)

REM Clean up
if exist temp_input.txt del temp_input.txt
if exist temp_output.txt del temp_output.txt

echo.
echo ✅ Basic connectivity test completed successfully!
goto :test_end

:test_full
echo.
echo 🔄 Running full command test...
echo.

REM Create input commands file
echo {"tool_calls":[{"func":"initialize","params":{}}]} > temp_full_input.txt
echo {"tool_calls":[{"func":"create_note","params":{"title":"TestNotepad","content":"Test content from exe","current_game":"TestGame"}}]} >> temp_full_input.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"TestGame"}}]} >> temp_full_input.txt
echo {"tool_calls":[{"func":"read_note","params":{"title":"TestNotepad","current_game":"TestGame"}}]} >> temp_full_input.txt
echo {"tool_calls":[{"func":"search_notes","params":{"query":"Test","current_game":"TestGame"}}]} >> temp_full_input.txt
echo {"tool_calls":[{"func":"export_notes","params":{"scope":"game","current_game":"TestGame"}}]} >> temp_full_input.txt
echo {"tool_calls":[{"func":"clear_notes","params":{"scope":"game","current_game":"TestGame"}}]} >> temp_full_input.txt
echo {"tool_calls":[{"func":"undo_clear","params":{}}]} >> temp_full_input.txt
echo {"tool_calls":[{"func":"shutdown","params":{}}]} >> temp_full_input.txt

echo Running all test commands in sequence...
echo.

REM Run plugin with input redirection (synchronous)
dist\notepad\g-assist-plugin-notepad.exe < temp_full_input.txt > temp_full_output.txt 2>&1

REM Show results
echo Plugin output:
echo --------------
if exist temp_full_output.txt (
    type temp_full_output.txt
) else (
    echo No output file generated
)

REM Clean up
if exist temp_full_input.txt del temp_full_input.txt
if exist temp_full_output.txt del temp_full_output.txt

echo.
echo ✅ Full command test completed!
goto :test_end

:test_interactive
echo.
echo 🎮 Interactive JSON Command Test
echo =================================
echo.
echo This mode sends individual commands to separate plugin instances.
echo For multi-command sessions, use the plugin manually or try the full test.
echo.
echo Enter JSON commands to test the plugin directly.
echo Examples:
echo   {"tool_calls":[{"func":"initialize","params":{}}]}
echo   {"tool_calls":[{"func":"create_note","params":{"title":"Test","content":"Hello","current_game":"MyGame"}}]}
echo   {"tool_calls":[{"func":"list_notes","params":{"current_game":"MyGame"}}]}
echo   {"tool_calls":[{"func":"shutdown","params":{}}]}
echo.
echo Type 'quit' to exit interactive mode.
echo.

:interactive_loop
set /p "json_cmd=JSON Command: "
if /i "!json_cmd!"=="quit" goto :test_end

if "!json_cmd!"=="" (
    echo Please enter a valid JSON command or 'quit'
    goto :interactive_loop
)

REM Create temp files for this command
echo !json_cmd! > temp_interactive_input.txt
echo {"tool_calls":[{"func":"shutdown","params":{}}]} >> temp_interactive_input.txt

REM Execute command (synchronous)
dist\notepad\g-assist-plugin-notepad.exe < temp_interactive_input.txt > temp_interactive_output.txt 2>&1

REM Show results
echo.
echo Response:
echo ---------
if exist temp_interactive_output.txt (
    type temp_interactive_output.txt
) else (
    echo No output generated
)
echo.

REM Clean up
if exist temp_interactive_input.txt del temp_interactive_input.txt
if exist temp_interactive_output.txt del temp_interactive_output.txt

goto :interactive_loop

:show_info
echo.
echo 📋 Plugin Information
echo =====================
echo.

REM Show manifest content
echo Manifest.json content:
echo ----------------------
type dist\notepad\manifest.json
echo.
echo.

REM Show file sizes
echo File Information:
echo -----------------
for %%f in (dist\notepad\*) do (
    echo %%~nxf - %%~zf bytes
)
echo.

REM Show directory structure
echo Directory Structure:
echo --------------------
dir /s dist\notepad

goto :test_end

:test_end
echo.
echo 📊 Test completed!
echo.
echo 💡 Tips:
echo - Check %USERPROFILE%\Documents\G-Assist-Notes\ for created notes
echo - Check %USERPROFILE%\notepad-plugin.log for detailed logs
echo - Check Desktop for exported files
pause
goto :end

:end
endlocal
