import copy
from abstract_game import AbstractGame
from abstract_game_decorator import GameDecorator
from abstract_player import AbstractPlayer
from game import Cell
from move import Move


class GameDecoratorAI(GameDecorator):
    def __init__(self, game: AbstractGame):
        super().__init__(game)

    def get_order(self):
        return super().get_order()

    def validate_move(self, move: Move, play: AbstractPlayer):
        super().validate_move(move, play)

    def get_valid_moves(self, play: AbstractPlayer):
        return self.game.get_valid_moves(play)

    def search(self, move: tuple, identity: int):
        super().search(move, identity)

    def valid_moves_avail(self, moves: list[Move], play: AbstractPlayer):
        sim_game = copy.deepcopy(self.game)
        for move in moves:
            current_player = sim_game.get_active_player()
            if sim_game.validate_move(move, current_player):

                if sim_game.get_active_player() == sim_game.get_order()[0]:
                    sim_game.update_board(move, Cell.BLACK)
                else:
                    sim_game.update_board(move, Cell.WHITE)

                sim_game.switch_players(current_player)
        return sim_game.get_valid_moves(play)

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
        return super().get_active_player()

    def switch_players(self, player: AbstractPlayer):
        super().switch_players(player)

    def simulate_play(self, moves):
        sim_game = copy.deepcopy(self.game)
        original_player = sim_game.get_active_player()
        old_score = original_player.score

        for move in moves:
<<<<<<< HEAD
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
=======
            current_player = sim_game.get_active_player()
            if sim_game.validate_move(move, current_player):

                if sim_game.get_active_player() == sim_game.get_order()[0]:
                    sim_game.update_board(move, Cell.BLACK)
                else:
                    sim_game.update_board(move, Cell.WHITE)

                sim_game.switch_players(current_player)
        sim_game.update_score()
>>>>>>> 3b0705693dd6c6f1a999d6effa4884b57b6e57c8

        new_score = original_player.score

        return new_score - old_score
