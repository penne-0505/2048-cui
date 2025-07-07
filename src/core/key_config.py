import curses
from typing import Dict, List, Set, Tuple, Optional, Any

from .constants import (
    ESCAPE_KEY_CODE,
    SPACE_KEY_CODE,
    ASCII_PRINTABLE_START,
    ASCII_PRINTABLE_END
)

# Whitelist of safe bindable keys for security
SAFE_BINDABLE_KEYS = {
    # Letters
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    
    # Numbers
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    
    # Arrow keys
    'KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT',
    
    # Function keys
    'KEY_F1', 'KEY_F2', 'KEY_F3', 'KEY_F4', 'KEY_F5', 'KEY_F6',
    'KEY_F7', 'KEY_F8', 'KEY_F9', 'KEY_F10', 'KEY_F11', 'KEY_F12',
    
    # Navigation keys
    'KEY_HOME', 'KEY_END', 'KEY_PPAGE', 'KEY_NPAGE',
    
    # Safe special keys
    'KEY_ENTER', 'KEY_BACKSPACE', 'KEY_DELETE', 'KEY_INSERT',
    'ESC', 'SPACE',
    
    # Safe punctuation
    ',', '.', '/', ';', "'", '[', ']', '\\', '=', '-',
    '`', '~', '!', '@', '#', '$', '%', '^', '&', '*',
    '(', ')', '_', '+', '{', '}', '|', ':', '"', '<', '>', '?'
}

# Human-readable names for special keys
KEY_DISPLAY_NAMES = {
    'KEY_UP': '↑',
    'KEY_DOWN': '↓',
    'KEY_LEFT': '←',
    'KEY_RIGHT': '→',
    'KEY_ENTER': 'Enter',
    'KEY_BACKSPACE': 'Backspace',
    'KEY_DELETE': 'Delete',
    'KEY_INSERT': 'Insert',
    'KEY_HOME': 'Home',
    'KEY_END': 'End',
    'KEY_PPAGE': 'Page Up',
    'KEY_NPAGE': 'Page Down',
    'ESC': 'Escape',
    'SPACE': 'Space',
    'KEY_F1': 'F1', 'KEY_F2': 'F2', 'KEY_F3': 'F3', 'KEY_F4': 'F4',
    'KEY_F5': 'F5', 'KEY_F6': 'F6', 'KEY_F7': 'F7', 'KEY_F8': 'F8',
    'KEY_F9': 'F9', 'KEY_F10': 'F10', 'KEY_F11': 'F11', 'KEY_F12': 'F12',
}


def is_key_safe(key: str) -> bool:
    """Check if a key is in the safe bindable keys whitelist."""
    return key in SAFE_BINDABLE_KEYS


def get_key_display_name(key: str) -> str:
    """Get human-readable display name for a key."""
    return KEY_DISPLAY_NAMES.get(key, key)


def key_to_code(key: str) -> int:
    """Convert a key string to curses key code."""
    if key == "ESC":
        return ESCAPE_KEY_CODE
    elif key == "SPACE":
        return SPACE_KEY_CODE
    elif key.startswith("KEY_"):
        return getattr(curses, key)
    else:
        return ord(key)


def code_to_key(code: int) -> str:
    """Convert curses key code to key string."""
    if code == ESCAPE_KEY_CODE:
        return "ESC"
    elif code == SPACE_KEY_CODE:
        return "SPACE"
    elif ASCII_PRINTABLE_START <= code <= ASCII_PRINTABLE_END:  # Printable ASCII
        return chr(code)
    else:
        # Check for special keys
        for key_name in dir(curses):
            if key_name.startswith('KEY_'):
                try:
                    if getattr(curses, key_name) == code:
                        return key_name
                except:
                    continue
        return f"UNKNOWN_{code}"


def validate_key_bindings(config: Dict[str, Any]) -> List[str]:
    """Validate key bindings and return list of errors."""
    errors = []
    used_keys = set()
    
    # Check movement keys
    for direction, keys in config["keys"]["movement"].items():
        for key in keys:
            if not is_key_safe(key):
                errors.append(f"Unsafe key '{key}' in movement.{direction}")
            if key in used_keys:
                errors.append(f"Key '{key}' is bound to multiple actions")
            used_keys.add(key)
    
    # Check action keys
    for action, keys in config["keys"]["actions"].items():
        for key in keys:
            if not is_key_safe(key):
                errors.append(f"Unsafe key '{key}' in actions.{action}")
            if key in used_keys:
                errors.append(f"Key '{key}' is bound to multiple actions")
            used_keys.add(key)
    
    return errors


def get_all_bound_keys(config: Dict[str, Any]) -> Set[str]:
    """Get all currently bound keys."""
    bound_keys = set()
    
    # Movement keys
    for keys in config["keys"]["movement"].values():
        bound_keys.update(keys)
    
    # Action keys
    for keys in config["keys"]["actions"].values():
        bound_keys.update(keys)
    
    return bound_keys


def get_available_keys(config: Dict[str, Any]) -> Set[str]:
    """Get all available (safe but unbound) keys."""
    bound_keys = get_all_bound_keys(config)
    return SAFE_BINDABLE_KEYS - bound_keys


def add_key_binding(config: Dict[str, Any], category: str, action: str, key: str) -> Tuple[bool, str]:
    """Add a key binding. Returns (success, error_message)."""
    if not is_key_safe(key):
        return False, f"Key '{key}' is not in the safe bindable keys list"
    
    # Check if key is already bound
    bound_keys = get_all_bound_keys(config)
    if key in bound_keys:
        return False, f"Key '{key}' is already bound to another action"
    
    # Add the key
    if category == "movement":
        if action not in config["keys"]["movement"]:
            return False, f"Unknown movement action: {action}"
        if key not in config["keys"]["movement"][action]:
            config["keys"]["movement"][action].append(key)
    elif category == "actions":
        if action not in config["keys"]["actions"]:
            return False, f"Unknown action: {action}"
        if key not in config["keys"]["actions"][action]:
            config["keys"]["actions"][action].append(key)
    else:
        return False, f"Unknown category: {category}"
    
    return True, ""


def remove_key_binding(config: Dict[str, Any], category: str, action: str, key: str) -> Tuple[bool, str]:
    """Remove a key binding. Returns (success, error_message)."""
    if category == "movement":
        if action not in config["keys"]["movement"]:
            return False, f"Unknown movement action: {action}"
        if key in config["keys"]["movement"][action]:
            config["keys"]["movement"][action].remove(key)
            # Don't allow empty key bindings
            if not config["keys"]["movement"][action]:
                return False, f"Cannot remove last key for {action}"
        else:
            return False, f"Key '{key}' is not bound to {action}"
    elif category == "actions":
        if action not in config["keys"]["actions"]:
            return False, f"Unknown action: {action}"
        if key in config["keys"]["actions"][action]:
            config["keys"]["actions"][action].remove(key)
            # Don't allow empty key bindings for critical actions
            if not config["keys"]["actions"][action] and action == "quit":
                return False, "Cannot remove last quit key"
        else:
            return False, f"Key '{key}' is not bound to {action}"
    else:
        return False, f"Unknown category: {category}"
    
    return True, ""


def get_action_display_name(category: str, action: str) -> str:
    """Get human-readable display name for an action."""
    display_names = {
        "movement": {
            "up": "Move Up",
            "down": "Move Down", 
            "left": "Move Left",
            "right": "Move Right"
        },
        "actions": {
            "quit": "Quit Game",
            "save": "Save Game",
            "return_to_title": "Return to Title",
            "load": "Load Game",
            "change_theme": "Change Theme"
        }
    }
    return display_names.get(category, {}).get(action, f"{category}.{action}")