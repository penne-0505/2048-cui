import curses
import json
import os

CONFIG_FILE = "config.json"

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
}


def load_config():
    """Load configuration from file or create default if not exists."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            return config
        except (json.JSONDecodeError, IOError):
            pass

    # Create default config file
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG


def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_theme(config):
    """Get the current theme name from config."""
    return config.get("theme", "modern")


def set_theme(config, theme_name):
    """Set the theme in config and save."""
    config["theme"] = theme_name
    save_config(config)


def get_key_codes(config):
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
