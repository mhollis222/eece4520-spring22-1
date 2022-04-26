from Model.abstract_player import AbstractPlayer
from Model.move import Move
from Controller.client import ReversiClient
from Controller.message import ReversiMessage as msg


class OnlinePlayer(AbstractPlayer):
    def __init__(self, name, game_id, human_name):
        """
        Creates the online player
        :param name: MUST be the opposing players username
        """
        super(OnlinePlayer, self).__init__(name)
        self.client = ReversiClient()
        self.game_id = game_id
        self.human_player = human_name

    def make_move(self, row, column):
        pass

    def send_move(self, move: Move):
        message = msg('send_move', [self.name, self.human_player, move, self.game_id])
        return self.client.send_request(message)

    def get_move(self):
        message = msg('rcv_message', [self.human_player])
        return self.client.send_request(message)

    def add_move(self, move: Move):
        self.history.append(move)

    def type(self):
        return 'Online'
