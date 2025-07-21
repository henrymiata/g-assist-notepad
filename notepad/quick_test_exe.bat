@echo off
REM Quick Test Script for Built Notepad Plugin Executable
REM Tests the essential functionality of the compiled plugin

echo 🚀 Quick Notepad Plugin Executable Test
echo ========================================

REM Check if executable exists
if not exist "dist\notepad\g-assist-plugin-notepad.exe" (
    echo ❌ Executable not found. Run build.bat first.
    pause
    exit /b 1
)

echo ✅ Testing executable: dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Create input commands file
echo {"tool_calls":[{"func":"initialize","params":{}}]} > temp_quick_input.txt
echo {"tool_calls":[{"func":"create_note","params":{"title":"QuickTest","content":"This is a quick test from the exe","current_game":"TestGame"}}]} >> temp_quick_input.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"TestGame"}}]} >> temp_quick_input.txt
echo {"tool_calls":[{"func":"read_note","params":{"title":"QuickTest","current_game":"TestGame"}}]} >> temp_quick_input.txt
echo {"tool_calls":[{"func":"export_notes","params":{"scope":"game","current_game":"TestGame"}}]} >> temp_quick_input.txt
echo {"tool_calls":[{"func":"search_notes","params":{"query":"quick","current_game":"TestGame"}}]} >> temp_quick_input.txt
echo {"tool_calls":[{"func":"shutdown","params":{}}]} >> temp_quick_input.txt

echo 🔄 Running all tests in sequence...
echo.

REM Run plugin with input redirection (synchronous)
dist\notepad\g-assist-plugin-notepad.exe < temp_quick_input.txt > temp_quick_output.txt 2>&1

REM Show results
echo Plugin output:
echo --------------
if exist temp_quick_output.txt (
    type temp_quick_output.txt
) else (
    echo No output file generated
)

REM Clean up
if exist temp_quick_input.txt del temp_quick_input.txt
if exist temp_quick_output.txt del temp_quick_output.txt

echo ✅ Quick test completed!
echo.
echo 💡 Check these locations for results:
echo    - Notes: %USERPROFILE%\Documents\G-Assist-Notes\TestGame\
echo    - Exports: %USERPROFILE%\Desktop\G-Assist_Export_*
echo    - Logs: %USERPROFILE%\notepad-plugin.log
echo.
pause
