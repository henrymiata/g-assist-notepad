# Testing Guide for Notepad Plugin

This directory contains comprehensive testing tools for the G-Assist Notepad Plugin.

## 🧪 Test Files

### `test_plugin.py` - Automated Test Suite
A comprehensive automated test suite that validates all plugin functionality:

- **Plugin initialization and shutdown**
- **Notepad creation and entry addition**
- **Reading notepad contents**
- **Listing all notepads**
- **Searching through entries**
- **Deleting notepads**
- **Game separation (ensuring different games have separate notes)**

**Usage:**
```bash
python test_plugin.py
```

**Features:**
- ✅ Comprehensive test coverage
- 🔧 Automatic setup/teardown with temporary directories
- 📊 Detailed test results and success rates
- 🛡️ Tests both success and failure scenarios
- 🎮 Validates game-specific data separation

---

### `interactive_test.py` - Interactive Interface
A user-friendly command-line interface for manual testing and exploration:

**Usage:**
```bash
python interactive_test.py
```

**Features:**
- 🎮 Simulates G-Assist commands interactively
- 📝 User-friendly command syntax
- 🎲 Optional demo data setup
- 🔍 Real-time response formatting
- 💡 Built-in help system

**Commands:**
```
add <notepad> <content>     - Add entry to notepad
read <notepad>             - Read notepad entries
list                       - List all notepads
search <query>             - Search entries
delete <notepad>           - Delete notepad
game <name>                - Change current game
help                       - Show help
quit                       - Exit
```

**Example Session:**
```
🎮 [Cyberpunk 2077] > add Missions Kill 100 monsters for Prof Amy
✅ SUCCESS: Added entry #1 to notepad 'Missions'...

🎮 [Cyberpunk 2077] > search Prof Amy
✅ SUCCESS: Found 1 entries matching 'Prof Amy'...
🔍 Search Results:
   • Missions #1: Kill 100 monsters for Prof Amy

🎮 [Cyberpunk 2077] > list
✅ SUCCESS: Found 1 notepads for game 'Cyberpunk 2077'
📚 Notepads:
   • Missions: 1 entries
```

---

### `run_tests.sh` / `run_tests.bat` - Test Runners
Platform-specific scripts that provide an easy menu interface:

**Options:**
1. Run automated tests only
2. Run interactive interface only  
3. Run automated tests, then interactive interface

**Linux/macOS:**
```bash
./run_tests.sh
```

**Windows:**
```batch
run_tests.bat
```

---

## 🚀 Quick Start

### 1. Run All Tests
```bash
# Linux/macOS
./run_tests.sh

# Windows
run_tests.bat

# Or directly
python test_plugin.py
```

### 2. Interactive Testing
```bash
python interactive_test.py
```

### 3. Development Workflow
1. Make changes to `plugin.py`
2. Run automated tests: `python test_plugin.py`
3. If tests pass, manually test with: `python interactive_test.py`
4. Use demo data to quickly populate test entries

---

## 📋 Test Coverage

The test suite covers:

### ✅ Core Functionality
- Plugin initialization/shutdown
- Notepad creation and management
- Entry addition and retrieval
- Search functionality
- Deletion operations

### ✅ Edge Cases
- Missing parameters
- Non-existent notepads
- Empty search results
- Invalid inputs

### ✅ Game Separation
- Multiple games with same notepad names
- Cross-game data isolation
- Game switching scenarios

### ✅ Data Integrity
- Proper JSON structure
- Entry ID assignment
- Timestamp tracking
- File system operations

---

## 🔧 Development Tips

### Adding New Tests
1. Add test methods to `NotepadPluginTester` class
2. Follow naming convention: `test_feature_name()`
3. Use `assert_response()` for validation
4. Add comprehensive error checking

### Debugging
- Tests use temporary directories (auto-cleanup)
- All test operations are logged
- Response data is available for inspection
- Mock Windows APIs for cross-platform testing

### Mock Environment
The test files include mocks for Windows-specific APIs, allowing testing on any platform:
- `ctypes.windll` - Mocked Windows DLL access
- `wintypes` - Mocked Windows data types
- Pipe operations - Stubbed for testing

---

## 🎯 Example Test Output

```
🧪 Starting Notepad Plugin Test Suite
==================================================
✅ PASS: Plugin initialization
✅ PASS: Create first mission entry
   ✓ Entry ID correctly assigned as #1
✅ PASS: Create second mission entry
   ✓ Entry ID correctly assigned as #2
✅ PASS: Create character entry
❌ FAIL: Create note without title (should fail)
✅ PASS: Read missions notepad
   ✓ Correct number of entries found
...
==================================================
📊 Test Results:
   ✅ Passed: 15
   ❌ Failed: 0
   📈 Success Rate: 100.0%
🎉 All tests passed!
```

This comprehensive testing suite ensures your notepad plugin works correctly and helps catch issues during development!
