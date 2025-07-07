"""
Game constants and configuration values for 2048-CLI.
Contains all magic numbers used throughout the application.
"""

# Game mechanics constants
DEFAULT_BOARD_SIZE = 4
INITIAL_TILE_VALUE = 2
SPECIAL_TILE_VALUE = 4
WIN_TILE_VALUE = 2048
MAX_TILE_VALUE = 4096

# Scoring and difficulty constants
SCORE_THRESHOLD_FOR_SPECIAL_TILES = 2000
SCORE_CHANGE_DISPLAY_DURATION = 10.0  # seconds
MAX_SCORE_HISTORY_ENTRIES = 5

# Probability constants
BASE_CHANCE_OF_4 = 0.5
CHANCE_INCREASE_RATE = 0.05
CHANCE_SCORE_INTERVAL = 2000

# UI Layout constants
TILE_WIDTH = 6
TILE_HEIGHT = 3
TILE_SPACING = 2
BOARD_PADDING = 2
MIN_TERMINAL_WIDTH = 80
MIN_TERMINAL_HEIGHT = 24

# Display timing constants
SCORE_FADE_RECENT_THRESHOLD = 2.0  # seconds
SCORE_FADE_MEDIUM_THRESHOLD = 5.0  # seconds

# File and directory constants
CONFIG_FILENAME = "config.json"
SAVE_SLOT_PREFIX = "slot_"
SAVE_FILE_EXTENSION = ".json"
DEFAULT_SAVE_SLOTS = 5

# Color pair ID ranges (to avoid conflicts with system colors)
COLOR_PAIR_START_TILE = 100
COLOR_PAIR_START_UI = 120

# Key codes
ESCAPE_KEY_CODE = 27
SPACE_KEY_CODE = 32
ENTER_KEY_CODES = [10, 13]
BACKSPACE_KEY_CODES = [8, 127]

# ASCII ranges
ASCII_PRINTABLE_START = 32
ASCII_PRINTABLE_END = 126

# Input validation constants
MAX_INPUT_LENGTH = 30
MAX_PATH_LENGTH = 255
