from abc import ABC, abstractmethod
from typing import Tuple, Type

import numpy as np
from scipy.signal import convolve

from .board import Board
from .enums import GameState


class Validator(ABC):
    def __init__(self, tics_to_win: int) -> None:
        self.tics_to_win = tics_to_win

    @abstractmethod
    def winning_condition(self, board: Type[Board]) -> bool:
        pass


class ConvolutionValidator(Validator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def winning_condition(self, board: Type[Board], last_move: Tuple[int, int]) -> int:
        score = self.score(board, last_move)
        if score == self.tics_to_win:
            return GameState.FINISHED_VICTORY
        if np.all(board.board):
            return GameState.FINISHED_DRAW
        return GameState.NOT_FINISHED

    def score(self, board: Type[Board], last_move: Tuple[int, int]):
        return max(
            [
                self.diagonal_check(board, last_move),
                self.non_diagonal_check(board, last_move),
            ]
        )

    def max_in_row(self, board, mask):
        return convolve(board, mask, mode="valid").max()

    def diagonal_check(self, board, last_move: Tuple[int, int]) -> bool:
        x, y = last_move
        mark = board.get_tile(x, y)
        board_view = board.board[
            max(x - self.tics_to_win - 1, 0) : min(x + self.tics_to_win, board.size),
            max(y - self.tics_to_win - 1, 0) : min(y + self.tics_to_win, board.size),
        ]

        # Top-left to bottom-right
        mask = np.diag(np.full(self.tics_to_win, fill_value=mark, dtype=np.int8))
        tlbr = self.max_in_row(board_view, mask)

        # Top-right to bottom-left
        mask = np.flip(mask, axis=1)
        trbl = self.max_in_row(board_view, mask)
        return max(tlbr, trbl)

    def non_diagonal_check(self, board, last_move: Tuple[int, int]) -> bool:
        x, y = last_move
        mark = board.get_tile(x, y)
        mask = np.full(self.tics_to_win, fill_value=mark, dtype=np.int8)

        # Vertical
        board_view = board.board[
            max(x - self.tics_to_win - 1, 0) : min(x + self.tics_to_win, board.size),
            y,
        ]
        vert = self.max_in_row(board_view, mask)

        # Horizontal
        board_view = board.board[
            x,
            max(y - self.tics_to_win - 1, 0) : min(y + self.tics_to_win, board.size),
        ]
        hori = self.max_in_row(board_view, mask)
        return max(vert, hori)
