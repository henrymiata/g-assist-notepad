# Notepad Plugin for NVIDIA G-Assist

A powerful note-taking plugin for NVIDIA G-Assist that lets you create, manage, and search notes directly through the G-Assist platform. Keep your thoughts organized and easily accessible without leaving your G-Assist experience.

## What Can It Do?
- Create new notes with custom titles and content
- Read existing notes by title
- List all your notes with creation/update timestamps
- Delete notes you no longer need
- Search through note titles and content
- Automatic file management and organization
- Detailed logging for troubleshooting

## Features
- **Simple Note Management**: Create, read, update, and delete notes with ease
- **Smart Search**: Find notes by searching through titles and content
- **Organized Storage**: Notes are automatically saved in your Documents folder
- **Safe Filenames**: Automatically handles special characters in note titles
- **Timestamped**: All notes include creation and modification timestamps
- **JSON Format**: Notes are stored in a readable JSON format for easy backup

## Before You Start
Make sure you have:
- Windows PC
- Python 3.6 or higher installed
- NVIDIA G-Assist installed

## Installation Guide

### Step 1: Get the Files
```bash
git clone <repo link>
cd notepad
```
This downloads all the necessary files to your computer.

### Step 2: Setup and Build
1. Run the setup script:
```bash
setup.bat
```
This installs all required Python packages and sets up the virtual environment.

2. Run the build script:
```bash
build.bat
```
This creates the executable and prepares all necessary files.

### Step 3: Install the Plugin
1. Copy the contents of the `dist/notepad/` folder to your G-Assist plugins directory
2. The plugin will be automatically detected by G-Assist

## Usage Examples

### Creating a Note
"Hey G-Assist, create a note titled 'Meeting Notes' with content 'Discuss project timeline and deliverables'"

### Reading a Note
"Hey G-Assist, read my note titled 'Meeting Notes'"

### Listing All Notes
"Hey G-Assist, list all my notes"

### Searching Notes
"Hey G-Assist, search my notes for 'project'"

### Deleting a Note
"Hey G-Assist, delete my note titled 'Old Ideas'"

## Note Storage
- Notes are stored in: `%USERPROFILE%\Documents\G-Assist-Notes\`
- Each note is saved as a JSON file with a sanitized filename
- Log files are saved to: `%USERPROFILE%\notepad-plugin.log`

## Note Format
Each note is stored as a JSON file containing:
```json
{
  "title": "Note Title",
  "content": "Note content here...",
  "created_at": "2024-03-14T12:34:56.789123",
  "updated_at": "2024-03-14T12:34:56.789123"
}
```

## Troubleshooting

### Build Issues
- Ensure Python is installed and available in your PATH
- Run `setup.bat` before `build.bat`
- Check that you have sufficient disk space

### Plugin Not Working
- Check the log file at `%USERPROFILE%\notepad-plugin.log`
- Ensure the notes directory has write permissions
- Verify the plugin files are in the correct G-Assist directory

### Common Issues
1. **"Note already exists"**: Use a different title or delete the existing note first
2. **"Note not found"**: Check the exact title spelling and case
3. **Permission errors**: Ensure you have write access to the Documents folder

## Development
This plugin follows the standard G-Assist plugin architecture:
- `manifest.json`: Defines plugin capabilities and functions
- `plugin.py`: Main plugin implementation
- `requirements.txt`: Python dependencies
- `setup.bat`: Environment setup script
- `build.bat`: Build script to create executable

## License
This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.
