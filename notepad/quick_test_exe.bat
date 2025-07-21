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

REM Test 1: Initialize
echo 🔄 Test 1: Initialize plugin
echo {"tool_calls":[{"func":"initialize","params":{}}]} | dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Test 2: Create a note
echo 🔄 Test 2: Create note
echo {"tool_calls":[{"func":"create_note","params":{"title":"QuickTest","content":"This is a quick test from the exe","current_game":"TestGame"}}]} | dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Test 3: List notes
echo 🔄 Test 3: List notes
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"TestGame"}}]} | dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Test 4: Read the note we created
echo 🔄 Test 4: Read note
echo {"tool_calls":[{"func":"read_note","params":{"title":"QuickTest","current_game":"TestGame"}}]} | dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Test 5: Export notes
echo 🔄 Test 5: Export notes
echo {"tool_calls":[{"func":"export_notes","params":{"scope":"game","current_game":"TestGame"}}]} | dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Test 6: Search
echo 🔄 Test 6: Search notes
echo {"tool_calls":[{"func":"search_notes","params":{"query":"quick","current_game":"TestGame"}}]} | dist\notepad\g-assist-plugin-notepad.exe
echo.

REM Test 7: Shutdown
echo 🔄 Test 7: Shutdown plugin
echo {"tool_calls":[{"func":"shutdown","params":{}}]} | dist\notepad\g-assist-plugin-notepad.exe
echo.

echo ✅ Quick test completed!
echo.
echo 💡 Check these locations for results:
echo    - Notes: %USERPROFILE%\Documents\G-Assist-Notes\TestGame\
echo    - Exports: %USERPROFILE%\Desktop\G-Assist_Export_*
echo    - Logs: %USERPROFILE%\notepad-plugin.log
echo.
pause
