import json
import os

SAVE_DIR = "saves"


def ensure_save_dir_exists():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def save_game(game, slot):
    ensure_save_dir_exists()
    file_path = os.path.join(SAVE_DIR, f"slot_{slot}.json")
    data = {"grid": game.board.grid, "score": game.score, "game_over": game.game_over}
    with open(file_path, "w") as f:
        json.dump(data, f)


def load_game(game, slot):
    file_path = os.path.join(SAVE_DIR, f"slot_{slot}.json")
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r") as f:
        data = json.load(f)

    game.board.grid = data["grid"]
    game.score = data["score"]
    game.game_over = data["game_over"]
    return True


def get_save_slots():
    ensure_save_dir_exists()
    files = os.listdir(SAVE_DIR)
    return [f for f in files if f.startswith("slot_") and f.endswith(".json")]
