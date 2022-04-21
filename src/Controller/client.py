import socket
import pickle
from msg import ReversiMessage as msg


class ReversiClient:
    def __init__(self, host='127.0.0.1', port=1234, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

    def start(self):
        with socket.socket() as my_socket:
            my_socket.connect((self.host, self.port))
            print('Client Connected')

            messages = [
                msg('get_elo', []),
                msg('set_elo', []),
                msg('get_players', []),
                msg('add_player', []),
                msg('rcv_move', [])]

            for m in messages:
                m_binary = pickle.dumps(m)
                my_socket.sendall(m_binary)

                result_binary = my_socket.recv(self.buffer_size)
                result = pickle.loads(result_binary)
                print(result)


if __name__ == '__main__':
    client = ReversiClient()
    client.start()

