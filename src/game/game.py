from .board import Board


class Game:
    def __init__(self, size=4):
        self.board = Board(size)
        self.score = 0
        self.game_over = False
        self.endless_mode = False
        self.recent_merges = []  # Track recent merges for animations
        self._last_score_change = 0  # Track score changes for display
        self._score_change_time = 0  # Track when score changed
        self._score_history = []  # Track recent score additions for display

    def start(self):
        self.board.place_new_tile(2)
        self.board.place_new_tile(2)

    def is_game_over(self):
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

    def enable_endless_mode(self):
        """Enable endless mode - game continues even after reaching win condition."""
        self.endless_mode = True
        self.game_over = False

    def has_won(self):
        """Check if player has reached 2048."""
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.grid[r][c] >= 2048:
                    return True
        return False

    def move(self, direction):
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

    def _move_left(self):
        moved = False
        self.recent_merges = []  # Clear previous merges
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

                    # Record merge for animation (position after merge)
                    self.recent_merges.append((r, col_offset, merged_value))

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
            import time

            current_time = time.time()
            self._score_change_time = current_time

            # Add to score history (keep last 5 entries)
            self._score_history.append({"points": score_change, "time": current_time})

            # Keep only the most recent 5 score changes
            if len(self._score_history) > 5:
                self._score_history = self._score_history[-5:]

        return moved

    def get_recent_merges(self):
        """Get recent tile merges for animation purposes."""
        return self.recent_merges
