import socket
import pickle
from msg import ReversiMessage as msg
from queue import Queue


class ReversiClient:
    def __init__(self, host='127.0.0.1', port=1234, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.out_queue = Queue(15)
        self.uid = None
        self.in_game = True

    def start(self):
        """
        Starts the main loop for the client.
        Expects to receive a UID value from the server
        Has a buffer 'out_queue' which receives messages to be sent
        Must be run in a separate thread?
        :return: Nothing
        """
        with socket.socket() as my_socket:
            my_socket.connect((self.host, self.port))
            print('Client Connected')
            # retrieve uid
            uid_binary = my_socket.recv(self.buffer_size)
            uid = pickle.loads(uid_binary)
            self.parse_response(uid)

            # start main loop
            while True:
                if not self.out_queue.empty():
                    m = self.out_queue.get()
                    m_binary = pickle.dumps(m)
                    my_socket.sendall(m_binary)

                result_binary = my_socket.recv(self.buffer_size)
                if not result_binary:
                    break
                result = pickle.loads(result_binary)
                self.parse_response(result)

    def parse_response(self, rsp: msg):
        """
        Handles callbacks for server requests
        Callbacks are defined the same as server callbacks.
        :param rsp: the response.
        :return: None
        """

        print('response received')
        msg_type = rsp.get_type()
        params = rsp.params
        return {
            'send_elo': self.send_elo,
            'send_leaderboard': self.send_leaderboard,
            'send_players': self.send_players,
            'send_move': self.send_move,
            'ack': self.ack,
            'log_in_resp': self.log_in_resp,
            'send_uid': self.send_uid,
            'mm_resp': self.mm_resp,
        }.get(msg_type)(params)

    def send_elo(self, params: list):
        """
        Handles receiving ELO rating from the server.
        :param params: [ELO]
        :return:
        """
        pass

    def send_leaderboard(self, params: list):
        """
        Receives the leaderboard from the server
        :param params: [leaderboard] (unimplemented on server-side)
        :return:
        """
        pass

    def send_players(self, params: list):
        """
        Receives the list of current players online
        :param params: [players] (see server->get_players() for more info)
        :return:
        """
        pass

    def send_move(self, params: list):
        """
        Receives opposing player's move
        :param params: [move]
        :return:
        """
        print(f'received a move with uid {params[0]}')

    def ack(self, params: list):
        """
        Used to check success of requests.
        :param params: [success?]
        :return:
        """
        print(f'received ack with value {params[0]}')

    def log_in_resp(self, params: list):
        """
        Handles response from log-in.
        Currently unimplemented
        :param params: unknown
        :return:
        """
        pass

    def send_uid(self, params: list):
        """
        Receives UID from server.
        :param params: [UID]
        :return:
        """
        self.uid = params[0]

    def mm_resp(self, params: list):
        """
        Handles response from matchmaking request
        :param params: [success?, opponent_UID?] opponent_UID only sent on successful mm.
        :return:
        """
        if params[0]:
            print(f'Received match with {params[1]}')
        else:
            print(f'matchmaking failed')


if __name__ == '__main__':
    client = ReversiClient()
    client.start()
