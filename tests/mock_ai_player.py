from abc import ABC

from abstract_player import AbstractPlayer
from move import Move


class AIPlayer(AbstractPlayer, ABC):
    def __init__(self, name, difficulty):
        super().__init__(name)
        self.first = False

    def type(self):
        return 'AI'

    def make_move(self, row, column):
        if self.first:
            return [3, 5]
        else:
            return [2, 5]
