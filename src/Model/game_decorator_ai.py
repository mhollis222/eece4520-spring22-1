from abstract_game import AbstractGame
from abstract_game_decorator import GameDecorator
from abstract_player import AbstractPlayer
from move import Move


class GameDecoratorAI(GameDecorator):
    def __init__(self, game: AbstractGame):
        super().__init__(game)

    def validate_move(self, move: Move, play: AbstractPlayer):
        super().validate_move(move, play)

    def get_valid_moves(self, play: AbstractPlayer):
        super().get_valid_moves(play)

    def search(self, move: tuple, identity: int):
        super().search(move, identity)

    def valid_moves_avail(self, play: AbstractPlayer):
        super().valid_moves_avail(play)

    def start(self) -> None:
        super().start()

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
        return super().get_active_player()

    def switch_players(self, player: AbstractPlayer):
        super().switch_players(player)