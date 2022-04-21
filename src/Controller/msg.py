class ReversiMessage:
    # add documentation here
    msg_types = ['get_elo', 'set_elo', 'get_players', 'add_player', 'send_move', 'rcv_move']

    def __init__(self, msg_type: str, params: list):
        assert(msg_type in ReversiMessage.msg_types)
        self.type = msg_type
        self.params = params

    def get_type(self):
        return self.type

    def get_params(self):
        return self.params