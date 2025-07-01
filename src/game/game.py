from .board import Board


class Game:
    def __init__(self, size=4):
        self.board = Board(size)
        self.score = 0
        self.game_over = False

    def start(self):
        self.board.place_new_tile(2)
        self.board.place_new_tile(2)

    def is_game_over(self):
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

    def move(self, direction):
        if direction == "left":
            return self._move_left()
        elif direction == "right":
            self.board.rotate(2)
            moved = self._move_left()
            self.board.rotate(2)
            return moved
        elif direction == "up":
            self.board.rotate(1)
            moved = self._move_left()
            self.board.rotate(3)
            return moved
        elif direction == "down":
            self.board.rotate(3)
            moved = self._move_left()
            self.board.rotate(1)
            return moved
        return False

    def _move_left(self):
        moved = False
        for r in range(self.board.size):
            new_row = [i for i in self.board.grid[r] if i != 0]

            # Merge tiles
            i = 0
            while i < len(new_row) - 1:
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    self.score += new_row[i]
                    new_row.pop(i + 1)
                    i += 1  # Skip next tile to prevent double merging
                else:
                    i += 1

            # Pad with zeros
            while len(new_row) < self.board.size:
                new_row.append(0)

            if new_row != self.board.grid[r]:
                moved = True
            self.board.grid[r] = new_row
        return moved
