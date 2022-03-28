from Model.abstract_player import AbstractPlayer
from Model.game import Game
from Model.move import Move
import numpy as np


class AIPLayer(AbstractPlayer):
    # TODO: switch to the decorator once merged
    def __init__(self, model: Game, difficulty: int):
        self.simulator = model
        self.depth = difficulty

    # call recursively with a list of previous moves?
    def make_move(self, row, column):
        # get the current possible moves
        moves = self.simulator.get_valid_moves(self)

        index = np.argmax([self.minmax(0, [move], False, int(float('-inf')), int(float('inf'))) for move in moves])

        return moves[index]

    def minmax(self, level: int, moves: list[Move], maximize: bool, alpha: int, beta: int) -> int:
        if level == self.depth:
            return 0 # utility function for this list of moves

        #self.simulator.simulate(moves)
        possible_moves = self.simulator.get_valid_moves(self)
        if maximize:
            best_val = float('-inf')
            for move in possible_moves:
                val = self.minmax(level + 1, moves + move, not maximize, alpha, beta)
                best_val = max(best_val, val)
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            return best_val
        else:
            best_val = float('inf')
            for move in possible_moves:
                val = self.minmax(level + 1, moves + move, not maximize, alpha, beta)
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val






