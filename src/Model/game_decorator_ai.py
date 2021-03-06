import copy
from Model.abstract_game import AbstractGame
from Model.abstract_game_decorator import GameDecorator
from Model.abstract_player import AbstractPlayer
from Model.game import Cell
from Model.move import Move


class GameDecoratorAI(GameDecorator):
    def __init__(self, game: AbstractGame, order):
        super().__init__(game)
        self.active_player = super().get_active_player()
        self.order = order
        self.active_player = 0

    def get_order(self):
        return self.order

    def validate_move(self, move: Move, play: AbstractPlayer):
        super().validate_move(move, play)

    def get_valid_moves(self, play: AbstractPlayer):
        return self.game.get_valid_moves(play)

    def search(self, move: tuple, identity: int):
        super().search(move, identity)

    def get_moves_sim(self, moves: list[Move], play: AbstractPlayer):
        old_save = self.game.get_board()
        sim = copy.deepcopy(old_save)
        self.game.board = sim
        for move in moves:
            current_player = self.game.get_active_player()
            if self.game.validate_move(move, current_player):

                if self.game.get_active_player() == self.game.get_order()[0]:
                    self.game.update_board(move, Cell.BLACK)
                else:
                    self.game.update_board(move, Cell.WHITE)

                self.game.switch_players(current_player)
        moves = self.game.get_valid_moves(play)
        self.game.board = old_save
        return moves

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
        super().switch_players(player)

    def simulate_play(self, moves):
        old_save = self.game.get_board()
        sim = copy.deepcopy(old_save)
        self.game.board = sim
        original_player = self.game.get_active_player()
        old_score = original_player.score

        for move in moves:
            if not self.game.has_game_ended():
                current_player = self.game.get_active_player()
                if self.game.validate_move(move, current_player):

                    if self.game.get_active_player() == self.game.get_order()[0]:
                        self.game.update_board(move, Cell.BLACK)
                    else:
                        self.game.update_board(move, Cell.WHITE)

                    self.game.switch_players(current_player)
            else:
                break

        self.game.update_score()
        new_score = original_player.score

        self.game.board = old_save

        return new_score - old_score
