from abstract_player import AbstractPlayer
from Model.move import Move


class HumanPlayer(AbstractPlayer):

    @staticmethod
    def make_move(row, column):
        return Move(int(row), int(column))
