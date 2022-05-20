from abc import ABC, abstractmethod
from typing import Tuple


class Player(ABC):
    def __init__(self, mark) -> None:
        self.mark = mark

    @abstractmethod
    def make_move(self, game) -> Tuple[int, int]:
        pass


class HumanPlayer(Player):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def make_move(self, board) -> Tuple[int, int]:
        while 1:
            try:
                x, y = map(int, input("Enter X Y: ").split())
            except ValueError:
                print("Enter both coordinates as integers.")
            if board.set_tile(x, y, self.mark):
                return (x, y)
