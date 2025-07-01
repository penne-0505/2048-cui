import json
import os

SAVE_DIR = "saves"
MANUAL_SAVE_SLOTS = 5


def ensure_save_dir_exists():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def save_game(game, slot, name=None):
    ensure_save_dir_exists()
    file_path = os.path.join(SAVE_DIR, f"slot_{slot}.json")

    # Load existing data to preserve name if not provided
    existing_name = None
    if name is None and os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                existing_data = json.load(f)
                existing_name = existing_data.get("name")
        except (json.JSONDecodeError, IOError):
            pass

    data = {
        "grid": game.board.grid,
        "score": game.score,
        "game_over": game.game_over,
        "endless_mode": getattr(game, "endless_mode", False),
        "name": name or existing_name or f"Save {slot}",
    }
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def load_game(game, slot):
    file_path = os.path.join(SAVE_DIR, f"slot_{slot}.json")
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r") as f:
        data = json.load(f)

    game.board.grid = data["grid"]
    game.score = data["score"]
    game.game_over = data["game_over"]
    game.endless_mode = data.get("endless_mode", False)

    # If loading a game over save that has won (2048+), enable endless mode
    if game.game_over and game.has_won():
        game.enable_endless_mode()

    return True


def get_save_slots():
    ensure_save_dir_exists()
    files = os.listdir(SAVE_DIR)
    return [f for f in files if f.startswith("slot_") and f.endswith(".json")]


def get_save_slot_info(slot):
    """Get save slot information including score and game status."""
    file_path = os.path.join(SAVE_DIR, f"slot_{slot}.json")
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        # Get modification time
        mod_time = os.path.getmtime(file_path)
        import time

        date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mod_time))

        return {
            "score": data.get("score", 0),
            "game_over": data.get("game_over", False),
            "date": date_str,
            "slot": slot,
            "name": data.get("name", f"Save {slot}"),
        }
    except (json.JSONDecodeError, KeyError):
        return None


def get_all_save_slots_info():
    """Get information for all save slots."""
    slots_info = []
    files = get_save_slots()

    for file in files:
        # Extract slot number from filename
        try:
            slot_num = int(file.split("_")[1].split(".")[0])
            info = get_save_slot_info(slot_num)
            if info:
                slots_info.append(info)
        except (ValueError, IndexError):
            continue

    # Sort by slot number
    slots_info.sort(key=lambda x: x["slot"])
    return slots_info
