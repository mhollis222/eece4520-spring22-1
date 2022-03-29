from Model.abstract_game import AbstractGame
from abstract_player import AbstractPlayer
from move import Move


class GameDecorator(AbstractGame):
    def __init__(self, game: AbstractGame):
        self.game = game

    def validate_move(self, move: Move, play: AbstractPlayer):
        self.game.validate_move(move, play)

    def get_valid_moves(self, play: AbstractPlayer):
        self.game.get_valid_moves(play)

    def search(self, move: tuple, identity: int):
        self.game.search(move, identity)

    def valid_moves_avail(self, moves: list[Move], play: AbstractPlayer):
        self.game.valid_moves_avail(play)

    def start(self) -> None:
        self.game.start()

    def get_board(self):
        self.game.get_board()

    def update_board(self, m: Move, c) -> None:
        self.game.update_board(m, c)

    def update_score(self):
        self.game.update_score()

    def is_board_filled(self) -> bool:
        return self.game.is_board_filled()

    def has_game_ended(self) -> bool:
        return self.game.has_game_ended()

    def display_winner(self) -> int:
        return self.game.display_winner()

    def get_active_player(self) -> AbstractPlayer:
        return self.game.get_active_player()

    def switch_players(self, player: AbstractPlayer):
        self.game.switch_players(player)
