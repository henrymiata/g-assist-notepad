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

echo 🔄 Running all tests in sequence...
echo.

REM Create a batch file that sends commands with echo and proper pipe handling
echo @echo off > temp_test_runner.bat
echo ^(echo {"tool_calls":[{"func":"initialize","params":{}}]} >> temp_test_runner.bat
echo echo {"tool_calls":[{"func":"create_note","params":{"title":"QuickTest","content":"This is a quick test from the exe","current_game":"TestGame"}}]} >> temp_test_runner.bat
echo echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"TestGame"}}]} >> temp_test_runner.bat
echo echo {"tool_calls":[{"func":"read_note","params":{"title":"QuickTest","current_game":"TestGame"}}]} >> temp_test_runner.bat
echo echo {"tool_calls":[{"func":"export_notes","params":{"scope":"game","current_game":"TestGame"}}]} >> temp_test_runner.bat
echo echo {"tool_calls":[{"func":"search_notes","params":{"query":"quick","current_game":"TestGame"}}]} >> temp_test_runner.bat
echo echo {"tool_calls":[{"func":"shutdown","params":{}}]}^) ^| dist\notepad\g-assist-plugin-notepad.exe >> temp_test_runner.bat

REM Run the test
call temp_test_runner.bat

REM Clean up
del temp_test_runner.bat

echo ✅ Quick test completed!
echo.
echo 💡 Check these locations for results:
echo    - Notes: %USERPROFILE%\Documents\G-Assist-Notes\TestGame\
echo    - Exports: %USERPROFILE%\Desktop\G-Assist_Export_*
echo    - Logs: %USERPROFILE%\notepad-plugin.log
echo.
pause
