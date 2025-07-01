"""
Modern minimalist display system for 2048-CLI.
Based on mm.png design - clean, floating tiles, minimal UI.
"""

import curses

from core.modern_themes import (
    get_tile_color_pair,
    get_ui_color_pairs,
    init_modern_colors,
)


def init_display():
    """Initialize the modern display system."""
    init_modern_colors()


def draw_modern_game(stdscr, game, config=None):
    """
    Draw the game using modern minimalist design.

    Layout:
    - Top: Score and score change
    - Center: 4x4 floating tile grid
    - Bottom: Simple controls
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    ui_colors = get_ui_color_pairs()

    # Draw header (score)
    draw_score_header(stdscr, game, ui_colors, width)

    # Calculate board position (centered) for bordered tiles
    board_start_y = 4  # Leave space for header
    board_width = 30  # 4 tiles * 6 chars + 3 gaps * 2 chars = 24 + 6 = 30
    # Center the board properly
    board_start_x = max(2, (width - board_width) // 2)

    # Draw floating tile grid
    draw_floating_tiles(stdscr, game, board_start_y, board_start_x)

    # Draw footer controls
    draw_simple_controls(stdscr, ui_colors, height, width)

    # Game over overlay if needed
    if game.game_over:
        draw_game_over(stdscr, ui_colors, height, width)

    stdscr.refresh()


def draw_score_header(stdscr, game, ui_colors, width):
    """Draw score display with total on top-right and history below."""
    try:
        # Game title on top-left
        title = "2048-CLI"
        if getattr(game, "endless_mode", False):
            title += " [ENDLESS]"
        stdscr.addstr(
            1, 2, title, curses.color_pair(ui_colors["controls"]) | curses.A_BOLD
        )

        # Main score on top-right
        score_text = f"Score: {game.score}"
        score_x = width - len(score_text) - 2
        stdscr.addstr(
            1,
            score_x,
            score_text,
            curses.color_pair(ui_colors["score"]) | curses.A_BOLD,
        )

        # Score history below main score (descending order)
        draw_score_history(stdscr, game, ui_colors, width)

    except curses.error:
        # Fallback for narrow screens
        stdscr.addstr(0, 0, f"Score: {game.score}")


def draw_score_history(stdscr, game, ui_colors, width):
    """Draw recent score additions in descending order."""
    score_history = getattr(game, "_score_history", [])

    if not score_history:
        return

    import time

    current_time = time.time()

    # Filter recent changes (last 10 seconds) and sort by time (newest first)
    recent_changes = [
        change for change in score_history if current_time - change["time"] < 10.0
    ]
    recent_changes.sort(key=lambda x: x["time"], reverse=True)

    # Display up to 4 recent score changes
    for i, change in enumerate(recent_changes[:4]):
        if i >= 4:  # Limit to 4 lines
            break

        # Calculate fade effect based on age
        age = current_time - change["time"]
        if age < 2.0:
            # Recent - bright
            color = curses.color_pair(ui_colors["score_accent"]) | curses.A_BOLD
        elif age < 5.0:
            # Medium - normal
            color = curses.color_pair(ui_colors["score_accent"])
        else:
            # Old - dim
            color = curses.color_pair(ui_colors["controls"])

        # Position and display
        change_text = f"+{change['points']}"
        change_x = width - len(change_text) - 2
        change_y = 3 + i  # Start from line 3, go down (adds spacing below main score)

        try:
            stdscr.addstr(change_y, change_x, change_text, color)
        except curses.error:
            break  # Stop if we run out of screen space


def draw_floating_tiles(stdscr, game, start_y, start_x):
    """Draw 4x4 grid of floating tiles with borders."""
    for row in range(4):
        for col in range(4):
            tile_value = game.board.grid[row][col]

            # Calculate tile position for bordered tiles
            tile_y = start_y + row * 4  # 4 lines per tile (3 content + 1 spacing)
            tile_x = start_x + col * 8  # 8 chars per tile (6 content + 2 spacing)

            draw_single_tile(stdscr, tile_value, tile_y, tile_x)


def draw_single_tile(stdscr, value, y, x):
    """Draw a single tile with border outline."""
    color_pair = get_tile_color_pair(value)

    if value == 0:
        # Empty tile - subtle border outline
        try:
            stdscr.addstr(y, x, "╭────╮", curses.color_pair(color_pair))
            stdscr.addstr(y + 1, x, "│    │", curses.color_pair(color_pair))
            stdscr.addstr(y + 2, x, "╰────╯", curses.color_pair(color_pair))
        except curses.error:
            pass
    else:
        # Tile with value - bordered box with centered number
        value_str = str(value)
        padding = (4 - len(value_str)) // 2
        left_pad = " " * padding
        right_pad = " " * (4 - len(value_str) - padding)

        middle_content = f"│{left_pad}{value_str}{right_pad}│"

        try:
            # Top border
            stdscr.addstr(y, x, "╭────╮", curses.color_pair(color_pair))
            # Middle with value
            stdscr.addstr(
                y + 1, x, middle_content, curses.color_pair(color_pair) | curses.A_BOLD
            )
            # Bottom border
            stdscr.addstr(y + 2, x, "╰────╯", curses.color_pair(color_pair))
        except curses.error:
            pass


def draw_simple_controls(stdscr, ui_colors, height, width):
    """Draw minimal control information at bottom."""
    controls = ["Back/Restart", "↑ ← ↓ →", "Quit"]

    # Position controls at bottom, accounting for bordered tile height
    control_y = height - 4

    try:
        # Left control
        stdscr.addstr(
            control_y, 2, controls[0], curses.color_pair(ui_colors["controls"])
        )

        # Center arrows
        center_x = (width - len(controls[1])) // 2
        stdscr.addstr(
            control_y, center_x, controls[1], curses.color_pair(ui_colors["controls"])
        )

        # Right control
        right_x = width - len(controls[2]) - 2
        stdscr.addstr(
            control_y, right_x, controls[2], curses.color_pair(ui_colors["controls"])
        )

        # Additional controls on next line
        control_y += 1
        extras = "r: Return   h: Save   l: Load   t: Theme"
        if len(extras) < width - 4:
            extra_x = (width - len(extras)) // 2
            stdscr.addstr(
                control_y, extra_x, extras, curses.color_pair(ui_colors["controls"])
            )

    except curses.error:
        pass


def draw_game_over(stdscr, ui_colors, height, width):
    """Draw game over overlay."""
    message = "Game Over!"

    try:
        msg_x = (width - len(message)) // 2
        msg_y = height // 2

        # Clear area around message
        clear_line = " " * len(message)
        stdscr.addstr(msg_y - 1, msg_x, clear_line)
        stdscr.addstr(msg_y + 1, msg_x, clear_line)

        # Draw message
        stdscr.addstr(
            msg_y,
            msg_x,
            message,
            curses.color_pair(ui_colors["score_accent"])
            | curses.A_BOLD
            | curses.A_BLINK,
        )

    except curses.error:
        pass


# Compatibility function for existing code
def draw_board(stdscr, game, config=None, enable_animations=False):
    """Compatibility wrapper for existing main.py."""
    draw_modern_game(stdscr, game, config)


def init_colors(theme_name="modern"):
    """Compatibility wrapper for existing main.py."""
    init_display()
