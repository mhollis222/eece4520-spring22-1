from AbstractPlayer import AbstractPlayer
from enum import Enum
from random import random
from Move import Move


class Cell(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class Game:

    def __init__(self, p1: AbstractPlayer, p2: AbstractPlayer, x: int = 8, y: int = 8):
        self.p1 = p1
        self.p2 = p2
        self.x = x
        self.y = y
        self.board = [[Cell.EMPTY for x in range(self.x)] for y in range(self.y)]
        self.order = []
        self.running = False
        self.round = 0

    def _coin_flip(self) -> [AbstractPlayer, AbstractPlayer]:
        """
        simulates a coin flip to decide which player goes first
        :return: the player to go first
        """
        if random() > 0.5:
            self.p1.identifier = 1
            self.p2.identifier = 2
            return [self.p1, self.p2]
        self.p1.identifier = 2
        self.p2.identifier = 1
        return [self.p2, self.p1]

    def validate_move(self, move: Move, play: AbstractPlayer) -> bool:
        """
        makes sure the desired move is in fact possible.
        :param move: The player requested move
        :param play: Player making move
        :return: valid?
        """
        # if this move is found in the list of valid moves at least once, return true
        if self._get_valid_moves(play).count(move) > 0:
            return True
        return False

    def _get_valid_moves(self, play: AbstractPlayer) -> list:
        """
        obtain cell locations for valid moves
        :param play: Player making move
        :return: list of locations on board (list:tuple)
        """
        board_size = max(self.x, self.y)  # 1D board size in event of asymmetrical board
        valid = []
        for x in range(self.x):
            for y in range(self.y):
                if self.board[x][y].value == play.identifier:
                    for dire in range(8):
                        flag = False
                        for dist in range(1, board_size):
                            location = Game._get_cardinal_location((x, y), dist,
                                                                   dire)  # obtain coordinates of current cell (tuple)
                            current_cell = self.board[location[0]][location[1]]  # obtain enum value of current cell
                            # next direction if board limit is reached
                            if (location[0] > self.x) | (location[1] > self.y):
                                break
                            # next direction if same cell reached
                            if current_cell.value == play.identifier:
                                break
                            # next direction if empty cell reached, append if flag==True
                            if current_cell == Cell.EMPTY:
                                if flag:
                                    valid.append(location)
                                break
                            # next distance if opposite cell reached, enable flag
                            flag = True
        return valid

    def valid_moves_avail(self, play: AbstractPlayer) -> bool:
        """
        determine if active player has moves available
        :param play: Player making move
        :return: moves available? (boolean)
        """
        # list evaluates to False if empty
        if self._get_valid_moves(play):
            return False
        return True

    def start(self) -> None:
        """
        Starts a game
        :return: None
        """
        self.order = self._coin_flip()
        self.running = True
        self.board[3][3] = Cell.BLACK
        self.board[3][4] = Cell.WHITE
        self.board[4][3] = Cell.WHITE
        self.board[4][4] = Cell.BLACK
        # self.loop()

    def get_board(self) -> [[Cell]]:
        return self.board

    def update_board(self, m: Move, c: Cell) -> None:
        """
        Updates the board after a valid move has been made.
        :param m: move
        :param c: the type of piece to be placed
        :return: None
        """

        board_size = max(self.x, self.y)  # 1D board size in event of asymmetrical board
        flip = []  # track cells to flip guaranteed

        # iterate over cardinal directions: N, NE, E, SE, S, SW, W, NW
        for dire in range(8):
            tracked = []  # track cells to flip if terminus == c

            # iterate over distances emerging from m
            for dist in range(1, board_size):

                location = Game._get_cardinal_location(m.getCoords(), dist,
                                                       dire)  # obtain coordinates of current cell (tuple)
                current_cell = self.board[location[0]][location[1]]  # obtain enum value of current cell

                # next direction if board limit is reached, discard tracked cells
                if (location[0] > self.x) | (location[1] > self.y):
                    tracked.clear()
                    break

                # next direction if empty cell is reached, discard tracked cells
                if current_cell == Cell.EMPTY:
                    tracked.clear()
                    break

                # next distance if opposite color is found, track
                if current_cell != c:
                    tracked.append(location)
                    continue

                # next direction if same cell is reached, save tracked cells
                for location in tracked:
                    flip.append(location)

        # flip cells using location tuple as index
        for x, y in flip:
            self.board[x][y] = c

    @staticmethod
    def _get_cardinal_location(origin_cell, distance, direction):
        """
        Obtains target cell location (cartesian) from cardinal inputs and reference cell
        :param origin_cell: reference location upon which distance and direction are applied
        :param distance: magnitude with respect to origin_cell
        :param direction: cardinal direction range(8) clockwise starting with North
        :return: target cell location (x, y)
        """
        location = (
            (origin_cell[0], origin_cell[1] + distance),  # N
            (origin_cell[0] + distance, origin_cell[1] + distance),  # NE
            (origin_cell[0] + distance, origin_cell[1]),  # E
            (origin_cell[0] + distance, origin_cell[1] - distance),  # SE
            (origin_cell[0], origin_cell[1] - distance),  # S
            (origin_cell[0] - distance, origin_cell[1] - distance),  # SW
            (origin_cell[0] - distance, origin_cell[1]),  # W
            (origin_cell[0] - distance, origin_cell[1] + distance)  # NW
        )
        return location[direction]

    # def loop(self) -> None:
    #     """
    #     Main loop for game
    #     :return: None
    #     """
    #     while self.running:
    #         valid = False
    #         move = None
    #
    #         # loop until the player picks a valid move
    #         # Functionality will probably change with the addition of a front end
    #         # Can probably break this into a helper fn
    #         while not valid:
    #             move = self.order[0].getMove()
    #             valid = self.validateMove(move, self.order[0])
    #
    #         self.updateBoard(move, Cell.P1)
    #
    #         valid = False
    #         move = None
    #
    #         # loop until the player picks a valid move
    #         # Functionality will probably change with the addition of a front end
    #         while not valid:
    #             move = self.order[1].getMove()
    #             valid = self.validateMove(move, self.order[1])
    #
    #         self.updateBoard(move, Cell.P2)
    #
    #         self.round += 1
    #         print("finished round " + str(self.round))
    #         if self.round == 5:
    #             self.running = False
