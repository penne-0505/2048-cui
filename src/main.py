import curses
import random

from src.core.save_load import load_game, save_game
from src.game.game import Game
from src.ui.display import draw_board, init_colors
from src.ui.menu import show_load_menu, show_save_menu, show_start_menu

AUTO_SAVE_SLOT = 0
MANUAL_SAVE_SLOTS = 5

KEY_MAP = {
    curses.KEY_UP: "up",
    ord("w"): "up",
    curses.KEY_DOWN: "down",
    ord("s"): "down",
    curses.KEY_LEFT: "left",
    ord("a"): "left",
    curses.KEY_RIGHT: "right",
    ord("d"): "right",
}


def main(stdscr):
    curses.curs_set(0)
    init_colors()

    # Game start menu
    choice = show_start_menu(stdscr)
    if choice is None:  # User quit from start menu
        return

    game = Game()

    if choice == "new":
        game.start()
    elif choice == "load":
        slot = show_load_menu(stdscr)
        if slot is None or not load_game(game, slot):
            # Fallback to new game if load fails or user quits load menu
            game.start()

    while not game.game_over:
        # Auto-save every turn
        save_game(game, AUTO_SAVE_SLOT)

        draw_board(stdscr, game)
        key = stdscr.getch()

        if key in [ord("q"), 27]:  # Quit on 'q' or ESC
            break

        if key == ord("p"):  # Manual save
            slot = show_save_menu(stdscr)
            if slot is not None:
                save_game(game, slot)
                # Optional: Add a message to confirm save
            continue

        if key in KEY_MAP:
            direction = KEY_MAP[key]
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
