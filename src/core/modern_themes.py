"""
Modern minimalist themes for 2048-CLI based on mm.png design.
Clean, contemporary visual design with floating tiles.
"""

import curses

# Modern minimalist theme inspired by mm.png
MODERN_THEME = {
    "name": "Modern Minimalist",
    "description": "Clean, contemporary design with floating tiles",
    # Tile colors - border-style design (foreground colors only)
    "tile_colors": {
        0: {"fg": 235, "bg": -1},  # Empty - very subtle grey border
        2: {"fg": 250, "bg": -1},  # Light grey border
        4: {"fg": 226, "bg": -1},  # Yellow border
        8: {"fg": 118, "bg": -1},  # Green border
        16: {"fg": 214, "bg": -1},  # Orange border
        32: {"fg": 196, "bg": -1},  # Red border
        64: {"fg": 129, "bg": -1},  # Blue border
        128: {"fg": 220, "bg": -1},  # Bright yellow border
        256: {"fg": 208, "bg": -1},  # Dark orange border
        512: {"fg": 160, "bg": -1},  # Pink border
        1024: {"fg": 93, "bg": -1},  # Purple border
        2048: {"fg": 21, "bg": -1},  # Dark blue border
        4096: {"fg": 52, "bg": -1},  # Dark red border
    },
    # UI elements colors
    "ui_colors": {
        "score": 250,  # Light grey for score
        "score_accent": 226,  # Yellow for score highlights
        "controls": 244,  # Grey for control text
        "background": 235,  # Dark background
    },
}

# Color pair mappings (starting from 100 to avoid conflicts)
COLOR_PAIRS = {
    "tile_empty": 100,
    "tile_2": 101,
    "tile_4": 102,
    "tile_8": 103,
    "tile_16": 104,
    "tile_32": 105,
    "tile_64": 106,
    "tile_128": 107,
    "tile_256": 108,
    "tile_512": 109,
    "tile_1024": 110,
    "tile_2048": 111,
    "tile_4096": 112,
    "ui_score": 120,
    "ui_score_accent": 121,
    "ui_controls": 122,
}


def init_modern_colors():
    """Initialize color pairs for modern theme."""
    curses.start_color()
    curses.use_default_colors()

    theme = MODERN_THEME

    # Initialize tile colors
    tile_values = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    for i, value in enumerate(tile_values):
        if value in theme["tile_colors"]:
            colors = theme["tile_colors"][value]
            pair_id = (
                COLOR_PAIRS[f"tile_{value}"] if value > 0 else COLOR_PAIRS["tile_empty"]
            )
            curses.init_pair(pair_id, colors["fg"], colors["bg"])

    # Initialize UI colors
    curses.init_pair(COLOR_PAIRS["ui_score"], theme["ui_colors"]["score"], -1)
    curses.init_pair(
        COLOR_PAIRS["ui_score_accent"], theme["ui_colors"]["score_accent"], -1
    )
    curses.init_pair(COLOR_PAIRS["ui_controls"], theme["ui_colors"]["controls"], -1)


def get_tile_color_pair(value):
    """Get color pair for tile value."""
    if value == 0:
        return COLOR_PAIRS["tile_empty"]
    elif value <= 4096 and f"tile_{value}" in COLOR_PAIRS:
        return COLOR_PAIRS[f"tile_{value}"]
    else:
        # For very high values, use the highest defined color
        return COLOR_PAIRS["tile_4096"]


def get_ui_color_pairs():
    """Get UI color pairs."""
    return {
        "score": COLOR_PAIRS["ui_score"],
        "score_accent": COLOR_PAIRS["ui_score_accent"],
        "controls": COLOR_PAIRS["ui_controls"],
    }
