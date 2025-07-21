@echo off
REM Stress Test Script for Built Notepad Plugin Executable
REM Tests edge cases, error handling, and multiple operations

echo 🔥 Notepad Plugin Executable Stress Test
echo ==========================================

if not exist "dist\notepad\g-assist-plugin-notepad.exe" (
    echo ❌ Executable not found. Run build.bat first.
    pause
    exit /b 1
)

echo ✅ Starting stress test...
echo.

REM Create a temporary file with all stress test commands
echo {"tool_calls":[{"func":"initialize","params":{}}]} > temp_stress_commands.txt

REM Test with multiple games
echo {"tool_calls":[{"func":"create_note","params":{"title":"Missions","content":"Primary mission: Defeat the dragon","current_game":"RPG Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"create_note","params":{"title":"Missions","content":"Side quest: Find the lost artifact","current_game":"RPG Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"create_note","params":{"title":"Builds","content":"Sniper build with stealth focus","current_game":"FPS Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"create_note","params":{"title":"Strategy","content":"Rush early, expand mid-game","current_game":"RTS Game"}}]} >> temp_stress_commands.txt

REM Test special characters and long content
echo {"tool_calls":[{"func":"create_note","params":{"title":"Special Characters","content":"Test with special chars: àáâãäåæçèéêë ñòóôõö ùúûüý ÀÁÂÃÄÅÆÇÈÉÊË ÑÒÓÔÕÖØÙÚÛÜÝß 漢字 한국어 العربية русский","current_game":"Unicode Test"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"create_note","params":{"title":"Long Content","content":"This is a very long note to test how the plugin handles large amounts of text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.","current_game":"Stress Test"}}]} >> temp_stress_commands.txt

REM Test error conditions
echo {"tool_calls":[{"func":"create_note","params":{"content":"Missing title parameter","current_game":"Error Test"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"read_note","params":{"title":"NonExistent","current_game":"Error Test"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"delete_note","params":{"title":"NonExistent","current_game":"Error Test"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"unknown_function","params":{}}]} >> temp_stress_commands.txt

REM Test all list operations
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"RPG Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"FPS Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"RTS Game"}}]} >> temp_stress_commands.txt

REM Test search across all content
echo {"tool_calls":[{"func":"search_notes","params":{"query":"mission","current_game":"RPG Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"search_notes","params":{"query":"build","current_game":"FPS Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"search_notes","params":{"query":"special","current_game":"Unicode Test"}}]} >> temp_stress_commands.txt

REM Test export functionality
echo {"tool_calls":[{"func":"export_notes","params":{"scope":"notepad","title":"Missions","current_game":"RPG Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"export_notes","params":{"scope":"game","current_game":"FPS Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"export_notes","params":{"scope":"all"}}]} >> temp_stress_commands.txt

REM Test clear and undo operations
echo {"tool_calls":[{"func":"clear_notes","params":{"scope":"game","current_game":"Stress Test"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"undo_clear","params":{}}]} >> temp_stress_commands.txt

REM Final verification
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"RPG Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"FPS Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"RTS Game"}}]} >> temp_stress_commands.txt
echo {"tool_calls":[{"func":"list_notes","params":{"current_game":"Unicode Test"}}]} >> temp_stress_commands.txt

REM Shutdown
echo {"tool_calls":[{"func":"shutdown","params":{}}]} >> temp_stress_commands.txt

echo 🔄 Running comprehensive stress test...
echo.
type temp_stress_commands.txt | dist\notepad\g-assist-plugin-notepad.exe

REM Clean up
del temp_stress_commands.txt

echo ✅ Stress test completed!
echo.
echo 📊 Results Summary:
echo - Created notes for 4 different games
echo - Tested special characters and Unicode
echo - Tested error conditions and edge cases
echo - Tested all export options (notepad, game, all)
echo - Tested clear and undo operations
echo - Tested search across different content
echo.
echo 💡 Check these locations:
echo    - Notes: %USERPROFILE%\Documents\G-Assist-Notes\
echo    - Exports: %USERPROFILE%\Desktop\G-Assist_Export_*
echo    - Recycle Bin: %USERPROFILE%\Documents\G-Assist-Notes\.recycle_bin\
echo    - Logs: %USERPROFILE%\notepad-plugin.log
echo.
pause
