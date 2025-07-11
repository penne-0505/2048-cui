import time
from typing import Any

from core.constants import (
    DEFAULT_BOARD_SIZE,
    INITIAL_TILE_VALUE,
    MAX_SCORE_HISTORY_ENTRIES,
    WIN_TILE_VALUE,
)

from .board import Board


class Game:
    def __init__(self, size: int = DEFAULT_BOARD_SIZE) -> None:
        self.board: Board = Board(size)
        self.score: int = 0
        self.game_over: bool = False
        self.endless_mode: bool = False
        self._last_score_change: int = 0  # Track score changes for display
        self._score_change_time: float = 0  # Track when score changed
        self._score_history: list[
            dict[str, Any]
        ] = []  # Track recent score additions for display

    def start(self) -> None:
        self.board.place_new_tile(INITIAL_TILE_VALUE)
        self.board.place_new_tile(INITIAL_TILE_VALUE)

    def is_game_over(self) -> bool:
        # In endless mode, never game over
        if self.endless_mode:
            return False

        if self.board.get_empty_cells():
            return False

        for r in range(self.board.size):
            for c in range(self.board.size):
                value = self.board.grid[r][c]
                # Check right neighbor
                if c + 1 < self.board.size and self.board.grid[r][c + 1] == value:
                    return False
                # Check down neighbor
                if r + 1 < self.board.size and self.board.grid[r + 1][c] == value:
                    return False
        return True

    def enable_endless_mode(self) -> None:
        """Enable endless mode - game continues even after reaching win condition."""
        self.endless_mode = True
        self.game_over = False

    def has_won(self) -> bool:
        """Check if player has reached the win condition."""
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.grid[r][c] >= WIN_TILE_VALUE:
                    return True
        return False

    def move(self, direction: str) -> bool:
        if direction == "left":
            return self._move_left()
        elif direction == "right":
            self.board.rotate(2)
            moved = self._move_left()
            self.board.rotate(2)
            return moved
        elif direction == "up":
            self.board.rotate(3)
            moved = self._move_left()
            self.board.rotate(1)
            return moved
        elif direction == "down":
            self.board.rotate(1)
            moved = self._move_left()
            self.board.rotate(3)
            return moved
        return False

    def _move_left(self) -> bool:
        moved = False
        old_score = self.score

        for r in range(self.board.size):
            new_row = [i for i in self.board.grid[r] if i != 0]

            # Merge tiles and track merges
            i = 0
            col_offset = 0  # Track position in compressed row
            while i < len(new_row) - 1:
                if new_row[i] == new_row[i + 1]:
                    merged_value = new_row[i] * 2
                    new_row[i] = merged_value
                    self.score += merged_value


                    new_row.pop(i + 1)
                    i += 1  # Skip next tile to prevent double merging
                else:
                    i += 1
                col_offset += 1

            # Pad with zeros
            while len(new_row) < self.board.size:
                new_row.append(0)

            if new_row != self.board.grid[r]:
                moved = True
            self.board.grid[r] = new_row

        # Track score change for display
        score_change = self.score - old_score
        if score_change > 0:
            self._last_score_change = score_change
            current_time = time.time()
            self._score_change_time = current_time

            # Add to score history (keep last 5 entries)
            self._score_history.append({"points": score_change, "time": current_time})

            # Keep only the most recent score changes
            if len(self._score_history) > MAX_SCORE_HISTORY_ENTRIES:
                self._score_history = self._score_history[-MAX_SCORE_HISTORY_ENTRIES:]

        return moved

