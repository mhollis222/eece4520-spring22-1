class ReversiMessage:
    #####################################################
    # Requests
    # get_elo: params = [username]
    # set_elo: params = [username, elo]
    # get_players: params = [None]
    # update_game_state = [game_id, last_player, move]
    # update_game_complete = [game_id, winner, winner_elo, winner_hs, loser, loser_elo, loser_hs]
    # send_move: params = [opponent_uid, move, game_id]
    # log_in: params = [username, password, uid]
    # request_game: params = [local username, local uid, elo]
    # challenge_player: params = [opposing player uid]
    #####################################################
    # Responses

    requests = ['get_elo', 'leaderboard', 'get_players', 'send_move', 'log_in', 'request_game', 'register']

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
