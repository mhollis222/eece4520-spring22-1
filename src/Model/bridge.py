import socket


class Bridge:
    def __init__(self, host='127.0.0.1', port=1234):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket as db_socket:
            db_socket.connect((self.host, self.port))
            # TODO: create payload
            message = "Dummy payload"
            message.encode('utf-8')
            db_socket.sendall(message)
            print("Message sent to server")
