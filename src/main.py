import curses
import random
import time

from core.config import get_key_codes, load_config
from core.save_load import load_game, save_game
from core.constants import (
    INITIAL_TILE_VALUE,
    SPECIAL_TILE_VALUE,
    SCORE_THRESHOLD_FOR_SPECIAL_TILES,
    BASE_CHANCE_OF_4,
    CHANCE_INCREASE_RATE,
    CHANCE_SCORE_INTERVAL
)
from game.game import Game
from ui.menu import show_load_menu, show_save_menu, show_start_menu
from ui.key_config_menu import show_key_config_menu
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

        if choice == "key_config":
            show_key_config_menu(stdscr, config)
            # Reload key mappings after configuration change
            key_map, action_keys = get_key_codes(config)
            continue

        game = Game()

        if choice == "new":
            game.start()
        elif choice == "load":
            slot = show_load_menu(stdscr, config)
            if slot is None or not load_game(game, slot, config):
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
                    success = save_game(game, slot, name, config)
                    # TODO: Show save confirmation/error message to user
                    # For now, we silently handle the success/failure
                continue

            if key in action_keys.get("load", []):  # Load game
                slot = show_load_menu(stdscr, config)
                if slot is not None and load_game(game, slot, config):
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
                    if score < SCORE_THRESHOLD_FOR_SPECIAL_TILES:
                        game.board.place_new_tile(INITIAL_TILE_VALUE)
                    else:
                        chance_of_4 = min(
                            BASE_CHANCE_OF_4, 
                            (score - SCORE_THRESHOLD_FOR_SPECIAL_TILES) // CHANCE_SCORE_INTERVAL * CHANCE_INCREASE_RATE
                        )
                        if random.random() < chance_of_4:
                            game.board.place_new_tile(SPECIAL_TILE_VALUE)
                        else:
                            game.board.place_new_tile(INITIAL_TILE_VALUE)

                # Check for game over
                if game.is_game_over():
                    game.game_over = True


if __name__ == "__main__":
    curses.wrapper(main)
