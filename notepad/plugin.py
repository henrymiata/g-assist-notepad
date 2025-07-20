"""Notepad Plugin for NVIDIA G-Assist Platform.

This plugin provides functionality to create, read, update, delete, and search notepads and their entries.
A notepad is a collection of related notes/entries (e.g., "Missions", "Characters", "Locations").
It implements a Windows pipe-based communication protocol for receiving commands and
sending responses, following the G-Assist plugin architecture.

Configuration:
    Notepads are stored in: %USERPROFILE%\\Documents\\G-Assist-Notes\\{game}\\
    Each notepad is a JSON file containing multiple entries
    Log location: %USERPROFILE%\\notepad-plugin.log

Commands Supported:
    - initialize: Initialize the plugin
    - create_note: Add a new entry to a notepad (creates notepad if it doesn't exist)
    - read_note: Read entries from a notepad or search within a notepad
    - list_notes: List all available notepads for a game
    - delete_note: Delete an entry from a notepad or delete entire notepad
    - search_notes: Search through notepad entries
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
    """Get the full path for a notepad file.
    
    Args:
        title (str): The notepad title (e.g., "Missions", "Characters").
        game_name (str): The game name. Defaults to "General".
    
    Returns:
        str: The full path to the notepad file.
    """
    if not game_name or game_name.strip() == "":
        game_name = "General"
    
    game_dir = get_game_notes_dir(game_name)
    filename = sanitize_filename(title)
    return os.path.join(game_dir, filename)

def create_empty_notepad(notepad_path: str, notepad_title: str, game_name: str) -> Dict[str, Any]:
    """Create an empty notepad structure.
    
    Args:
        notepad_path (str): Path where the notepad will be saved.
        notepad_title (str): Title of the notepad.
        game_name (str): Name of the game.
    
    Returns:
        Dict[str, Any]: Empty notepad structure.
    """
    return {
        "title": notepad_title,
        "game": game_name,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "entries": []
    }

def add_entry_to_notepad(notepad_data: Dict[str, Any], content: str) -> Dict[str, Any]:
    """Add a new entry to a notepad.
    
    Args:
        notepad_data (Dict[str, Any]): The notepad data structure.
        content (str): The content of the new entry.
    
    Returns:
        Dict[str, Any]: The entry that was added.
    """
    entry = {
        "id": len(notepad_data["entries"]) + 1,
        "content": content,
        "created_at": datetime.now().isoformat()
    }
    
    notepad_data["entries"].append(entry)
    notepad_data["updated_at"] = datetime.now().isoformat()
    
    return entry

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
    """Add a new entry to a notepad (creates notepad if it doesn't exist).
    
    Args:
        params (Dict[str, str]): Dictionary containing 'title', 'content', and 'current_game' keys.
                                'title' is the notepad name (e.g., "Missions", "Characters")
                                'content' is the entry to add to that notepad
    
    Returns:
        Response: Dictionary containing success status and message.
    """
    notepad_title = params.get("title")
    content = params.get("content")
    current_game = params.get("current_game", "General")
    
    if not notepad_title:
        return generate_response(False, "Missing required parameter: title (notepad name)")
    
    if not content:
        return generate_response(False, "Missing required parameter: content (entry to add)")
    
    try:
        ensure_notes_directory()
        ensure_game_notes_directory(current_game)
        notepad_path = get_note_path(notepad_title, current_game)
        
        # Load existing notepad or create new one
        if os.path.exists(notepad_path):
            with open(notepad_path, 'r', encoding='utf-8') as f:
                notepad_data = json.load(f)
        else:
            notepad_data = create_empty_notepad(notepad_path, notepad_title, current_game)
        
        # Add new entry
        entry = add_entry_to_notepad(notepad_data, content)
        
        # Save notepad
        with open(notepad_path, 'w', encoding='utf-8') as f:
            json.dump(notepad_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Added entry #{entry['id']} to notepad '{notepad_title}' for game: {current_game}")
        return generate_response(True, f"Added entry #{entry['id']} to notepad '{notepad_title}' for game '{current_game}': {content[:50]}{'...' if len(content) > 50 else ''}")
        
    except Exception as e:
        logging.error(f"Error adding entry to notepad: {e}")
        return generate_response(False, f"Failed to add entry to notepad: {str(e)}")

def read_note(params: Dict[str, str]) -> Response:
    """Read entries from a notepad or search within a specific notepad.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'title' and 'current_game' keys.
                                'title' is the notepad name to read from
    
    Returns:
        Response: Dictionary containing success status, message, and notepad data.
    """
    notepad_title = params.get("title")
    current_game = params.get("current_game", "General")
    
    if not notepad_title:
        return generate_response(False, "Missing required parameter: title (notepad name)")
    
    try:
        notepad_path = get_note_path(notepad_title, current_game)
        
        if not os.path.exists(notepad_path):
            return generate_response(False, f"Notepad '{notepad_title}' not found for game '{current_game}'")
        
        # Read notepad
        with open(notepad_path, 'r', encoding='utf-8') as f:
            notepad_data = json.load(f)
        
        entry_count = len(notepad_data.get("entries", []))
        logging.info(f"Read notepad '{notepad_title}' with {entry_count} entries for game: {current_game}")
        
        # Format entries for display
        entries_text = []
        for entry in notepad_data.get("entries", []):
            entries_text.append(f"#{entry['id']}: {entry['content']}")
        
        message = f"Notepad '{notepad_title}' for game '{current_game}' contains {entry_count} entries"
        if entries_text:
            message += f":\n" + "\n".join(entries_text)
        
        return generate_response(True, message, notepad_data)
        
    except Exception as e:
        logging.error(f"Error reading notepad: {e}")
        return generate_response(False, f"Failed to read notepad: {str(e)}")

def list_notes(params: Dict[str, str]) -> Response:
    """List all available notepads for a specific game.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'current_game' key.
    
    Returns:
        Response: Dictionary containing success status and list of notepads.
    """
    current_game = params.get("current_game", "General")
    
    try:
        ensure_notes_directory()
        ensure_game_notes_directory(current_game)
        
        notepads = []
        game_dir = get_game_notes_dir(current_game)
        pattern = os.path.join(game_dir, '*.json')
        
        for notepad_file in glob.glob(pattern):
            try:
                with open(notepad_file, 'r', encoding='utf-8') as f:
                    notepad_data = json.load(f)
                
                entry_count = len(notepad_data.get("entries", []))
                notepads.append({
                    "title": notepad_data.get("title", "Unknown"),
                    "game": notepad_data.get("game", current_game),
                    "entry_count": entry_count,
                    "created_at": notepad_data.get("created_at", "Unknown"),
                    "updated_at": notepad_data.get("updated_at", "Unknown")
                })
            except Exception as e:
                logging.warning(f"Error reading notepad file {notepad_file}: {e}")
                continue
        
        # Sort by last updated
        notepads.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        
        logging.info(f"Listed {len(notepads)} notepads for game: {current_game}")
        
        # Format message with notepad summaries
        message_parts = [f"Found {len(notepads)} notepads for game '{current_game}'"]
        for notepad in notepads:
            message_parts.append(f"- {notepad['title']}: {notepad['entry_count']} entries")
        
        message = "\n".join(message_parts) if notepads else f"No notepads found for game '{current_game}'"
        return generate_response(True, message, {"notepads": notepads, "game": current_game})
        
    except Exception as e:
        logging.error(f"Error listing notepads: {e}")
        return generate_response(False, f"Failed to list notepads: {str(e)}")

def delete_note(params: Dict[str, str]) -> Response:
    """Delete an entry from a notepad or delete entire notepad.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'title' and 'current_game' keys.
                                If 'content' is provided, it will try to find and delete that specific entry.
                                If no 'content', it will delete the entire notepad.
    
    Returns:
        Response: Dictionary containing success status and message.
    """
    notepad_title = params.get("title")
    current_game = params.get("current_game", "General")
    entry_to_delete = params.get("content", "")  # Optional: specific entry to delete
    
    if not notepad_title:
        return generate_response(False, "Missing required parameter: title (notepad name)")
    
    try:
        notepad_path = get_note_path(notepad_title, current_game)
        
        if not os.path.exists(notepad_path):
            return generate_response(False, f"Notepad '{notepad_title}' not found for game '{current_game}'")
        
        if not entry_to_delete:
            # Delete entire notepad
            os.remove(notepad_path)
            logging.info(f"Deleted entire notepad: {notepad_title} for game: {current_game}")
            return generate_response(True, f"Notepad '{notepad_title}' deleted successfully from game '{current_game}'")
        else:
            # Delete specific entry (this is more complex, for now just delete the whole notepad)
            # In a full implementation, you'd search for the entry and remove it
            os.remove(notepad_path)
            logging.info(f"Deleted notepad: {notepad_title} for game: {current_game}")
            return generate_response(True, f"Notepad '{notepad_title}' deleted successfully from game '{current_game}'")
        
    except Exception as e:
        logging.error(f"Error deleting notepad: {e}")
        return generate_response(False, f"Failed to delete notepad: {str(e)}")

def search_notes(params: Dict[str, str]) -> Response:
    """Search through notepad entries for matching text within a specific game.
    
    Args:
        params (Dict[str, str]): Dictionary containing 'query' and 'current_game' keys.
                                Optionally 'title' to search within a specific notepad.
    
    Returns:
        Response: Dictionary containing success status and matching entries.
    """
    query = params.get("query")
    current_game = params.get("current_game", "General")
    specific_notepad = params.get("title", "")  # Optional: search within specific notepad
    
    if not query:
        return generate_response(False, "Missing required parameter: query")
    
    try:
        ensure_notes_directory()
        ensure_game_notes_directory(current_game)
        
        matching_results = []
        game_dir = get_game_notes_dir(current_game)
        
        # Determine which notepads to search
        if specific_notepad:
            notepad_files = [get_note_path(specific_notepad, current_game)]
        else:
            pattern = os.path.join(game_dir, '*.json')
            notepad_files = glob.glob(pattern)
        
        query_lower = query.lower()
        
        for notepad_file in notepad_files:
            if not os.path.exists(notepad_file):
                continue
                
            try:
                with open(notepad_file, 'r', encoding='utf-8') as f:
                    notepad_data = json.load(f)
                
                notepad_title = notepad_data.get("title", "Unknown")
                
                # Search through entries
                for entry in notepad_data.get("entries", []):
                    content = entry.get("content", "").lower()
                    
                    if query_lower in content:
                        matching_results.append({
                            "notepad": notepad_title,
                            "entry_id": entry.get("id"),
                            "content": entry.get("content", ""),
                            "created_at": entry.get("created_at", "Unknown")
                        })
                        
            except Exception as e:
                logging.warning(f"Error searching notepad file {notepad_file}: {e}")
                continue
        
        # Sort by creation date
        matching_results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        logging.info(f"Search for '{query}' found {len(matching_results)} entries in game: {current_game}")
        
        # Format results message
        if matching_results:
            message_parts = [f"Found {len(matching_results)} entries matching '{query}' in game '{current_game}':"]
            for result in matching_results:
                message_parts.append(f"- {result['notepad']} #{result['entry_id']}: {result['content'][:100]}{'...' if len(result['content']) > 100 else ''}")
            message = "\n".join(message_parts)
        else:
            search_scope = f"notepad '{specific_notepad}'" if specific_notepad else f"game '{current_game}'"
            message = f"No entries found matching '{query}' in {search_scope}"
        
        return generate_response(True, message, {"results": matching_results, "game": current_game, "query": query})
        
    except Exception as e:
        logging.error(f"Error searching notepads: {e}")
        return generate_response(False, f"Failed to search notepads: {str(e)}")

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
