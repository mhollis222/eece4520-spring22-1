import copy
import random
import socket
import pickle
import threading
from queue import Queue
from Controller.message import ReversiMessage as msg
import time
from Model.database import Database

TIMEOUT = 30
TOLERANCE = 500  # not sure what this should actually be but i'll figure it out
event = threading.Event()


class ReversiServer:
    def __init__(self, host='127.0.0.1', port=1234, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.occupants = []
        self.move_queues = dict()
        self.queueing = []
        self.challenges = []
        self.db = Database('localhost', 'reversi', 'eece4520')

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server Started')

            mm_thread = threading.Thread(target=self.match_making)
            mm_thread.start()

            while True:
                conn, address = my_socket.accept()
                conn.settimeout(5)
                print(f'Connected by {address}')
                thread = threading.Thread(target=self.handle_client, args=[conn])
                thread.start()

    # do we need queues???
    def handle_client(self, conn):
        """
        Handles sending and receiving messages to/from the client.
        :param conn: The client connection.
        :param uid: Client UID
        :param move_queue: queue used for receiving opponents' moves
        :return: Nothing
        """
        with conn:
            while True:
                try:
                    # Check the buffer to see if there has been any received messages
                    ex_binary = conn.recv(self.buffer_size)
                    print('received message')
                    if not ex_binary:
                        break
                    ex = pickle.loads(ex_binary)
                    rsp = self.parse_msg(ex)
                    if rsp:
                        rsp_binary = pickle.dumps(rsp)
                        conn.sendall(rsp_binary)
                        print('sent a message to client')
                # If no messages are received for 5 seconds, loop
                except socket.timeout:
                    pass
            print('Client Disconnected')

    def match_making(self):
        """
        This function runs in a separate thread to the client threads.
        It loops infinitely checking to see if the players can be matched.
        Uses two tunable constants:  TIMOUT and TOLERANCE
        TIMEOUT - The amount of time (seconds) a player can be queueing before it fails.
        TOLERANCE - How much of a gap is allowed between elo rankings for a game to be valid
            abs(p1.elo - p2.elo) < TOLERANCE
        Once a match has been found it will send a message to each player with their opponents uid.
        This allows us to properly route move messages to their correct client.
        Sends 'mm_resp' to clients with params [success?, opponent_UID]
        opponent_UID is not sent if success is False
        :return: Nothing
        """
        while True:
            if len(self.challenges) > 1:
                p1 = self.challenges[0]
                p2 = self.challenges[1]
                if p1[1] == p2[0] and p1[0] == p2[1]:
                    game_id = self.db.write_update_game_start([p1[0], p2[0]])
                    q = self.move_queues.get(p1[0])
                    q.put([p2[0], game_id])
                    q = self.move_queues.get(p2[0])
                    q.put([p1[0], game_id])
            if len(self.queueing) > 1:
                print('checking for matches')
                # we don't want to modify the server copy.
                queue = copy.deepcopy(self.queueing)
                queue.sort(key=lambda e: e[1])

                # boot anyone queueing for more than TIMEOUT seconds
                for p in queue:
                    if time.time() - p[2] > TIMEOUT:
                        q = self.move_queues.get(p[0])
                        q.put(['MATCH_NOT_FOUND'])
                        self.move_queues[p[0]] = None

                # attempt to pair players
                if len(queue) == 2:
                    print('found match')
                    player = queue[0]
                    opp = queue[1]
                    # send mm_resp
                    order = [player[0], opp[0]] if random.Random().random() > 0.5 else [opp[0], player[0]]
                    game_id = self.db.write_update_game_start(order)
                    q = self.move_queues.get(player[0])
                    q.put([opp[0], game_id, order])
                    print(f'queue size player {q.qsize()}')
                    q = self.move_queues.get(opp[0])
                    q.put([player[0], game_id, order])
                    print(f'queue size opp {q.qsize()}')
                    # remove from queue
                    self.queueing.remove(player)
                    self.queueing.remove(opp)
                    queue.remove(player)
                    queue.remove(opp)
                else:
                    for i in range(1, len(queue) - 1, 2):
                        player = queue[i]
                        # pairs with neighbor with smallest elo difference (while less than TOLERANCE)
                        opp = queue[i - 1] if abs(player[1] - queue[i - 1][1]) < abs(player[1] - queue[i + 1][1]) else \
                            queue[
                                i + 1]
                        if abs(player[1] - opp[1]) < TOLERANCE:
                            print('found match')
                            # send mm_resp
                            order = [player[0], opp[0]] if random.Random().random() > 0.5 else [opp[0], player[0]]
                            game_id = self.db.write_update_game_start(order)
                            q = self.move_queues.get(player[0])
                            q.put(msg('mm_resp', [opp[0], game_id, order]))
                            print(f'queue size player {q.qsize()}')
                            q = self.move_queues.get(opp[0])
                            q.put(msg('mm_resp', [player[0], game_id, order]))
                            print(f'queue size opp {q.qsize()}')
                            # remove from queue
                            self.queueing.remove(player)
                            self.queueing.remove(opp)
                            queue.remove(player)
                            queue.remove(opp)
            event.wait(5)

    def parse_msg(self, request: msg):
        """
        Handles how client requests are handled by the server.
        It matches the request type to its appropriate callback.
        See get_elo() for info on how to implement this.
        :param request: The incoming request.
        :return: server response as generated by each callback.
        """
        msg_type = request.get_type()
        params = request.get_params()
        return {
            'get_elo': self.get_elo,
            'leaderboard': self.leaderboard,
            'get_players': self.get_players,
            'send_move': self.send_move,
            'request_game': self.match_make,
            'register': self.register,
            'log_in': self.log_in_request,
            'update_game_state': self.update_game_state,
            'get_game_state': self.get_game_state,
            'update_game_complete': self.update_game_complete,
            'expected_win': self.expected_win,
            'updated_elo': self.updated_elo,
            'challenge': self.challenge,
            'rcv_message': self.receive,
            'get_game_participants': self.get_game_participants,
            'get_game_by_user': self.get_game_by_user,
        }.get(msg_type)(params)

    """
    Defining a request callback:
    all callbacks must have the same signature (self, params: list)
    Each callback must return a response to the client.
    If no information needs to be returned, an ack: `msg('ack', [success?])` works.
    `params` can be unused, but bust be a parameter.
    """
    # Done
    def get_elo(self, params: list):
        """
        Returns the current user's elo
        :param params: [the player's username]
        :return: a 'send_elo' message with param [user elo]
        """
        # query db for elo rating
        username = params[0]
        for user in self.db.fetch_user_data():
            if user.get("username") == username:
                return [user.get("elo")]
        return ['Error']

    def challenge(self, params: list):
        """
        Challenges a player
        """
        local, online = params
        curr_time = time.time()
        self.queueing.append((local, online, curr_time))


    """
    Temporary functions for calculating elo
    """
    def expected_win(self, params: list):
        """
        Calculates the expected win rate of player (self) against the opponent
        :param params: [username, opponent]
        :return: player's expected win rate
        """
        for user in self.db.fetch_user_data():
            if user.get("username") == params[0]:
                playerELO = user.get("elo")
            if user.get("username") == params[1]:
                opponentELO = user.get("elo")
        exponent = (opponentELO - playerELO) / 400
        probability = 1 / (1 + pow(10, exponent))
        return [probability]

    """
    expected in the parameter is the probability from the above functions
    maybe we can add another thing to the database that shows the expected_win rate of that player
    not sure if it's "safe" to have a variable in the server that keeps track of that instead
    """
    def updated_elo(self, params: list):
        """
        Calculates change in ELO rating
        :param params: [Result of game (0 = lose; 0.5 = draw; 1 = win), Expected probability to win (from expected_win)]
        :return: updated ELO rating
        """
        for user in self.db.fetch_user_data():
            if user.get("username") == params[0]:
                playerELO = user.get("elo")
        k = 32
        newELO = k * (params[0] - params[1])
        return [playerELO + newELO]

    def leaderboard(self, params: list):
        """
        Potentially unneeded.
        Meant to update the elo ranking for a player.
        However, this might be handled by the server.
        :param params: [username, elo]
        :return: an ack with param [success?]
        """
        # update elo rating after game
        return [self.db.sorted_leaderboard()]

    def register(self, params: list):
        """
        Handles registration for an account
        :param params: [username, password]
        :return:
        """
        username, password = params
        self.move_queues[username] = Queue(5)
        self.occupants.append(username)
        return [self.db.write_user(username, password)]

    # Finished
    def get_players(self, params: list):
        """
        Returns the players currently online, along with their UID, elo, and username
        :param params: []
        :return: a 'send_players' message with param [[(username, uid, elo)]] (param[0] is the list of players)
        """
        return [self.occupants]

    def update_game_state(self, params: list):
        """
        Updates database with last played move to corresponding game
        :param params: [game_id, last_player, move]
        """
        self.db.write_update_turn(params[0], params[1], params[2])

    def get_game_state(self, params: list):
        """
        Retrieves move list corresponding to requested game
        :param params: [game_id]
        :return: list of type Move
        """
        return [self.db.fetch_game_data(params[0]).get("gamestate"),
                self.db.fetch_game_data(params[0]).get("lastactiveplayer")]

    def get_game_participants(self, params: list):
        """
        Retrieves participants list corresponding to requested game
        :param params: [game_id]
        :return: list of usernames (2)
        """
        return [self.db.fetch_game_data(params[0]).get("players")]

    def get_game_by_user(self, params: list):
        """
        Retrieves game id based on username
        :param params: [username]
        :return: game id
        """
        return [self.db.find_game_by_user(params[0])]

    def update_game_complete(self, params: list):
        """
        Removes game instance from database if not done so already
        :param params: [game_id, winner, winner_elo, winner_hs, loser, loser_elo, loser_hs]
        """
        if self.db.fetch_game_data(params[0]):
            self.db.write_update_game_complete(game_id=params[0])
            self.db.write_update_users_complete(winner=params[1], winner_elo=params[2], winner_hs=params[3],
                                                loser=params[4], loser_elo=params[5], loser_hs=params[6])

    # Unfinished
    def send_move(self, params: list):
        """
        Receives a move from a player and routes it to their opponent.
        :param params: [opponent_user, current_user, move]
        :return: ack describing success
        """
        try:
            q = self.move_queues.get(params[0])
            q.put(params[2])
            print('message added successfuly')
            return ['hi']

        except:
            return [-1]

    def log_in_request(self, params: list):
        """
        Handles a client request to log in.
        On success adds players to the online roster.
        :param params: [username, password, uid]
        :return: ack on success
        """
        username, password = params
        if self.db.verify_credentials(username, password):

            self.move_queues[username] = Queue(5)
            self.occupants.append(username)
            return [True]
        return [False]

    # Finished (kinda)
    def match_make(self, params: list):
        """
        Initiates matchmaking for a player
        :param msg_queue: message queue used to return the message
        :param params: [username, uid, elo]
        :return: ack
        """
        curr_username, elo = params
        curr_time = time.time()
        self.queueing.append((curr_username, elo, curr_time))
        return ['matchmaking_started']

    def receive(self, params: list):
        q: Queue = self.move_queues.get(params[0])
        print('checking for messages')
        if not q.empty():
            return q.get()


if __name__ == '__main__':
    server = ReversiServer()
    server.start()
