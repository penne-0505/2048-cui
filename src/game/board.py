import random


class Board:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]

    def get_empty_cells(self):
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.grid[r][c] == 0
        ]

    def place_new_tile(self, value):
        empty_cells = self.get_empty_cells()
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = value

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.grid])

    def rotate(self, times=1):
        for _ in range(times):
            self.grid = [list(row) for row in zip(*self.grid[::-1])]
