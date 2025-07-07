import json
import os
import platform
import time
from pathlib import Path
from typing import Any

from .constants import DEFAULT_SAVE_SLOTS, SAVE_FILE_EXTENSION, SAVE_SLOT_PREFIX

MANUAL_SAVE_SLOTS = DEFAULT_SAVE_SLOTS


def get_default_save_path() -> str:
    """Get the default save path based on the operating system."""
    system = platform.system()

    if system == "Windows":
        # Windows: Use %APPDATA%
        appdata = os.environ.get("APPDATA")
        if appdata:
            return str(Path(appdata) / "2048-cli" / "saves")
        else:
            return str(Path.home() / "AppData" / "Roaming" / "2048-cli" / "saves")

    elif system == "Darwin":  # macOS
        # macOS: Use ~/Library/Application Support
        return str(
            Path.home() / "Library" / "Application Support" / "2048-cli" / "saves"
        )

    else:  # Linux and other Unix-like systems
        # Linux: Use XDG_DATA_HOME or ~/.local/share
        xdg_data_home = os.environ.get("XDG_DATA_HOME")
        if xdg_data_home:
            return str(Path(xdg_data_home) / "2048-cli" / "saves")
        else:
            return str(Path.home() / ".local" / "share" / "2048-cli" / "saves")


def get_save_dir(config: dict[str, Any] | None = None) -> str:
    """Get the save directory from config or use default."""
    if config and "save_path" in config:
        return config["save_path"]

    # Check for legacy saves directory for backward compatibility
    legacy_path = "saves"
    if os.path.exists(legacy_path) and os.listdir(legacy_path):
        return legacy_path

    return get_default_save_path()


def ensure_save_dir_exists(save_dir: str) -> bool:
    """Ensure the save directory exists. Returns True if successful, False otherwise."""
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        return True
    except (OSError, PermissionError):
        # Failed to create directory
        return False
    except Exception:
        # Any other unexpected error
        return False


def save_game(
    game: Any, slot: int, name: str | None = None, config: dict[str, Any] | None = None
) -> bool:
    """Save game to specified slot. Returns True if successful, False otherwise."""
    try:
        save_dir = get_save_dir(config)
        if not ensure_save_dir_exists(save_dir):
            return False
        file_path = os.path.join(
            save_dir, f"{SAVE_SLOT_PREFIX}{slot}{SAVE_FILE_EXTENSION}"
        )

        # Load existing data to preserve name if not provided
        existing_name = None
        if name is None and os.path.exists(file_path):
            try:
                with open(file_path) as f:
                    existing_data = json.load(f)
                    existing_name = existing_data.get("name")
            except (OSError, json.JSONDecodeError, PermissionError):
                # If we can't read the existing file, just continue without the name
                pass

        data = {
            "grid": game.board.grid,
            "score": game.score,
            "game_over": game.game_over,
            "endless_mode": getattr(game, "endless_mode", False),
            "name": name or existing_name or f"Save {slot}",
        }

        # Write the save file with error handling
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        return True

    except (OSError, PermissionError, json.JSONEncodeError):
        # Log the error or handle it appropriately
        # For now, we silently fail but return False to indicate failure
        return False
    except Exception:
        # Catch any other unexpected errors
        return False


def load_game(game: Any, slot: int, config: dict[str, Any] | None = None) -> bool:
    """Load game from specified slot. Returns True if successful, False otherwise."""
    try:
        save_dir = get_save_dir(config)
        file_path = os.path.join(
            save_dir, f"{SAVE_SLOT_PREFIX}{slot}{SAVE_FILE_EXTENSION}"
        )
        if not os.path.exists(file_path):
            return False

        with open(file_path) as f:
            data = json.load(f)

        # Validate that required keys exist in the loaded data
        required_keys = ["grid", "score", "game_over"]
        for key in required_keys:
            if key not in data:
                return False

        # Validate grid structure
        grid = data["grid"]
        if not isinstance(grid, list) or len(grid) != game.board.size:
            return False
        for row in grid:
            if not isinstance(row, list) or len(row) != game.board.size:
                return False
            for cell in row:
                if not isinstance(cell, int) or cell < 0:
                    return False

        # Apply the loaded data
        game.board.grid = data["grid"]
        game.score = data["score"]
        game.game_over = data["game_over"]
        game.endless_mode = data.get("endless_mode", False)

        # If loading a game over save that has won (2048+), enable endless mode
        if game.game_over and game.has_won():
            game.enable_endless_mode()

        return True

    except (
        OSError,
        PermissionError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ):
        # File access, parsing, or data validation errors
        return False
    except Exception:
        # Any other unexpected errors
        return False


def get_save_slots(config: dict[str, Any] | None = None) -> list[str]:
    """Get list of save slot files. Returns empty list if directory can't be accessed."""
    try:
        save_dir = get_save_dir(config)
        if not ensure_save_dir_exists(save_dir):
            return []
        files = os.listdir(save_dir)
        return [
            f
            for f in files
            if f.startswith(SAVE_SLOT_PREFIX) and f.endswith(SAVE_FILE_EXTENSION)
        ]
    except (OSError, PermissionError):
        # Can't access the directory
        return []
    except Exception:
        # Any other unexpected errors
        return []


def get_save_slot_info(
    slot: int, config: dict[str, Any] | None = None
) -> dict[str, Any] | None:
    """Get save slot information including score and game status."""
    try:
        save_dir = get_save_dir(config)
        file_path = os.path.join(
            save_dir, f"{SAVE_SLOT_PREFIX}{slot}{SAVE_FILE_EXTENSION}"
        )
        if not os.path.exists(file_path):
            return None

        with open(file_path) as f:
            data = json.load(f)

        # Get modification time
        mod_time = os.path.getmtime(file_path)
        date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mod_time))

        return {
            "score": data.get("score", 0),
            "game_over": data.get("game_over", False),
            "date": date_str,
            "slot": slot,
            "name": data.get("name", f"Save {slot}"),
        }
    except (json.JSONDecodeError, KeyError, OSError, PermissionError, ValueError):
        # File access, parsing, or time formatting errors
        return None
    except Exception:
        # Any other unexpected errors
        return None


def get_all_save_slots_info(
    config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Get information for all save slots. Returns empty list if unable to access files."""
    try:
        slots_info = []
        files = get_save_slots(config)

        for file in files:
            # Extract slot number from filename
            try:
                # Remove prefix and extension to get slot number
                filename_without_prefix = file[len(SAVE_SLOT_PREFIX) :]
                slot_num = int(filename_without_prefix.split(".")[0])
                info = get_save_slot_info(slot_num, config)
                if info:
                    slots_info.append(info)
            except (ValueError, IndexError):
                # Skip files with invalid names
                continue

        # Sort by slot number
        slots_info.sort(key=lambda x: x["slot"])
        return slots_info
    except Exception:
        # Any unexpected errors
        return []
