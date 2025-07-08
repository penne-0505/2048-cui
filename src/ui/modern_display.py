"""
Modern minimalist display system for 2048-CLI.
Based on mm.png design - clean, floating tiles, minimal UI.
"""

import curses
import time
from typing import Any, Optional

from core.config import get_animation_fps, get_animation_speed, is_animations_enabled
from core.constants import (
    DEFAULT_BOARD_SIZE,
    SCORE_CHANGE_DISPLAY_DURATION,
    SCORE_FADE_MEDIUM_THRESHOLD,
    SCORE_FADE_RECENT_THRESHOLD,
    TILE_HEIGHT,
    TILE_SPACING,
    TILE_WIDTH,
)
from core.modern_themes import (
    get_tile_color_pair,
    get_ui_color_pairs,
    init_modern_colors,
)
from ui.animation import AnimationManager


# Global animation manager instance
_animation_manager: Optional[AnimationManager] = None


def init_display() -> None:
    """Initialize the modern display system."""
    global _animation_manager
    init_modern_colors()
    _animation_manager = AnimationManager()


def get_animation_manager() -> Optional[AnimationManager]:
    """Get the global animation manager instance."""
    return _animation_manager


def draw_modern_game(
    stdscr: curses.window, game: Any, config: dict[str, Any] | None = None
) -> None:
    """
    Draw the game using modern minimalist design.

    Layout:
    - Top: Score and score change
    - Center: 4x4 floating tile grid
    - Bottom: Simple controls
    """
    global _animation_manager
    
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    ui_colors = get_ui_color_pairs()
    
    # Initialize and configure animation manager if needed
    if config and _animation_manager:
        animations_enabled = is_animations_enabled(config)
        if animations_enabled:
            _animation_manager.set_fps(get_animation_fps(config))
            _animation_manager.set_speed_multiplier(get_animation_speed(config))
            if not _animation_manager.running:
                _animation_manager.start()
        elif _animation_manager.running:
            _animation_manager.stop()

    # Draw header (score)
    draw_score_header(stdscr, game, ui_colors, width)

    # Calculate board position (centered) for bordered tiles
    board_start_y = 4  # Leave space for header
    board_width = (
        DEFAULT_BOARD_SIZE * TILE_WIDTH + (DEFAULT_BOARD_SIZE - 1) * TILE_SPACING
    )
    # Center the board properly
    board_start_x = max(2, (width - board_width) // 2)

    # Draw floating tile grid with animation support
    animations_enabled = config and is_animations_enabled(config)
    draw_floating_tiles(stdscr, game, board_start_y, board_start_x, animations_enabled)

    # Draw footer controls
    draw_simple_controls(stdscr, ui_colors, height, width)

    # Game over overlay if needed
    if game.game_over:
        draw_game_over(stdscr, ui_colors, height, width)

    stdscr.refresh()


def draw_score_header(
    stdscr: curses.window, game: Any, ui_colors: dict[str, int], width: int
) -> None:
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


def draw_score_history(
    stdscr: curses.window, game: Any, ui_colors: dict[str, int], width: int
) -> None:
    """Draw recent score additions in descending order."""
    score_history = getattr(game, "_score_history", [])

    if not score_history:
        return

    current_time = time.time()

    # Filter recent changes and sort by time (newest first)
    recent_changes = [
        change
        for change in score_history
        if current_time - change["time"] < SCORE_CHANGE_DISPLAY_DURATION
    ]
    recent_changes.sort(key=lambda x: x["time"], reverse=True)

    # Display up to 4 recent score changes
    for i, change in enumerate(recent_changes[:4]):
        if i >= 4:  # Limit to 4 lines
            break

        # Calculate fade effect based on age
        age = current_time - change["time"]
        if age < SCORE_FADE_RECENT_THRESHOLD:
            # Recent - bright
            color = curses.color_pair(ui_colors["score_accent"]) | curses.A_BOLD
        elif age < SCORE_FADE_MEDIUM_THRESHOLD:
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


def draw_floating_tiles(
    stdscr: curses.window, game: Any, start_y: int, start_x: int, animations_enabled: bool = False
) -> None:
    """Draw grid of floating tiles with borders and animation support."""
    global _animation_manager
    
    for row in range(DEFAULT_BOARD_SIZE):
        for col in range(DEFAULT_BOARD_SIZE):
            tile_value = game.board.grid[row][col]

            # Calculate base tile position for bordered tiles
            base_tile_y = start_y + row * (TILE_HEIGHT + 1)  # tile height + spacing
            base_tile_x = start_x + col * (TILE_WIDTH + TILE_SPACING)  # tile width + spacing

            # Check for animation data if animations are enabled
            actual_y, actual_x = base_tile_y, base_tile_x
            scale = 1.0
            alpha = 1.0
            
            if animations_enabled and _animation_manager:
                tile_id = f"{row}_{col}"
                render_data = _animation_manager.get_tile_render_data(tile_id)
                if render_data:
                    # Apply animation transformations
                    anim_pos = render_data['position']
                    scale = render_data['scale']
                    alpha = render_data['alpha']
                    
                    # Convert logical position to screen coordinates
                    actual_y = start_y + int(anim_pos.y * (TILE_HEIGHT + 1))
                    actual_x = start_x + int(anim_pos.x * (TILE_WIDTH + TILE_SPACING))

            # Only draw non-empty tiles or tiles with animation data
            if tile_value > 0 or (animations_enabled and scale != 1.0):
                draw_single_tile(stdscr, tile_value, actual_y, actual_x, scale, alpha)
            elif tile_value == 0:
                # Draw empty tile placeholder
                draw_single_tile(stdscr, 0, actual_y, actual_x)


def draw_single_tile(stdscr: curses.window, value: int, y: int, x: int, scale: float = 1.0, alpha: float = 1.0) -> None:
    """Draw a single tile with border outline and animation effects."""
    color_pair = get_tile_color_pair(value)
    
    # Apply scale effect for animations (simple approximation)
    if scale != 1.0:
        # For scale effects, we can adjust the tile width/height or use different characters
        # This is a simplified implementation - in a full version you might skip drawing
        # parts of the tile or use different characters to simulate scaling
        if scale < 0.8:
            # Very small - draw a minimal representation
            try:
                if value > 0:
                    value_str = str(value)
                    stdscr.addstr(y + 1, x + 2, value_str[:2], curses.color_pair(color_pair))
                return
            except curses.error:
                return

    if value == 0:
        # Empty tile - subtle border outline
        try:
            border_line = "─" * (TILE_WIDTH - 2)
            spaces_line = " " * (TILE_WIDTH - 2)
            stdscr.addstr(y, x, f"╭{border_line}╮", curses.color_pair(color_pair))
            stdscr.addstr(y + 1, x, f"│{spaces_line}│", curses.color_pair(color_pair))
            stdscr.addstr(y + 2, x, f"╰{border_line}╯", curses.color_pair(color_pair))
        except curses.error:
            pass
    else:
        # Tile with value - bordered box with centered number
        value_str = str(value)
        content_width = TILE_WIDTH - 2  # Account for border characters
        padding = (content_width - len(value_str)) // 2
        left_pad = " " * padding
        right_pad = " " * (content_width - len(value_str) - padding)

        middle_content = f"│{left_pad}{value_str}{right_pad}│"

        try:
            border_line = "─" * (TILE_WIDTH - 2)
            # Apply alpha effect for fading (simplified - in terminal this is limited)
            color_attr = curses.color_pair(color_pair)
            if alpha < 0.7:
                # Dim the tile for fade effect
                color_attr = curses.color_pair(color_pair)
            elif scale > 1.1:
                # Brighten for emphasis during merge
                color_attr = curses.color_pair(color_pair) | curses.A_BOLD
            else:
                color_attr = curses.color_pair(color_pair) | curses.A_BOLD
                
            # Top border
            stdscr.addstr(y, x, f"╭{border_line}╮", curses.color_pair(color_pair))
            # Middle with value
            stdscr.addstr(y + 1, x, middle_content, color_attr)
            # Bottom border
            stdscr.addstr(y + 2, x, f"╰{border_line}╯", curses.color_pair(color_pair))
        except curses.error:
            pass


def draw_simple_controls(
    stdscr: curses.window, ui_colors: dict[str, int], height: int, width: int
) -> None:
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


def draw_game_over(
    stdscr: curses.window, ui_colors: dict[str, int], height: int, width: int
) -> None:
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
def draw_board(
    stdscr: curses.window,
    game: Any,
    config: dict[str, Any] | None = None,
    enable_animations: bool = False,
) -> None:
    """Compatibility wrapper for existing main.py."""
    draw_modern_game(stdscr, game, config)


def init_colors(theme_name: str = "modern") -> None:
    """Compatibility wrapper for existing main.py."""
    init_display()
