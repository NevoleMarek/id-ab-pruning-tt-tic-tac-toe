from .ai import AlphaBetaPruningPlayer
from .board import Board
from .enums import GameState
from .player import HumanPlayer
from .validator import ConvolutionValidator

TICS_TO_WIN = 5
SIZE = 15


class Game:
    def __init__(self) -> None:
        self.players = None
        self.turn_counter = None
        self.game_state = None
        self.player_on_turn = None
        self.last_move = None
        self.board = None
        self.validator = None

    def run(self) -> None:
        self.initialize()
        self.game_loop()

    def initialize(self) -> None:
        self.board = Board(SIZE)
        self.validator = ConvolutionValidator(tics_to_win=TICS_TO_WIN)

        self.players = {
            0: HumanPlayer(mark=-1),
            1: AlphaBetaPruningPlayer(time_limit=5, tics_to_win=TICS_TO_WIN, mark=1),
        }
        self.turn_counter = 0
        self.game_state = GameState.INITIALIZED
        self.player_on_turn = self.players[0]

    def next_turn(self) -> None:
        self.turn_counter += 1
        self.player_on_turn = self.players[self.turn_counter % 2]

    def game_loop(self) -> None:
        if self.game_state is GameState.INITIALIZED:
            self.game_state = GameState.NOT_FINISHED

        self.render()
        while self.game_state is GameState.NOT_FINISHED:

            move = self.player_on_turn.make_move(self.board)
            self.game_state = self.validator.winning_condition(self.board, move)

            if self.game_state is GameState.FINISHED_DRAW:
                print("It is a draw.")
            elif self.game_state is GameState.FINISHED_VICTORY:
                print(f"Player {self.board.tics[self.player_on_turn.mark]} won!")
            else:
                self.next_turn()

            self.render()

    def render(self) -> None:
        self.board.print()
