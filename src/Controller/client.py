import socket
import pickle
from Controller.message import ReversiMessage as msg


class ReversiClient:
    _instance = None

    def __new__(cls, host='127.0.0.1', port=1234, buffer_size=1024):
        """
        Creates a new outgoing queue for the client. Only one should ever exist.
        Should be importable from any file and used where needed.
        :param size: the size for our queue.
        """

        if cls._instance is None:
            print('creating client singleton')
            cls._instance = super(ReversiClient, cls).__new__(cls)
            cls._instance.host = host
            cls._instance.port = port
            cls._instance.buffer_size = buffer_size
            cls._instance.uid = None
            cls._instance.socket = None
            cls._instance.username = None

        return cls._instance

    def send_request(self, req: msg) -> list:
        with socket.socket() as my_socket:
            my_socket.connect((self.host, self._instance.port))
            my_socket.settimeout(5)
            m_binary = pickle.dumps(req)
            my_socket.sendall(m_binary)
            print(f'sent message {req}')
            try:
                result_binary = my_socket.recv(self.buffer_size)
                result = pickle.loads(result_binary)
                print(f'received message {result}')
                return result
            except socket.timeout:
                return 'TIMEOUT'

