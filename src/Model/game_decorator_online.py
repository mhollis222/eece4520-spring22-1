from abstract_game import AbstractGame
from abstract_game_decorator import GameDecorator
from abstract_player import AbstractPlayer
from game import Cell
from move import Move


class GameDecoratorOnline(GameDecorator):
    def __init__(self, game: AbstractGame):
        super().__init__(game)
        self.active_player = super().get_active_player()

    def reconstruct(self, state: list, last_active_player: AbstractPlayer):
        # call this immediately after start() if reconstruction is needed
        cell = 1
        for elem in state:
            cell = (cell + 1) % 2
            if cell == 0:
                color = Cell.BLACK
            else:
                color = Cell.WHITE

            move = Move(elem[0], elem[1])
            self.update_board(move, color)
        self.active_player = last_active_player

    def get_order(self):
        return super().get_order()

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
        return self.active_player

    def switch_players(self, player: AbstractPlayer):
        super().switch_players(player)