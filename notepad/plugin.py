"""Notepad Plugin for NVIDIA G-Assist Platform.

This plugin provides functionality to create, read, update, delete, and search notes.
It implements a Windows pipe-based communication protocol for receiving commands and
sending responses, following the G-Assist plugin architecture.

Configuration:
    Notes are stored in: %USERPROFILE%\\Documents\\G-Assist-Notes\\
    Log location: %USERPROFILE%\\notepad-plugin.log

Commands Supported:
    - initialize: Initialize the plugin
    - create_note: Create a new note with title and content
    - read_note: Read an existing note by title
    - list_notes: List all available notes
    - delete_note: Delete a note by title
    - search_notes: Search through note titles and content
    - shutdown: Gracefully shutdown the plugin

Dependencies:
    - os: For file system operations
    - json: For JSON handling
    - datetime: For timestamps
    - ctypes: For Windows pipe communication
"""

import json
import logging
import os
import sys
from typing import Optional, Dict, Any, List
from datetime import datetime
from ctypes import byref, windll, wintypes
import glob

# Type definitions
Response = Dict[str, Any]
"""Type alias for response dictionary containing 'success' and optional 'message'."""

# Constants
STD_INPUT_HANDLE = -10
"""Windows standard input handle constant."""

STD_OUTPUT_HANDLE = -11
"""Windows standard output handle constant."""

BUFFER_SIZE = 4096
"""Size of buffer for reading from pipe in bytes."""

NOTES_DIR = os.path.join(os.environ.get("USERPROFILE", "."), 'Documents', 'G-Assist-Notes')
"""Directory where notes are stored."""

LOG_FILE = os.path.join(os.environ.get("USERPROFILE", "."), 'notepad-plugin.log')
"""Path to log file for plugin operations."""

def setup_logging() -> None:
    """Configure logging with appropriate format and level.
    
    Sets up the logging configuration with file output, INFO level, and timestamp format.
    The log file location is determined by LOG_FILE constant.
    
    Log Format:
        %(asctime)s - %(levelname)s - %(message)s
        Example: 2024-03-14 12:34:56,789 - INFO - Plugin initialized
    """
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def ensure_notes_directory() -> None:
    """Ensure the notes directory exists."""
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
        logging.info(f"Created notes directory: {NOTES_DIR}")

def sanitize_filename(title: str) -> str:
    """Sanitize a title to be used as a filename.
    
    Args:
        title (str): The note title to sanitize.
    
    Returns:
        str: A safe filename.
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '_')
    
    # Limit length and add extension
    return title[:100] + '.json'

def sanitize_game_name(game_name: str) -> str:
    """Sanitize a game name to be used as a folder name.
    
    Args:
        game_name (str): The game name to sanitize.
    
    Returns:
        str: A safe folder name.
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        game_name = game_name.replace(char, '_')
    
    # Limit length
    return game_name[:100]

def get_game_notes_dir(game_name: str) -> str:
    """Get the directory for notes of a specific game.
    
    Args:
        game_name (str): The name of the game.
    
    Returns:
        str: The full path to the game's notes directory.
    """
    if not game_name or game_name.strip() == "":
        game_name = "General"
    
    safe_game_name = sanitize_game_name(game_name)
    return os.path.join(NOTES_DIR, safe_game_name)

def ensure_game_notes_directory(game_name: str) -> None:
    """Ensure the game-specific notes directory exists.
    
    Args:
        game_name (str): The name of the game.
    """
    game_dir = get_game_notes_dir(game_name)
    if not os.path.exists(game_dir):
        os.makedirs(game_dir)
        logging.info(f"Created game notes directory: {game_dir}")

def get_note_path(title: str, game_name: str = "General") -> str:
    """Get the full path for a note file.
    
    Args:
        title (str): The note title.
        game_name (str): The game name. Defaults to "General".
    
    Returns:
        str: The full path to the note file.
    """
    if not game_name or game_name.strip() == "":
        game_name = "General"
    
    game_dir = get_game_notes_dir(game_name)
    filename = sanitize_filename(title)
    return os.path.join(game_dir, filename)

def generate_response(success: bool, message: Optional[str] = None, data: Optional[Dict] = None) -> Response:
    """Generate a standardized response dictionary.
    
    Args:
        success (bool): Whether the operation was successful.
        message (Optional[str]): Optional message to include in response.
        data (Optional[Dict]): Optional data to include in response.
    
    Returns:
        Response: Dictionary containing success status and optional message/data.
    """
    response = {'success': success}
    if message:
        response['message'] = message
    if data:
        response['data'] = data
    return response

def create_note(params: Dict[str, str]) -> Response:
    """Create a new note with title and content.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'title', 'content', and 'current_game' keys.
    
    Returns:
        Response: Dictionary containing success status and message.
    """
    title = params.get("title")
    content = params.get("content")
    current_game = params.get("current_game", "General")
    
    if not title:
        return generate_response(False, "Missing required parameter: title")
    
    if not content:
        content = ""
    
    try:
        ensure_notes_directory()
        ensure_game_notes_directory(current_game)
        note_path = get_note_path(title, current_game)
        
        # Check if note already exists
        if os.path.exists(note_path):
            return generate_response(False, f"Note with title '{title}' already exists for game '{current_game}'")
        
        # Create note data
        note_data = {
            "title": title,
            "content": content,
            "game": current_game,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save note
        with open(note_path, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Created note: {title} for game: {current_game}")
        return generate_response(True, f"Note '{title}' created successfully for game '{current_game}'")
        
    except Exception as e:
        logging.error(f"Error creating note: {e}")
        return generate_response(False, f"Failed to create note: {str(e)}")

def read_note(params: Dict[str, str]) -> Response:
    """Read an existing note by title.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'title' and 'current_game' keys.
    
    Returns:
        Response: Dictionary containing success status, message, and note data.
    """
    title = params.get("title")
    current_game = params.get("current_game", "General")
    
    if not title:
        return generate_response(False, "Missing required parameter: title")
    
    try:
        note_path = get_note_path(title, current_game)
        
        if not os.path.exists(note_path):
            return generate_response(False, f"Note with title '{title}' not found for game '{current_game}'")
        
        # Read note
        with open(note_path, 'r', encoding='utf-8') as f:
            note_data = json.load(f)
        
        logging.info(f"Read note: {title} for game: {current_game}")
        return generate_response(True, f"Note '{title}' retrieved successfully from game '{current_game}'", note_data)
        
    except Exception as e:
        logging.error(f"Error reading note: {e}")
        return generate_response(False, f"Failed to read note: {str(e)}")

def list_notes(params: Dict[str, str]) -> Response:
    """List all available notes for a specific game.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'current_game' key.
    
    Returns:
        Response: Dictionary containing success status and list of notes.
    """
    current_game = params.get("current_game", "General")
    
    try:
        ensure_notes_directory()
        ensure_game_notes_directory(current_game)
        
        notes = []
        game_dir = get_game_notes_dir(current_game)
        pattern = os.path.join(game_dir, '*.json')
        
        for note_file in glob.glob(pattern):
            try:
                with open(note_file, 'r', encoding='utf-8') as f:
                    note_data = json.load(f)
                
                notes.append({
                    "title": note_data.get("title", "Unknown"),
                    "game": note_data.get("game", current_game),
                    "created_at": note_data.get("created_at", "Unknown"),
                    "updated_at": note_data.get("updated_at", "Unknown")
                })
            except Exception as e:
                logging.warning(f"Error reading note file {note_file}: {e}")
                continue
        
        # Sort by creation date
        notes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        logging.info(f"Listed {len(notes)} notes for game: {current_game}")
        message = f"Found {len(notes)} notes for game '{current_game}'"
        return generate_response(True, message, {"notes": notes, "game": current_game})
        
    except Exception as e:
        logging.error(f"Error listing notes: {e}")
        return generate_response(False, f"Failed to list notes: {str(e)}")

def delete_note(params: Dict[str, str]) -> Response:
    """Delete a note by title.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'title' and 'current_game' keys.
    
    Returns:
        Response: Dictionary containing success status and message.
    """
    title = params.get("title")
    current_game = params.get("current_game", "General")
    
    if not title:
        return generate_response(False, "Missing required parameter: title")
    
    try:
        note_path = get_note_path(title, current_game)
        
        if not os.path.exists(note_path):
            return generate_response(False, f"Note with title '{title}' not found for game '{current_game}'")
        
        # Delete note
        os.remove(note_path)
        
        logging.info(f"Deleted note: {title} for game: {current_game}")
        return generate_response(True, f"Note '{title}' deleted successfully from game '{current_game}'")
        
    except Exception as e:
        logging.error(f"Error deleting note: {e}")
        return generate_response(False, f"Failed to delete note: {str(e)}")

def search_notes(params: Dict[str, str]) -> Response:
    """Search through note titles and content for matching text within a specific game.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'query' and 'current_game' keys.
    
    Returns:
        Response: Dictionary containing success status and matching notes.
    """
    query = params.get("query")
    current_game = params.get("current_game", "General")
    
    if not query:
        return generate_response(False, "Missing required parameter: query")
    
    try:
        ensure_notes_directory()
        ensure_game_notes_directory(current_game)
        
        matching_notes = []
        game_dir = get_game_notes_dir(current_game)
        pattern = os.path.join(game_dir, '*.json')
        query_lower = query.lower()
        
        for note_file in glob.glob(pattern):
            try:
                with open(note_file, 'r', encoding='utf-8') as f:
                    note_data = json.load(f)
                
                title = note_data.get("title", "").lower()
                content = note_data.get("content", "").lower()
                
                if query_lower in title or query_lower in content:
                    matching_notes.append({
                        "title": note_data.get("title", "Unknown"),
                        "content": note_data.get("content", ""),
                        "game": note_data.get("game", current_game),
                        "created_at": note_data.get("created_at", "Unknown"),
                        "updated_at": note_data.get("updated_at", "Unknown")
                    })
                    
            except Exception as e:
                logging.warning(f"Error searching note file {note_file}: {e}")
                continue
        
        # Sort by creation date
        matching_notes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        logging.info(f"Search for '{query}' found {len(matching_notes)} notes in game: {current_game}")
        message = f"Found {len(matching_notes)} notes matching '{query}' in game '{current_game}'"
        return generate_response(True, message, {"notes": matching_notes, "game": current_game})
        
    except Exception as e:
        logging.error(f"Error searching notes: {e}")
        return generate_response(False, f"Failed to search notes: {str(e)}")

def read_command() -> Optional[Dict[str, Any]]:
    """Read command from stdin pipe.
    
    Reads data from Windows pipe in chunks until complete message is received.
    Expects JSON-formatted input.
    
    Returns:
        Optional[Dict[str, Any]]: Parsed command dictionary if successful,
                                 None if reading or parsing fails.
    
    Expected Command Format:
        {
            "tool_calls": [
                {
                    "func": "command_name",
                    "params": {
                        "param1": "value1",
                        ...
                    }
                }
            ]
        }
    """
    try:
        pipe = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
        chunks = []
        
        while True:
            message_bytes = wintypes.DWORD()
            buffer = bytes(BUFFER_SIZE)
            success = windll.kernel32.ReadFile(
                pipe,
                buffer,
                BUFFER_SIZE,
                byref(message_bytes),
                None
            )

            if not success:
                logging.error('Error reading from command pipe')
                return None

            chunk = buffer.decode('utf-8')[:message_bytes.value]
            chunks.append(chunk)

            if message_bytes.value < BUFFER_SIZE:
                break

        retval = ''.join(chunks)
        logging.info(f'Raw Input: {retval}')
        return json.loads(retval)
        
    except json.JSONDecodeError:
        logging.error(f'Received invalid JSON: {retval}')
        logging.exception("JSON decoding failed:")
        return None
    except Exception as e:
        logging.error(f'Exception in read_command(): {e}')
        return None

def write_response(response: Response) -> None:
    """Write response to stdout pipe.
    
    Writes JSON-formatted response to Windows pipe with <<END>> marker.
    The marker is used by the reader to determine the end of the response.
    
    Args:
        response (Response): Response dictionary to write.
    
    Response Format:
        JSON-encoded dictionary followed by <<END>> marker.
        Example: {"success":true,"message":"Plugin initialized successfully"}<<END>>
    """
    try:
        pipe = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        json_message = json.dumps(response) + '<<END>>'
        message_bytes = json_message.encode('utf-8')
        
        bytes_written = wintypes.DWORD()
        windll.kernel32.WriteFile(
            pipe,
            message_bytes,
            len(message_bytes),
            bytes_written,
            None
        )
    except Exception as e:
        logging.error(f'Error writing response: {e}')

def initialize() -> Response:
    """Initialize the plugin.
    
    Performs any necessary setup for the plugin.
    
    Returns:
        Response: Success response with initialization status.
    """
    logging.info("Initializing notepad plugin")
    ensure_notes_directory()
    return generate_response(True, "Notepad plugin initialized successfully")

def shutdown() -> Response:
    """Shutdown the plugin.
    
    Performs any necessary cleanup before plugin shutdown.
    
    Returns:
        Response: Success response with shutdown status.
    """
    logging.info("Shutting down notepad plugin")
    return generate_response(True, "Notepad plugin shutdown successfully")

def main() -> None:
    """Main plugin loop.
    
    Sets up logging and enters main command processing loop.
    Handles incoming commands and routes them to appropriate handlers.
    Continues running until shutdown command is received.
    
    Command Processing Flow:
        1. Read command from pipe
        2. Parse command and parameters
        3. Route to appropriate handler
        4. Write response back to pipe
        5. Repeat until shutdown command
    
    Error Handling:
        - Invalid commands return error response
        - Failed command reads are logged and loop continues
        - Shutdown command exits loop gracefully
    """
    setup_logging()
    logging.info("Notepad Plugin Started")
    
    while True:
        command = read_command()
        if command is None:
            logging.error('Error reading command')
            continue
        
        tool_calls = command.get("tool_calls", [])
        for tool_call in tool_calls:
            func = tool_call.get("func")
            params = tool_call.get("params", {})
            
            if func == "initialize":
                response = initialize()
            elif func == "create_note":
                response = create_note(params)
            elif func == "read_note":
                response = read_note(params)
            elif func == "list_notes":
                response = list_notes(params)
            elif func == "delete_note":
                response = delete_note(params)
            elif func == "search_notes":
                response = search_notes(params)
            elif func == "shutdown":
                response = shutdown()
                write_response(response)
                return
            else:
                response = generate_response(False, f"Unknown function call: {func}")
            
            write_response(response)

if __name__ == "__main__":
    main()
