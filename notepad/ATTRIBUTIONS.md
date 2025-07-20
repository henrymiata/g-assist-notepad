# Third-Party Attributions

This project includes or depends on the following third-party software:

## PyInstaller
- **License**: GPL v2 or later with a special exception allowing distribution of binary executables
- **Version**: 6.11.0
- **Description**: Converts Python applications into stand-alone executables
- **Website**: https://www.pyinstaller.org/
- **License Text**: See PyInstaller's license at https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt

## Python Standard Library
- **License**: Python Software Foundation License
- **Description**: Various modules from Python's standard library including:
  - `json`: JSON encoder and decoder
  - `logging`: Logging facility for Python
  - `os`: Operating system interface
  - `sys`: System-specific parameters and functions
  - `datetime`: Date and time handling
  - `ctypes`: Foreign function library for Python
  - `glob`: Unix shell-style wildcards
- **Website**: https://www.python.org/
- **License Text**: See https://docs.python.org/3/license.html

## Windows API
- **License**: Microsoft Software License Terms
- **Description**: Windows API functions accessed through ctypes:
  - `kernel32.dll`: Core Windows functions for file and pipe operations
  - `wintypes`: Windows data types
- **Note**: Used for pipe-based communication with G-Assist platform

---

**Note**: This software is provided "as is" without warranty of any kind. The licenses and attributions above apply to the respective third-party components only.
