#!/usr/bin/env python3
"""
Interactive Notepad Plugin Interface

This script provides an interactive command-line interface to test the notepad plugin
functionality. It simulates being G-Assist by sending JSON commands to the plugin
functions and displaying the responses in a user-friendly format.
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

# Add the plugin directory to the path so we can import the plugin
plugin_dir = Path(__file__).parent
sys.path.insert(0, str(plugin_dir))

# Mock the Windows-specific imports for testing
class MockWinDLL:
    def GetStdHandle(self, handle): return None
    def ReadFile(self, *args): return False
    def WriteFile(self, *args): return True

class MockWinTypes:
    class DWORD:
        def __init__(self): self.value = 0

# Mock ctypes for non-Windows testing
import ctypes
ctypes.windll = type('MockWindll', (), {'kernel32': MockWinDLL()})()
ctypes.wintypes = MockWinTypes()

# Now import the plugin
from plugin import (
    create_note, read_note, list_notes, delete_note, search_notes,
    initialize, shutdown, generate_response
)

class InteractiveNotepadInterface:
    """Interactive interface for testing the notepad plugin."""
    
    def __init__(self):
        self.current_game = "Test Game"
        self.running = True
        
    def print_header(self):
        """Print the application header."""
        print("🎮 G-Assist Notepad Plugin - Interactive Test Interface")
        print("=" * 60)
        print(f"Current Game: {self.current_game}")
        print("Type 'help' for available commands or 'quit' to exit")
        print("=" * 60)
        
    def print_help(self):
        """Print available commands."""
        print("\n📋 Available Commands:")
        print("━" * 40)
        print("🆕 add <notepad> <content>     - Add entry to notepad")
        print("📖 read <notepad>             - Read notepad entries")
        print("📝 list                       - List all notepads")
        print("🔍 search <query>             - Search entries")
        print("🗑️  delete <notepad>           - Delete notepad")
        print("🎮 game <name>                - Change current game")
        print("❓ help                       - Show this help")
        print("🚪 quit                       - Exit interface")
        print("\n💡 Examples:")
        print("   add Missions Kill 100 monsters for Prof Amy")
        print("   read Missions")
        print("   search Prof Amy")
        print("   game Cyberpunk 2077")
        print("━" * 40)
        
    def format_response(self, response: Dict[str, Any]) -> str:
        """Format a plugin response for display."""
        success = response.get('success', False)
        message = response.get('message', 'No message')
        
        if success:
            icon = "✅"
            status = "SUCCESS"
        else:
            icon = "❌"
            status = "ERROR"
            
        formatted = f"{icon} {status}: {message}"
        
        # Add additional data formatting for specific responses
        data = response.get('data')
        if data:
            if 'notepads' in data:
                notepads = data['notepads']
                if notepads:
                    formatted += "\n\n📚 Notepads:"
                    for notepad in notepads:
                        formatted += f"\n   • {notepad['title']}: {notepad['entry_count']} entries"
                        
            elif 'results' in data:
                results = data['results']
                if results:
                    formatted += "\n\n🔍 Search Results:"
                    for result in results[:5]:  # Limit to first 5 results
                        formatted += f"\n   • {result['notepad']} #{result['entry_id']}: {result['content'][:80]}{'...' if len(result['content']) > 80 else ''}"
                    if len(results) > 5:
                        formatted += f"\n   ... and {len(results) - 5} more results"
                        
            elif 'entries' in data:
                entries = data.get('entries', [])
                if entries:
                    formatted += "\n\n📋 Entries:"
                    for entry in entries:
                        formatted += f"\n   #{entry['id']}: {entry['content']}"
        
        return formatted
        
    def cmd_add(self, args: list) -> None:
        """Handle add command."""
        if len(args) < 2:
            print("❌ Usage: add <notepad> <content>")
            print("   Example: add Missions Kill 100 monsters for Prof Amy")
            return
            
        notepad = args[0]
        content = " ".join(args[1:])
        
        params = {
            "title": notepad,
            "content": content,
            "current_game": self.current_game
        }
        
        print(f"🔄 Adding entry to '{notepad}' notepad...")
        response = create_note(params)
        print(self.format_response(response))
        
    def cmd_read(self, args: list) -> None:
        """Handle read command."""
        if len(args) != 1:
            print("❌ Usage: read <notepad>")
            print("   Example: read Missions")
            return
            
        notepad = args[0]
        params = {
            "title": notepad,
            "current_game": self.current_game
        }
        
        print(f"🔄 Reading '{notepad}' notepad...")
        response = read_note(params)
        print(self.format_response(response))
        
    def cmd_list(self, args: list) -> None:
        """Handle list command."""
        params = {
            "current_game": self.current_game
        }
        
        print(f"🔄 Listing notepads for '{self.current_game}'...")
        response = list_notes(params)
        print(self.format_response(response))
        
    def cmd_search(self, args: list) -> None:
        """Handle search command."""
        if len(args) < 1:
            print("❌ Usage: search <query>")
            print("   Example: search Prof Amy")
            return
            
        query = " ".join(args)
        params = {
            "query": query,
            "current_game": self.current_game
        }
        
        print(f"🔄 Searching for '{query}'...")
        response = search_notes(params)
        print(self.format_response(response))
        
    def cmd_delete(self, args: list) -> None:
        """Handle delete command."""
        if len(args) != 1:
            print("❌ Usage: delete <notepad>")
            print("   Example: delete Missions")
            return
            
        notepad = args[0]
        
        # Confirm deletion
        confirm = input(f"⚠️  Are you sure you want to delete the '{notepad}' notepad? (y/N): ")
        if confirm.lower() != 'y':
            print("🚫 Deletion cancelled")
            return
            
        params = {
            "title": notepad,
            "current_game": self.current_game
        }
        
        print(f"🔄 Deleting '{notepad}' notepad...")
        response = delete_note(params)
        print(self.format_response(response))
        
    def cmd_game(self, args: list) -> None:
        """Handle game command."""
        if len(args) < 1:
            print("❌ Usage: game <name>")
            print("   Example: game Cyberpunk 2077")
            return
            
        new_game = " ".join(args)
        old_game = self.current_game
        self.current_game = new_game
        
        print(f"🎮 Changed game from '{old_game}' to '{new_game}'")
        
    def cmd_help(self, args: list) -> None:
        """Handle help command."""
        self.print_help()
        
    def cmd_quit(self, args: list) -> None:
        """Handle quit command."""
        print("👋 Goodbye!")
        self.running = False
        
    def process_command(self, command_line: str) -> None:
        """Process a user command."""
        parts = command_line.strip().split()
        if not parts:
            return
            
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Map commands to methods
        commands = {
            'add': self.cmd_add,
            'read': self.cmd_read,
            'list': self.cmd_list,
            'search': self.cmd_search,
            'delete': self.cmd_delete,
            'game': self.cmd_game,
            'help': self.cmd_help,
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
        }
        
        if cmd in commands:
            try:
                commands[cmd](args)
            except Exception as e:
                print(f"❌ Error executing command: {e}")
        else:
            print(f"❌ Unknown command: {cmd}")
            print("Type 'help' for available commands")
            
    def setup_demo_data(self) -> None:
        """Set up some demo data for testing."""
        print("🔄 Setting up demo data...")
        
        # Initialize plugin
        initialize()
        
        # Add some sample entries
        demo_entries = [
            ("Missions", "Kill 100 lv2 monsters and report back to Prof Amy"),
            ("Missions", "Collect 50 cybernetic implants from corpo district"),
            ("Missions", "Infiltrate Arasaka Tower and steal data chip"),
            ("Characters", "Prof Amy teaches cybernetics at Night City University"),
            ("Characters", "Johnny Silverhand - legendary rockerboy and anti-corp terrorist"),
            ("Characters", "Viktor Vector - underground ripperdoc in Watson district"),
            ("Locations", "Night City - sprawling metropolis dominated by corporations"),
            ("Locations", "Watson District - working-class area with many small businesses"),
            ("Inventory", "Mantis Blades - cybernetic arm weapons for close combat"),
            ("Inventory", "Sandevistan - time dilation cyberware implant"),
        ]
        
        for notepad, content in demo_entries:
            params = {
                "title": notepad,
                "content": content,
                "current_game": self.current_game
            }
            create_note(params)
            
        print("✅ Demo data created successfully!")
        print("Try commands like: 'list', 'read Missions', 'search Prof Amy'")
        
    def run(self):
        """Run the interactive interface."""
        self.print_header()
        
        # Ask if user wants demo data
        setup_demo = input("\n🎲 Would you like to set up demo data? (Y/n): ")
        if setup_demo.lower() != 'n':
            self.setup_demo_data()
            
        print("\n" + "=" * 60)
        
        try:
            while self.running:
                try:
                    command = input(f"\n🎮 [{self.current_game}] > ")
                    if command.strip():
                        self.process_command(command)
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    break
                except EOFError:
                    print("\n\n👋 Goodbye!")
                    break
                    
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            
def main():
    """Main entry point."""
    interface = InteractiveNotepadInterface()
    interface.run()

if __name__ == "__main__":
    main()
