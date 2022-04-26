import copy
import random
import socket
import pickle
import threading
import uuid
from queue import Queue
from Controller.message import ReversiMessage as msg
import time
from Model.database import Database

TIMEOUT = 60
TOLERANCE = 20  # not sure what this should actually be but i'll figure it out
event = threading.Event()


class ReversiServer:
    def __init__(self, host='127.0.0.1', port=1235, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.occupants = []
        self.move_queues = dict()
        self.queueing = []
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
                queue = Queue(5)
                thread = threading.Thread(target=self.handle_client, args=(conn, queue))
                thread.start()
                thread.join()

    # do we need queues???
    def handle_client(self, conn, move_queue: Queue):
        """
        Handles sending and receiving messages to/from the client.
        :param conn: The client connection.
        :param uid: Client UID
        :param move_queue: queue used for receiving opponents' moves
        :return: Nothing
        """
        with conn:
            # if not self.move_queues[address]:
            #     id_binary = pickle.dumps([address])
            #     conn.sendall(id_binary)
            #     print('sent address')

            while True:
                # Check if we have received any messages to transmit
                if not move_queue.empty():
                    move = move_queue.get()
                    rsp = pickle.dumps(move)
                    conn.sendall(rsp)
                    print('sent a message to client')

                try:
                    # Check the buffer to see if there has been any received messages
                    ex_binary = conn.recv(self.buffer_size)
                    print('received message')
                    if not ex_binary:
                        break
                    ex = pickle.loads(ex_binary)
                    rsp = self.parse_msg(ex, move_queue)
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
            if len(self.queueing) > 1:
                print('checking for matches')
                # we don't want to modify the server copy.
                queue = copy.deepcopy(self.queueing)
                queue.sort(key=lambda e: e[1])

                # boot anyone queueing for more than TIMEOUT seconds
                for p in queue:
                    if time.time() - p[3] > TIMEOUT:
                        q = self.move_queues.get(p[0])
                        q.put(msg('mm_resp', [False]))
                        self.move_queues[p[0]] = None

                # attempt to pair players
                for i in range(1, len(queue) - 1, 2):
                    player = queue[i]
                    # pairs with neighbor with smallest elo difference (while less than TOLERANCE)
                    opp = queue[i - 1] if abs(player[1] - queue[i - 1][1]) < abs(player[1] - queue[i + 1][1]) else \
                        queue[
                            i + 1]
                    if abs(player[1] - opp[1]) < TOLERANCE:
                        print('found match')
                        # send mm_resp
                        q = self.move_queues.get(player[0])
                        q.put(msg('mm_resp', [True, opp[0]]))
                        print(f'queue size player {q.qsize()}')
                        q = self.move_queues.get(opp[0])
                        q.put(msg('mm_resp', [True, player[0]]))
                        print(f'queue size opp {q.qsize()}')
                        # remove from queue
                        self.queueing.remove(player)
                        self.queueing.remove(opp)
                        queue.remove(player)
                        queue.remove(opp)
                        self.move_queues[player[0]] = None
                        self.move_queues[opp[0]] = None
                        self.db.write_update_game_start()
            event.wait(5)

    def parse_msg(self, request: msg, msg_queue):
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
        }.get(msg_type)(params, msg_queue)

    """
    Defining a request callback:
    all callbacks must have the same signature (self, params: list)
    Each callback must return a response to the client.
    If no information needs to be returned, an ack: `msg('ack', [success?])` works.
    `params` can be unused, but bust be a parameter.
    """
    # Done
    def get_elo(self, params: list, msg_queue: Queue):
        """
        Returns the current user's elo
        :param params: [the player's username]
        :return: a 'send_elo' message with param [user elo]
        """
        # query db for elo rating
        username = params[0]
        return [self.db.fetch_user_data()[username].get('elo')]

    """
    Temporary functions for calculating elo
    """
    def expected_win(self, opponent):
        """
        Calculates the expected win rate of player (self) against the opponent
        :param opponent: opponent's name
        :return: player's expected win rate
        """
        playerELO = self.db.fetch_data(self).get("elo")
        opponentELO = self.db.fetch_data(opponent).get("elo")
        exponent = (opponentELO - playerELO) / 400
        probability = 1 / (1 + pow(10, exponent))
        return probability

    """
    expected in the parameter is the probability from the above functions
    maybe we can add another thing to the database that shows the expected_win rate of that player
    not sure if it's "safe" to have a variable in the server that keeps track of that instead
    """
    def updated_elo(self, result, expected):
        """
        Calculates change in ELO rating
        :param result: Result of game (0 = lose; 0.5 = draw; 1 = win)
        :param expected: Expected probability to win (from expected_win)
        :return: updated ELO rating
        """
        playerELO = self.db.fetch_data(self).get("elo")
        k = 32
        newELO = k * (result - expected)
        return playerELO + newELO

    def leaderboard(self, params: list, msg_queue: Queue):
        """
        Potentially unneeded.
        Meant to update the elo ranking for a player.
        However, this might be handled by the server.
        :param params: [username, elo]
        :return: an ack with param [success?]
        """
        # update elo rating after game
        return [self.db.sorted_leaderboard()]

    def register(self, params: list, msg_queue: Queue):
        """
        Handles registration for an account
        :param params: [username, password]
        :return:
        """
        username, password = params
        return [self.db.write_user(username, password)]

    # Finished
    def get_players(self, params: list, msg_queue: Queue):
        """
        Returns the players currently online, along with their UID, elo, and username
        :param params: []
        :return: a 'send_players' message with param [[(username, uid, elo)]] (param[0] is the list of players)
        """
        return [self.occupants]

    def update_game_state(self, params: list, msg_queue: Queue):
        """
        Updates database with last played move to corresponding game
        :param params: [game_id, last_player, move]
        """
        self.db.write_update_turn(params[0], params[1], params[2])

    def update_game_complete(self, params: list, msg_queue: Queue):
        """
        Removes game instance from database if not done so already
        :param params: [game_id, winner, winner_elo, winner_hs, loser, loser_elo, loser_hs]
        """
        if self.db.fetch_game_data(params[0]):
            self.db.write_update_game_complete(game_id=params[0])
            self.db.write_update_users_complete(winner=params[1], winner_elo=params[2], winner_hs=params[3],
                                                loser=params[4], loser_elo=params[5], loser_hs=params[6])

    # Unfinished
    def send_move(self, params: list, msg_queue: Queue):
        """
        Receives a move from a player and routes it to their opponent.
        :param params: [opponent_uid, move]
        :return: ack describing success
        """
        try:
            q = self.move_queues.get(params[0])
            q.put(msg('send_move', params))
            return msg('ack', [True])
        except:
            return msg('ack', [False])

    def log_in_request(self, params: list, msg_queue: Queue):
        """
        Handles a client request to log in.
        On success adds players to the online roster.
        :param params: [username, password, uid]
        :return: ack on success
        """
        username, password, uid = params
        if self.db.verify_credentials(username, password):
            self.occupants.append(username)
            return [True]
        return [False]

    # Finished (kinda)
    def match_make(self, params: list, msg_queue: Queue):
        """
        Initiates matchmaking for a player
        :param msg_queue: message queue used to return the message
        :param params: [username, uid, elo]
        :return: ack
        """
        curr_username, opp_username, elo = params
        curr_time = time.time()
        self.move_queues[curr_username] = msg_queue
        self.queueing.append((curr_username, elo, curr_time))



if __name__ == '__main__':
    server = ReversiServer()
    server.start()