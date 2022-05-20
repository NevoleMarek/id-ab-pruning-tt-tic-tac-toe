from abc import ABC, abstractmethod
from collections import Counter

import numpy as np
from scipy.signal import convolve

from .enums import GameState


class Scorer(ABC):
    def __init__(self, tics_to_win) -> None:
        self.tics_to_win = tics_to_win
        super().__init__()

    @abstractmethod
    def score(self, board):
        pass


class ConvolutionScorer(Scorer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def score(self, board, mark: int):
        cntr = self.combination_counter(board, mark)
        score = 0
        state = GameState.NOT_FINISHED

        if self.tics_to_win in cntr:
            score += 1000
            state = GameState.FINISHED_VICTORY
        if self.tics_to_win - 1 in cntr:
            score += 40 * cntr[self.tics_to_win - 1]
        if self.tics_to_win - 2 in cntr:
            score += 10 * cntr[self.tics_to_win - 2]
        if self.tics_to_win - 3 in cntr:
            score += 1 * cntr[self.tics_to_win - 3]

        if -self.tics_to_win in cntr:
            score -= 1000
            state = GameState.FINISHED_VICTORY
        if -self.tics_to_win + 1 in cntr:
            score -= 20 * cntr[-self.tics_to_win + 1]
        if -self.tics_to_win + 2 in cntr:
            score -= 5 * cntr[-self.tics_to_win + 2]
        if -self.tics_to_win + 3 in cntr:
            score -= 1 * cntr[self.tics_to_win + 3]

        return score, state

    def combination_counter(self, board, mark: int) -> bool:
        cntr = Counter()

        mask = np.full((1, self.tics_to_win), fill_value=mark, dtype=np.int8)
        hor = convolve(board, mask, mode="valid")  # Horizontal
        ver = convolve(board, mask.T, mode="valid")  # Vertical

        mask = np.diag(np.full(self.tics_to_win, fill_value=mark, dtype=np.int8))
        tlbr = convolve(board, mask, mode="valid")  # Top-left to bottom-right
        mask = np.flip(mask, axis=1)
        trbl = convolve(board, mask, mode="valid")  # Top-right to bottom-left

        cntr.update(hor.ravel())
        cntr.update(ver.ravel())
        cntr.update(tlbr.ravel())
        cntr.update(trbl.ravel())

        return cntr


if __name__ == "__main__":
    cs = ConvolutionScorer(tics_to_win=3)
