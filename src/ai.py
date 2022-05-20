import random
import time
from typing import List, Tuple

from .enums import GameState
from .player import Player
from .scorer import ConvolutionScorer
from .transposition_table import TranspositionTable, TTEntry


class AlphaBetaPruningPlayer(Player):
    def __init__(self, time_limit, tics_to_win, *args, **kwargs) -> None:
        self.time_limit = time_limit
        self.start = None
        self.scorer = ConvolutionScorer(tics_to_win)
        self.transposition_table = dict()
        super().__init__(*args, **kwargs)

    def make_move(self, board) -> Tuple[int, int]:
        print("AI move")
        self.moves_tried = 0
        self.tt = TranspositionTable(mod=2**16)
        self.start = time.time()
        max_depth = len(self.admissible_moves(board, radius=2))

        best_move = None
        best_score = float("-inf")

        for depth in range(1, max_depth + 1):
            score, move = self.alphabeta(
                board=board,
                alpha=float("-inf"),
                beta=float("inf"),
                mark=1,
                depth=depth,
            )

            if self.time_exceeded():
                break

            best_move = move
            best_score = score
        board.set_tile(best_move[0], best_move[1], self.mark)

        print(f"ABP finished with max depth={depth} after {time.time() - self.start}s")
        print(f"Moves tried: {self.moves_tried}")
        print(f"x={best_move[0]} y={best_move[1]}")
        return best_move

    def admissible_moves(self, board, radius: int) -> List[Tuple[int, int]]:
        radius = radius
        moves = set()
        for x, y in board.occupied_tiles:
            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    if board.is_empty(x + i, y + j):
                        moves.add((x + i, y + j))
        return list(moves)

    def time_exceeded(self) -> float:
        return time.time() - self.start > self.time_limit

    def alphabeta(
        self,
        board,
        alpha,
        beta,
        mark: int,
        depth: int,
    ) -> int:
        score, state = None, None
        if depth == 0:  # If leaf add to or search TT and return
            if board.z_hash not in self.tt:
                score, state = self.scorer.score(board.board, mark)
                self.tt[board.z_hash] = TTEntry(0, 0, score, state)
            return self.tt[board.z_hash].score, None
        elif board.z_hash in self.tt:  # If terminal but not leaf
            tte = self.tt[board.z_hash]
            if tte.state is GameState.FINISHED_VICTORY:
                return tte.score, None
        else:
            score, state = self.scorer.score(board.board, mark)
            if (
                depth == 0
                or state is GameState.FINISHED_VICTORY
                or self.time_exceeded()
            ):
                return score, None

        moves = self.admissible_moves(board, radius=1)
        if not moves:  # no moves means draw
            return 0, None

        random.shuffle(moves)

        best_score = float("-inf")
        best_move = None
        for move in moves:

            self.moves_tried += 1

            board.set_tile_(move[0], move[1], mark)
            score, _ = self.alphabeta(
                board=board,
                alpha=-beta,
                beta=-alpha,
                mark=-mark,
                depth=depth - 1,
            )
            board.set_tile_(move[0], move[1], 0)

            if best_score < -score:
                best_score = -score
                best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

            if self.time_exceeded():
                return best_score, best_move

        return best_score, best_move
