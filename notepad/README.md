# Notepad Plugin for NVIDIA G-Assist

A powerful note-taking plugin for NVIDIA G-Assist that lets you create, manage, and search notepads directly through the G-Assist platform. Organize your notes by game and category, and easily export them for backup or sharing.

## What Can It Do?
- Create new notepad entries with custom categories and content
- Read existing notepads with all their entries
- List all your notepads with entry counts and timestamps
- Delete notepads you no longer need
- Search through notepad entries across all categories
- Export notepads to human-readable text files on your Desktop
- Game-specific organization (notes are separated by current game)
- Automatic file management and organization
- Detailed logging for troubleshooting

## Features
- **Notepad Organization**: Create themed notepads like "Missions", "Characters", "Locations"
- **Game Separation**: Notes are automatically organized by the current game you're playing
- **Smart Search**: Find entries by searching through all notepad content
- **Export Functionality**: Export individual notepads, game collections, or everything to Desktop
- **Entry Management**: Each notepad contains multiple numbered entries
- **Organized Storage**: Notes are automatically saved in your Documents folder with game folders
- **Safe Filenames**: Automatically handles special characters in notepad titles and game names
- **Timestamped**: All notepads and entries include creation and modification timestamps
- **JSON Format**: Notepads are stored in a readable JSON format for easy backup

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

### Creating Notepad Entries
"Hey G-Assist, create a note titled 'Missions' with content 'Kill 100 monsters and report back to Prof Amy'"
"Hey G-Assist, create a note titled 'Characters' with content 'Prof Amy teaches cybernetics at Night City University'"

### Reading a Notepad
"Hey G-Assist, read my notepad titled 'Missions'"

### Listing All Notepads
"Hey G-Assist, list all my notepads"

### Searching Notepad Entries
"Hey G-Assist, search my notes for 'Prof Amy'"

### Exporting Notepads
"Hey G-Assist, export my notepad titled 'Missions'" (exports single notepad)
"Hey G-Assist, export my current game notes" (exports all notepads from current game)
"Hey G-Assist, export all my notes" (exports all notepads from all games)

### Deleting a Notepad
"Hey G-Assist, delete my notepad titled 'Old Ideas'"

## Note Storage
- Notes are stored in: `%USERPROFILE%\Documents\G-Assist-Notes\{Game Name}\`
- Each notepad is saved as a JSON file containing multiple entries
- Exported files are saved to your Desktop with timestamps
- Log files are saved to: `%USERPROFILE%\notepad-plugin.log`

## Notepad Format
Each notepad is stored as a JSON file containing:
```json
{
  "title": "Missions",
  "game": "Cyberpunk 2077",
  "created_at": "2024-03-14T12:34:56.789123",
  "updated_at": "2024-03-14T12:45:30.123456",
  "entries": [
    {
      "id": 1,
      "content": "Kill 100 monsters and report back to Prof Amy",
      "created_at": "2024-03-14T12:34:56.789123"
    },
    {
      "id": 2,
      "content": "Collect 50 cybernetic implants from corpo district",
      "created_at": "2024-03-14T12:40:15.456789"
    }
  ]
}
```

## Export Format
Exported files are human-readable text files with clear formatting:
- Single notepad exports: `G-Assist_Export_{Game}_{Notepad}_{Timestamp}.txt`
- Game exports: `G-Assist_Export_{Game}_All_Notepads_{Timestamp}.txt`
- Master exports: `G-Assist_Export_All_Games_{Timestamp}.txt`

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
1. **"Notepad already exists"**: You can add multiple entries to the same notepad
2. **"Notepad not found"**: Check the exact notepad title spelling and current game
3. **Permission errors**: Ensure you have write access to the Documents folder
4. **Export file not found**: Check your Desktop folder and ensure sufficient disk space

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
