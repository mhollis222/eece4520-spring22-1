import pickle
import socket
import threading


class DatabaseServer:
    def __init__(self, host='127.0.0.1', port=1234, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

    def start(self):
        with socket.socket as db_socket:
            db_socket.bind(address=(self.host, self.port))
            db_socket.listen()
            print("Server started")
            while True:
                conn, address = db_socket.accept()
                print(f'Connected by {address}')
                thread = threading.Thread(target=self.handle_client, args=(conn,))
                thread.start()

    def handle_client(self, conn):
        with conn:
            while True:
                ex_binary = conn.recv(self.buffer_size)
                if not ex_binary:
                    break
                ex = pickle.loads(ex_binary)
                print(f'Received payload: {ex}')
                # TODO: interpret payload and execute accordingly


if __name__ == '__main__':
    server = DatabaseServer()
    server.start()
