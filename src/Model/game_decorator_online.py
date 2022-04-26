from Model.abstract_game import AbstractGame
from Model.abstract_game_decorator import GameDecorator
from Model.abstract_player import AbstractPlayer
from Model.game import Cell
from Model.move import Move


class GameDecoratorOnline(GameDecorator):
    def __init__(self, game: AbstractGame, order):
        super().__init__(game)
        self.active_player = super().get_active_player()
        self.order = order
        # if order[0].name == self.game.p1.name:
        #     self.game.p1.identifier = 1
        #     self.game.p2.identifier = 2
        # else:
        #     self.game.p1.identifier = 2
        #     self.game.p2.identifier = 1
        self.active_player = 0

    def reconstruct(self, state: list, last_active_player: AbstractPlayer):
        # call this immediately after start() if reconstruction is needed

        cell = 1
        for elem in state:
            cell = (cell + 1) % 2 # this will alternate between 0 and 1, we use 0 as empty.
            if cell == 0:
                color = Cell.BLACK
            else:
                color = Cell.WHITE

            move = Move(elem[0], elem[1])
            self.update_board(move, color)
        self.active_player = last_active_player

    def get_order(self):
        return self.order

    def validate_move(self, move: Move, play: AbstractPlayer):
        super().validate_move(move, play)

    def get_valid_moves(self, play: AbstractPlayer):
        return self.game.get_valid_moves(play)

    def start(self) -> None:
        super().start()

    def get_board(self):
        return super().get_board()

    def update_board(self, m: Move, c) -> None:
        super().update_board(m, c)

    def update_score(self):
        super().update_score()

    def is_board_filled(self) -> bool:
        return super().is_board_filled()

    def has_game_ended(self) -> bool:
        return super().has_game_ended()

    def display_winner(self) -> int:
        return super().display_winner()

    def get_active_player(self) -> AbstractPlayer:
        return self.order[self.active_player]

    def switch_players(self, player: AbstractPlayer):
        self.active_player = (self.active_player + 1) % 2
