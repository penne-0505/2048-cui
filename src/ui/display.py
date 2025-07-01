import curses

# Tile colors based on value
COLORS = {
    0: 235,  # Dark grey for empty tiles
    2: 253,  # Light grey
    4: 229,  # Light yellow
    8: 185,  # Green
    16: 143,  # Cyan
    32: 135,  # Blue
    64: 99,  # Magenta
    128: 220,  # Yellow
    256: 214,  # Orange
    512: 208,  # Dark Orange
    1024: 202,  # Red
    2048: 196,  # Dark Red
}


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    for value, color_code in COLORS.items():
        curses.init_pair(value, color_code, -1)


def draw_board(stdscr, game):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Title and Score
    score_text = f"Score: {game.score}"
    stdscr.addstr(0, 1, "2048-CLI")
    stdscr.addstr(0, width - len(score_text) - 1, score_text)

    # Board
    board_height = game.board.size * 2 + 1
    board_width = game.board.size * 4 + 1
    start_y = (height - board_height) // 2
    start_x = (width - board_width) // 2

    for r in range(game.board.size):
        for c in range(game.board.size):
            value = game.board.grid[r][c]
            color = curses.color_pair(value if value in COLORS else 2048)
            tile_str = f"{value:^4}"
            stdscr.addstr(start_y + r * 2 + 1, start_x + c * 4 + 1, tile_str, color)

    # Borders
    for r in range(board_height):
        stdscr.addstr(start_y + r, start_x, "|")
        stdscr.addstr(start_y + r, start_x + board_width - 1, "|")
    for c in range(board_width):
        stdscr.addstr(start_y, start_x + c, "-")
        stdscr.addstr(start_y + board_height - 1, start_x + c, "-")

    if game.game_over:
        game_over_text = "Game Over!"
        stdscr.addstr(height // 2, (width - len(game_over_text)) // 2, game_over_text)

    stdscr.refresh()
