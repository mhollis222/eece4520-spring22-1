from Model.abstract_player import AbstractPlayer
from Model.game_decorator_ai import GameDecoratorAI
from Model.move import Move
import numpy as np


class AIPLayer(AbstractPlayer):
    # TODO: switch to the decorator once merged
    def __init__(self, name, difficulty: int):
        super(AIPLayer, self).__init__(name)
        self.simulator = None
        self.depth = difficulty
        self.opp = None

    def add_simulator(self, sim: GameDecoratorAI):
        self.simulator = sim

    def add_opp(self, player: AbstractPlayer):
        self.opp = player

    # call recursively with a list of previous moves?
    def make_move(self, row, column):
        # get the current possible moves
        moves = self.simulator.get_valid_moves(self)

        index = np.argmax([self.minmax(0, [Move(move[0], move[1])], True, -100, 100) for move in moves])

        return moves[index]

    def minmax(self, level: int, moves, maximize: bool, alpha: int, beta: int) -> int:
        if level == self.depth:
            # print(self.simulator.simulate_play(moves))
            return self.simulator.simulate_play(moves) # utility function for this list of moves

        if max:
            possible_moves = self.simulator.get_moves_sim(moves, self)
        else:
            possible_moves = self.simulator.get_moves_sim(moves, self.opp)

        if maximize:
            best_val = float('-inf')
            for move in possible_moves:
                val = self.minmax(level + 1, moves + [Move(move[0], move[1])], not maximize, alpha, beta)
                best_val = max(best_val, val)
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            return best_val
        else:
            best_val = float('inf')
            for move in possible_moves:
                val = self.minmax(level + 1, moves + [Move(move[0], move[1])], not maximize, alpha, beta)
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val

    def type(self):
        return 'AI'





