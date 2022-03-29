from abstract_game import AbstractGame
from abstract_game_decorator import GameDecorator
from abstract_player import AbstractPlayer
from game import Game, Cell
from move import Move
import copy


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

    def simulate_play(self, moves):
        sim_game = copy.copy(self.game)
        original_player = sim_game.get_active_player()
        old_score = original_player.score

        for move in moves:
            if not sim_game.has_game_ended():
                current_player = sim_game.get_active_player()
                if sim_game.validate_move(self, move, current_player):

                    if sim_game.get_active_player() == sim_game.order[0]:
                        sim_game.update_board(move, Cell.BLACK)
                    else:
                        sim_game.update_board(move, Cell.WHITE)

                    sim_game.switch_players(self, current_player)
                else:
                    return None
            else:
                break

        new_score = original_player.score

        return new_score - old_score











