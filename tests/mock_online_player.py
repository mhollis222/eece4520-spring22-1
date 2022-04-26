from abc import ABC

from abstract_player import AbstractPlayer
from move import Move


class OnlinePlayer(AbstractPlayer, ABC):
    def __init__(self, name, game_id, human_name):
        super().__init__(name)
        self.first = False

    def type(self):
        return 'Online'

    def make_move(self, row, column):
        if self.first:
            return Move(5, 3)
        else:
            return Move(5, 2)
