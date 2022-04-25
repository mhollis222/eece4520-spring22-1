class ReversiMessage:
    #####################################################
    # Requests
    # get_elo: params = [current player]
    # set_elo: params = [current player, elo]
    # get_players: params = [None]
    # send_move: params = [opponent_uid, move]
    # rcv_move: params = [None]
    # log_in: params = [username, password, uid]
    # request_game: params = [local username, local uid, elo]
    # challenge_player: params = [opposing player uid]
    #####################################################
    # Responses

    requests = ['get_elo', 'set_elo', 'get_players', 'send_move', 'log_in', 'request_game', 'test']

    def __init__(self, msg_type: str, params: list):
        assert(msg_type in ReversiMessage.requests)
        self.type = msg_type
        self.params = params

    def get_type(self):
        return self.type

    def get_params(self):
        return self.params

    def __str__(self):
        return f'msg_type: {self.type} params: {self.params}'
