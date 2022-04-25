from Model.abstract_player import AbstractPlayer
from Model.move import Move


class OnlinePlayer(AbstractPlayer):

    def make_move(self, row: str, column: str):
        return Move(int(row), int(column))

    def add_move(self, move: Move):
        self.history.append(move)

    def type(self):
        return 'Online'
