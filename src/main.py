import curses
import random

from core.config import get_key_codes, load_config
from core.save_load import load_game, save_game
from game.game import Game
from ui.menu import show_load_menu, show_save_menu, show_start_menu
from ui.modern_display import draw_board, init_colors

AUTO_SAVE_SLOT = 0
MANUAL_SAVE_SLOTS = 5


def main(stdscr: curses.window) -> None:
    curses.curs_set(0)

    # Load configuration
    config = load_config()
    init_colors()  # Modern display uses fixed modern theme
    key_map, action_keys = get_key_codes(config)

    while True:  # Main application loop
        # Game start menu
        choice = show_start_menu(stdscr)
        if choice is None:  # User quit from start menu
            break

        game = Game()

        if choice == "new":
            game.start()
        elif choice == "load":
            slot = show_load_menu(stdscr)
            if slot is None or not load_game(game, slot):
                # Fallback to new game if load fails or user quits load menu
                game.start()

        # Game loop
        return_to_title = False
        while not game.game_over and not return_to_title:
            draw_board(stdscr, game, config)
            key = stdscr.getch()

            if key in action_keys.get("quit", []):  # Quit application
                return

            if key in action_keys.get("return_to_title", []):  # Return to title
                return_to_title = True
                continue

            if key in action_keys.get("save", []):  # Manual save
                result = show_save_menu(stdscr)
                if result is not None:
                    slot, name = result
                    save_game(game, slot, name)
                    # Optional: Add a message to confirm save
                continue

            if key in action_keys.get("load", []):  # Load game
                slot = show_load_menu(stdscr)
                if slot is not None and load_game(game, slot):
                    # Game loaded successfully, continue with loaded state
                    pass
                continue

            if key in action_keys.get("change_theme", []):  # Theme cycling disabled
                continue  # Skip - modern design uses fixed theme

            if key in key_map:
                direction = key_map[key]
                if game.move(direction):
                    # Add new tile based on score
                    score = game.score
                    if score < 2000:
                        game.board.place_new_tile(2)
                    else:
                        chance_of_4 = min(0.5, (score - 2000) // 2000 * 0.05)
                        if random.random() < chance_of_4:
                            game.board.place_new_tile(4)
                        else:
                            game.board.place_new_tile(2)

                # Check for game over
                if game.is_game_over():
                    game.game_over = True


if __name__ == "__main__":
    curses.wrapper(main)
