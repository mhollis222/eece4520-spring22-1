from Model.abstract_player import AbstractPlayer
from Model.move import Move
from Controller.client import ReversiClient
from Controller.message import ReversiMessage as msg


class OnlinePlayer(AbstractPlayer):
    def __init__(self, name, game_id):
        """
        Creates the online player
        :param name: MUST be the opposing players username
        """
        super(OnlinePlayer, self).__init__(name)
        self.client = ReversiClient()
        self.game_id = game_id

    def make_move(self, row: int, column: int):
        message = msg('send_move', [self.name, Move(row, column), self.game_id])
        response = self.client.send_request(message)
        return response[0]

    def add_move(self, move: Move):
        self.history.append(move)

    def type(self):
        return 'Online'
