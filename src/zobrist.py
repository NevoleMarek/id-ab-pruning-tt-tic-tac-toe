from typing import Tuple

import numpy as np


class ZobristHashing:
    def __init__(self, size: int) -> None:
        rng = np.random.default_rng()
        self.table = rng.integers(2**64, size=(size, size, 3), dtype=np.uint64)

    def hash(self, board) -> int:
        h = 0
        for i in range(board.shape[0]):
            for j in range(board.shape[0]):
                h ^= int(self.table[i, j, board[i, j] + 1])
        return h

    def update_hash(
        self, hsh: int, tile: Tuple[int, int], old_val: int, new_val: int
    ) -> int:
        x, y = tile
        hsh ^= int(self.table[x, y, old_val + 1])
        hsh ^= int(self.table[x, y, new_val + 1])
        return hsh
