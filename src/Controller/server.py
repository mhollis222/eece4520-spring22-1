import copy
import random
import socket
from socket import MSG_DONTWAIT
import pickle
import threading
import uuid
from queue import Queue
from msg import ReversiMessage as msg
import time

TIMEOUT = 30
TOLERANCE = 20  # not sure what this should actually be but i'll figure it out
event = threading.Event()

class ReversiServer:
    def __init__(self, host='127.0.0.1', port=1234, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.occupants = []
        self.move_queues = dict()
        self.queueing = []

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()
            print('Server Started')

            mm_thread = threading.Thread(target=self.match_making)
            mm_thread.start()

            threads = []

            while True:
                conn, address = my_socket.accept()
                conn.settimeout(5)
                uid = uuid.uuid4()
                queue = Queue(5)
                self.move_queues[uid] = queue
                print(f'Connected by {address}')
                thread = threading.Thread(target=self.handle_client, args=(conn, uid, queue))
                threads.append(thread)
                thread.start()

    # do we need queues???
    def handle_client(self, conn, uid, move_queue: Queue):
        with conn:
            id_message = msg('send_uid', [uid])
            id_binary = pickle.dumps(id_message)
            conn.sendall(id_binary)

            while True:
                print(f'queue size: {move_queue.qsize()}')
                if not move_queue.empty():
                    move = move_queue.get()
                    rsp = pickle.dumps(move)
                    conn.sendall(rsp)
                    print('sent a message to client')

                try:
                    ex_binary = conn.recv(self.buffer_size)
                    if not ex_binary:
                        break
                    ex = pickle.loads(ex_binary)
                    rsp = self.parse_msg(ex, move_queue)
                    rsp_binary = pickle.dumps(rsp)
                    conn.sendall(rsp_binary)
                    print('sent a message to client')
                except socket.timeout:
                    pass
            print('Client Disconnected')

    def match_making(self):
        while True:
            if len(self.queueing) > 1:
                print('checking for matches')
                queue = copy.deepcopy(self.queueing)
                queue.sort(key=lambda e: e[2])

                # boot anyone queueing for more than 5 minutes
                for p in queue:
                    if time.time() - p[3] > TIMEOUT:
                        q = self.move_queues.get(p[1])
                        q.put(msg('mm_resp', [False]))


                # attempt to pair players
                for i in range(1, len(queue) - 1, 2):
                    player = queue[i]
                    # attempt to pair with closest player
                    opp = queue[i - 1] if abs(player[2] - queue[i - 1][2]) < abs(player[2] - queue[i + 1][2]) else queue[
                        i + 1]
                    if abs(player[2] - opp[2]) < TOLERANCE:
                        print('found match')
                        # send mm_resp
                        q = self.move_queues.get(player[1])
                        q.put(msg('mm_resp', [True, opp[1]]))
                        print(f'queue size player {q.qsize()}')
                        q = self.move_queues.get(opp[1])
                        q.put(msg('mm_resp', [True, player[1]]))
                        print(f'queue size opp {q.qsize()}')
                        # remove from queue
                        self.queueing.remove(player)
                        self.queueing.remove(opp)
                        queue.remove(player)
                        queue.remove(opp)

            event.wait(5)

    def parse_msg(self, message: msg, move_queue):
        msg_type = message.get_type()
        params = message.get_params()
        return {
            'get_elo': self.get_elo,
            'set_elo': self.set_elo,
            'get_players': self.get_players,
            'send_move': self.send_move,
            'request_game': self.match_make,
        }.get(msg_type)(params, move_queue)

    def get_elo(self, params: list, move_queue: Queue):
        # query db for elo rating
        return msg('send_elo', [0])

    def set_elo(self, params: list, move_queue: Queue):
        # update elo rating after game
        if True:  # if sucessful
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
        # if successful
        # get their elo
        elo = random.randint(0, 100)
        self.occupants.append((username, uid, elo))
        return msg('ack', [True])

    def match_make(self, params: list, move_queue: Queue):
        username, uid, elo = params
        curr_time = time.time()
        self.queueing.append((username, uid, elo, curr_time))
        return msg('ack', [True])


if __name__ == '__main__':
    server = ReversiServer()
    server.start()
