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
        with socket.socket() as my_socket:
            my_socket.connect((self.host, self.port))
            print('Client Connected')
            # retrieve uid
            uid_binary = my_socket.recv(self.buffer_size)
            uid = pickle.loads(uid_binary)
            self.parse_response(uid)

            test1 = msg('send_move', [1234, 5])
            test2 = msg('send_move', [self.uid, 6])

            self.out_queue.put(test1)
            self.out_queue.put(test2)
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
        }.get(msg_type)(params)

    def send_elo(self, params: list):
        pass

    def send_leaderboard(self, params: list):
        pass

    def send_players(self, params: list):
        pass

    def send_move(self, params: list):
        print(f'received a move with uid {params[0]}')

    def ack(self, params: list):
        print(f'received ack with value {params[0]}')

    def log_in_resp(self, params: list):
        pass

    def send_uid(self, params: list):
        self.uid = params[0]


if __name__ == '__main__':
    client = ReversiClient()
    client.start()
