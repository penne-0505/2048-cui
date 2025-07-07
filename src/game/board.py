import random

from core.constants import DEFAULT_BOARD_SIZE


class Board:
    def __init__(self, size: int = DEFAULT_BOARD_SIZE) -> None:
        self.size: int = size
        self.grid: list[list[int]] = [[0] * size for _ in range(size)]

    def get_empty_cells(self) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.grid[r][c] == 0
        ]

    def place_new_tile(self, value: int) -> None:
        empty_cells = self.get_empty_cells()
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = value

    def __str__(self) -> str:
        return "\n".join([" ".join(map(str, row)) for row in self.grid])

    def rotate(self, times: int = 1) -> None:
        for _ in range(times):
            self.grid = [list(row) for row in zip(*self.grid[::-1], strict=False)]
