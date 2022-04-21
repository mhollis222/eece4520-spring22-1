import socket
import pickle
import threading
from queue import Queue
from msg import ReversiMessage as msg


class ReversiServer:
    def __init__(self, host='127.0.0.1', port=1234, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.occupants = []

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server Started')

            while True:
                conn, address = my_socket.accept()
                i_buff = Queue()
                o_buff = Queue()
                print(f'Connected by {address}')
                thread = threading.Thread(target=self.handle_client, args=(conn, i_buff, o_buff,))
                thread.start()

    # do we need queues???
    def handle_client(self, conn, i_buff: Queue, o_buff: Queue):
        with conn:
            while True:
                ex_binary = conn.recv(self.buffer_size)
                if not ex_binary:
                    break
                ex = pickle.loads(ex_binary)
                rsp = self.parse_msg(ex)
                rsp_binary = pickle.dumps(rsp)
                conn.sendall(rsp_binary)
            print('Client Disconnected')

    def parse_msg(self, msg: msg):
        msg_type = msg.get_type()
        params = msg.get_params()
        return {
            'get_elo': self.get_elo(params),
            'set_elo': self.set_elo(params),
            'get_players': self.get_players(params),
            'add_player': self.add_player(params),
            'rcv_move': self.rcv_move(params)

        }.get(msg_type)

    def get_elo(self, params: list):
        return 'getting_elo'

    def set_elo(self, params: list):
        return 'setting_elo'

    def get_players(self, params: list):
        return 'getting_players'

    def add_player(self, params: list):
        return 'adding_player'

    def rcv_move(self, params: list):
        return 'receiving_move'


if __name__ == '__main__':
    server = ReversiServer()
    server.start()
