import math

import numpy as np

from .zobrist import ZobristHashing


class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int8)
        self.tics = {-1: "X", 0: " ", 1: "O"}
        self.hasher = ZobristHashing(size=size)
        self.z_hash = self.hasher.hash(self.board)
        self.occupied_tiles = set()

    def is_empty(self, x: int, y: int) -> bool:
        return True if self.board[x, y] == 0 else False

    def _add_occupied(self, x: int, y: int) -> None:
        self.occupied_tiles.add((x, y))

    def _discard_occupied(self, x: int, y: int) -> None:
        self.occupied_tiles.discard((x, y))

    def out_of_bounds(self, x: int, y: int) -> bool:
        if 0 <= x < self.size and 0 <= y < self.size:
            return False
        return True

    def set_tile(self, x: int, y: int, mark: int) -> bool:
        if self.out_of_bounds(x, y) and self.is_empty(x, y):
            return False
        old_val = self.board[x, y]
        self.board[x, y] = mark
        if mark == 0:
            self._discard_occupied(x, y)
        else:
            self._add_occupied(x, y)
        self._update_hash(x, y, old_val)
        return True

    def set_tile_(self, x: int, y: int, mark: int):
        old_val = self.board[x, y]
        self.board[x, y] = mark
        self._update_hash(x, y, old_val)
        if mark == 0:
            self._discard_occupied(x, y)
        else:
            self._add_occupied(x, y)

    def get_tile(self, x: int, y: int) -> int:
        return self.board[x, y]

    def _update_hash(self, x: int, y: int, old_val: int):
        self.z_hash = self.hasher.update_hash(
            hsh=self.z_hash, tile=(x, y), new_val=self.board[x, y], old_val=old_val
        )

    def print(self):
        board = "-\n"
        s_width = math.ceil(math.log10(self.size))
        x_coords = [f"{i:>{s_width}}" for i in range(self.size)]
        top_row = f"{'':>{s_width}} " + " ".join(x_coords) + "\n"
        board += top_row
        for x, row in enumerate(self.board):
            formatted_row = [f"{self.tics[i]:>{s_width}}" for i in row]
            board += f"{x:>{s_width}} " + " ".join(formatted_row) + "\n"
        board += "-"
        print(board)
