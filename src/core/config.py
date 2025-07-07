import curses
import json
import os
from typing import Any

from .constants import CONFIG_FILENAME

CONFIG_FILE = CONFIG_FILENAME

# Default key mappings
DEFAULT_CONFIG = {
    "keys": {
        "movement": {
            "up": ["KEY_UP", "w"],
            "down": ["KEY_DOWN", "s"],
            "left": ["KEY_LEFT", "a"],
            "right": ["KEY_RIGHT", "d"],
        },
        "actions": {
            "quit": ["q", "ESC"],
            "save": ["h"],
            "return_to_title": ["r"],
            "load": ["l"],
            "change_theme": ["t"],
        },
    },
    "theme": "modern",
    "save_path": None,  # None means use default path
}


def load_config() -> dict[str, Any]:
    """Load configuration from file or create default if not exists."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
            # Validate that config has required structure
            if isinstance(config, dict) and "keys" in config:
                return config
        except (OSError, json.JSONDecodeError, PermissionError):
            # If we can't read or parse the config file, fall back to default
            pass

    # Create default config file
    if save_config(DEFAULT_CONFIG):
        return DEFAULT_CONFIG
    else:
        # If we can't save the config file, just return the default in memory
        return DEFAULT_CONFIG.copy()


def save_config(config: dict[str, Any]) -> bool:
    """Save configuration to file. Returns True if successful, False otherwise."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except (OSError, PermissionError, json.JSONDecodeError):
        # File access or JSON encoding errors
        return False
    except Exception:
        # Any other unexpected errors
        return False


def get_theme(config: dict[str, Any]) -> str:
    """Get the current theme name from config."""
    return config.get("theme", "modern")


def set_theme(config: dict[str, Any], theme_name: str) -> bool:
    """Set the theme in config and save. Returns True if successful."""
    config["theme"] = theme_name
    return save_config(config)


def get_save_path(config: dict[str, Any]) -> str | None:
    """Get the custom save path from config."""
    return config.get("save_path")


def set_save_path(config: dict[str, Any], save_path: str | None) -> bool:
    """Set the save path in config and save. Returns True if successful."""
    config["save_path"] = save_path
    return save_config(config)


def get_key_codes(
    config: dict[str, Any],
) -> tuple[dict[int, str], dict[str, list[int]]]:
    """Convert string key names to curses key codes."""
    key_map = {}

    # Movement keys
    for direction, keys in config["keys"]["movement"].items():
        for key in keys:
            if key.startswith("KEY_"):
                key_code = getattr(curses, key)
            else:
                key_code = ord(key)
            key_map[key_code] = direction

    # Action keys
    action_keys = {}
    for action, keys in config["keys"]["actions"].items():
        action_keys[action] = []
        for key in keys:
            if key == "ESC":
                action_keys[action].append(27)
            elif key.startswith("KEY_"):
                action_keys[action].append(getattr(curses, key))
            else:
                action_keys[action].append(ord(key))

    return key_map, action_keys
