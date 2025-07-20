# Contributing to Notepad Plugin

We welcome contributions to the Notepad Plugin for NVIDIA G-Assist! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs
- Use the issue tracker to report bugs
- Include detailed steps to reproduce the issue
- Provide information about your environment (Windows version, Python version, etc.)
- Include relevant log files from `%USERPROFILE%\notepad-plugin.log`

### Suggesting Features
- Use the issue tracker to suggest new features
- Clearly describe the feature and its benefits
- Consider how it fits with the existing plugin architecture

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## Development Guidelines

### Code Style
- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Add type hints where appropriate

### Testing
- Test all new functionality thoroughly
- Ensure the plugin builds successfully with `build.bat`
- Test on a clean Windows environment when possible
- Verify compatibility with existing G-Assist functionality

### Documentation
- Update README.md if adding new features
- Include clear docstrings for new functions
- Update manifest.json if adding new commands

## Plugin Architecture

### File Structure
```
notepad/
├── manifest.json       # Plugin manifest defining capabilities
├── plugin.py          # Main plugin implementation
├── requirements.txt   # Python dependencies
├── setup.bat         # Environment setup script
├── build.bat         # Build script
├── README.md         # Documentation
└── CONTRIBUTING.md   # This file
```

### Key Components
- **Command Processing**: Handle incoming commands from G-Assist
- **Note Management**: Core note CRUD operations
- **File I/O**: Safe file operations with error handling
- **Logging**: Comprehensive logging for debugging
- **Windows Pipes**: Communication protocol with G-Assist

### Adding New Commands
1. Add the function definition to `manifest.json`
2. Implement the function in `plugin.py`
3. Add the function call to the main command router
4. Update documentation and tests

## License
By contributing to this project, you agree that your contributions will be licensed under the Apache License 2.0.
