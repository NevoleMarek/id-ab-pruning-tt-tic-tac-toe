from enum import Enum


class GameState(Enum):
    INITIALIZED = -1
    NOT_FINISHED = 0
    FINISHED_VICTORY = 1
    FINISHED_DRAW = 2
