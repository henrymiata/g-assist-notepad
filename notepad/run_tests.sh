#!/bin/bash

# Test Runner Script for Notepad Plugin
# This script runs both the automated tests and provides an option to run the interactive interface

echo "🧪 Notepad Plugin Test Suite"
echo "=============================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "🐍 Python 3 found: $(python3 --version)"

# Make scripts executable
chmod +x test_plugin.py
chmod +x interactive_test.py

echo ""
echo "Choose an option:"
echo "1) Run automated tests"
echo "2) Run interactive interface"
echo "3) Run both"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🤖 Running automated tests..."
        python3 test_plugin.py
        ;;
    2)
        echo ""
        echo "🎮 Starting interactive interface..."
        python3 interactive_test.py
        ;;
    3)
        echo ""
        echo "🤖 Running automated tests first..."
        python3 test_plugin.py
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ All tests passed! Starting interactive interface..."
            echo "Press Enter to continue or Ctrl+C to exit..."
            read
            python3 interactive_test.py
        else
            echo ""
            echo "❌ Some tests failed. Fix issues before using interactive interface."
            exit 1
        fi
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
