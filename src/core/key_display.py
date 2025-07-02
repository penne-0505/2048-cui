"""
Key display name mapping and formatting utilities.
This module automatically generates human-readable key descriptions from config.
"""

from typing import Any

# Mapping of action keys to display names
ACTION_DISPLAY_NAMES = {
    "quit": "Quit",
    "save": "Save",
    "return_to_title": "Return to Title",
    "load": "Load Game",
    "change_theme": "Change Theme",
    "pause": "Pause",
    "restart": "Restart",
    "help": "Help",
    "menu": "Menu",
}

# Mapping of movement keys to display names
MOVEMENT_DISPLAY_NAMES = {"up": "Up", "down": "Down", "left": "Left", "right": "Right"}

# Mapping of special key names for display
KEY_DISPLAY_MAPPING = {
    "KEY_UP": "↑",
    "KEY_DOWN": "↓",
    "KEY_LEFT": "←",
    "KEY_RIGHT": "→",
    "KEY_ENTER": "Enter",
    "ESC": "Esc",
    "SPACE": "Space",
}


def get_action_display_name(action_key: str) -> str:
    """Get human-readable display name for an action key."""
    return ACTION_DISPLAY_NAMES.get(action_key, action_key.replace("_", " ").title())


def get_movement_display_name(movement_key: str) -> str:
    """Get human-readable display name for a movement key."""
    return MOVEMENT_DISPLAY_NAMES.get(movement_key, movement_key.capitalize())


def format_key_for_display(key: str) -> str:
    """Format a key name for display (e.g., KEY_UP -> ↑)."""
    return KEY_DISPLAY_MAPPING.get(key, key.upper())


def format_key_list_for_display(keys: list[str]) -> str:
    """Format a list of keys for display with proper separators."""
    formatted_keys = [format_key_for_display(key) for key in keys]
    return "/".join(formatted_keys)


def generate_cheatsheet_data(config: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    """Generate cheatsheet data from config automatically."""
    cheatsheet = {"movement": [], "actions": []}

    # Process movement keys
    if "movement" in config["keys"]:
        for direction, keys in config["keys"]["movement"].items():
            display_name = get_movement_display_name(direction)
            key_display = format_key_list_for_display(keys)
            cheatsheet["movement"].append({"name": display_name, "keys": key_display})

    # Process action keys
    if "actions" in config["keys"]:
        for action, keys in config["keys"]["actions"].items():
            display_name = get_action_display_name(action)
            key_display = format_key_list_for_display(keys)
            cheatsheet["actions"].append({"name": display_name, "keys": key_display})

    return cheatsheet
