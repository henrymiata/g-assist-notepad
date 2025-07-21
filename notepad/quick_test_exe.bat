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

REM Create a temporary file with all JSON commands
echo {"tool_calls":[{"func":"initialize","params":{}}]} > temp_commands.txt
echo {"tool_calls":[{"func":"create_note","params":{"title":"QuickTest","content":"This is a quick test from the exe","current_game":"TestGame"}}]} >> temp_commands.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"TestGame"}}]} >> temp_commands.txt
echo {"tool_calls":[{"func":"read_note","params":{"title":"QuickTest","current_game":"TestGame"}}]} >> temp_commands.txt
echo {"tool_calls":[{"func":"export_notes","params":{"scope":"game","current_game":"TestGame"}}]} >> temp_commands.txt
echo {"tool_calls":[{"func":"search_notes","params":{"query":"quick","current_game":"TestGame"}}]} >> temp_commands.txt
echo {"tool_calls":[{"func":"shutdown","params":{}}]} >> temp_commands.txt

echo 🔄 Running all tests in sequence...
echo.

REM Feed all commands to a single instance of the plugin
type temp_commands.txt | dist\notepad\g-assist-plugin-notepad.exe

REM Clean up
del temp_commands.txt

echo ✅ Quick test completed!
echo.
echo 💡 Check these locations for results:
echo    - Notes: %USERPROFILE%\Documents\G-Assist-Notes\TestGame\
echo    - Exports: %USERPROFILE%\Desktop\G-Assist_Export_*
echo    - Logs: %USERPROFILE%\notepad-plugin.log
echo.
pause
