import socket
import pickle
import threading
import uuid
from queue import Queue
from msg import ReversiMessage as msg


class ReversiServer:
    def __init__(self, host='127.0.0.1', port=1234, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.occupants = []
        self.move_queues = {}

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server Started')

            while True:
                conn, address = my_socket.accept()
                uid = uuid.uuid4()
                queue = Queue(5)
                self.move_queues[uid] = queue
                print(f'Connected by {address}')
                thread = threading.Thread(target=self.handle_client, args=(conn, uid, queue))
                thread.start()

    # do we need queues???
    def handle_client(self, conn, uid, move_queue: Queue):
        with conn:
            id_message = msg('send_uid', [uid])
            id_binary = pickle.dumps(id_message)
            conn.sendall(id_binary)

            while True:
                if not move_queue.empty():
                    move = move_queue.get()
                    rsp = pickle.dumps(move)
                    conn.sendall(rsp)
                    print('sent a move to client')

                ex_binary = conn.recv(self.buffer_size)
                if not ex_binary:
                    break
                ex = pickle.loads(ex_binary)
                rsp = self.parse_msg(ex, move_queue)
                rsp_binary = pickle.dumps(rsp)
                conn.sendall(rsp_binary)
                print('sent a message to client')
            print('Client Disconnected')

    def parse_msg(self, message: msg, move_queue):
        msg_type = message.get_type()
        params = message.get_params()
        return {
            'get_elo': self.get_elo,
            'set_elo': self.set_elo,
            'get_players': self.get_players,
            'send_move': self.send_move,
        }.get(msg_type)(params, move_queue)

    def get_elo(self, params: list, move_queue: Queue):
        # query db for elo rating
        return msg('send_elo', [0])

    def set_elo(self, params: list, move_queue: Queue):
        # update elo rating after game
        if True: #if sucessful
            return msg('ack', [True])
        return msg('ack', [False])

    def get_players(self, params: list, move_queue: Queue):
        return msg('send_players', [self.occupants])

    def send_move(self, params: list, move_queue: Queue):
        try:
            q = self.move_queues.get(params[0])
            q.put(msg('send_move', params))
            return msg('ack', [True])
        except:
            return msg('ack', [False])


    def log_in_request(self, params: list, move_queue: Queue):
        username, password, uid = params

        # check db with username and password
        #if successful
        self.occupants.append((username, uid))
        return msg('ack', [True])



if __name__ == '__main__':
    server = ReversiServer()
    server.start()
