from AbstractPlayer import AbstractPlayer
from enum import Enum
from random import random
from Move import Move


class Cell(Enum):
    EMPTY = 0  # Empty Cell
    BLACK = 1  # Player One's Piece
    WHITE = 2  # Player Two's Piece


class Game:

    def __init__(self, p1: AbstractPlayer, p2: AbstractPlayer, x: int = 8, y: int = 8):
        self.p1 = p1  # Player One
        self.p2 = p2  # Player Two
        self.x = x  # width of board
        self.y = y  # height of board
        self.board = [[Cell.EMPTY for x in range(self.x)] for y in range(self.y)]  # 2D array of cells
        self.order = []  # order of players
        self.active_player = None  # Player whose turn it currently is

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
        if self.get_valid_moves(play).count(move.getCoords()) > 0:
            return True
        return False

    def get_valid_moves(self, play: AbstractPlayer) -> list:
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
                    # print("active player piece found at ", x, y)
                    for dire in range(board_size):
                        # print("\ndirection ", dire)
                        flag = False
                        for dist in range(1, board_size):
                            location = Game._get_cardinal_location((x, y), dist,
                                                                   dire)  # obtain coordinates of current cell (tuple)
                            # print("searching ", location)
                            # next direction if board limit is reached
                            if (location[0] >= self.x) | (location[1] >= self.y):
                                # print("board limit reached, next direction")
                                break
                            current_cell = self.board[location[0]][location[1]]  # obtain enum value of current cell
                            # next direction if same cell reached
                            if current_cell.value == play.identifier:
                                # print("cell of same player reached, next direction")
                                break
                            # next direction if empty cell reached, append if flag==True
                            if current_cell == Cell.EMPTY:
                                # print("empty cell reached, next direction")
                                if flag:
                                    # print("cell valid at ", location)
                                    valid.append(location)
                                break
                            # next distance if opposite cell reached, enable flag
                            # print("cell of opponent reached, continuing")
                            flag = True
        return valid

    def valid_moves_avail(self, play: AbstractPlayer) -> bool:
        """
        determine if active player has moves available
        :param play: Player making move
        :return: moves available? (boolean)
        """
        # list evaluates to False if empty
        if not self.get_valid_moves(play):
            return False
        return True

    def start(self) -> None:
        """
        Initializes a game
        :return: None
        """
        self.order = self._coin_flip()
        self.active_player = self.order[0]
        self.board[3][3] = Cell.WHITE
        self.board[3][4] = Cell.BLACK
        self.board[4][3] = Cell.BLACK
        self.board[4][4] = Cell.WHITE

    def get_board(self) -> [[Cell]]:
        """
        :return: 2D array of cells representative of the board ([[Cell]])
        """
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

        # iterate over cardinal directions: W, SW, S, SE, E, NE, N
        for dire in range(board_size):
            tracked = []  # track cells to flip if terminus == c
            # print("\ndirection ", dire)
            # iterate over distances emerging from m
            for dist in range(1, board_size):

                location = Game._get_cardinal_location(m.getCoords(), dist,
                                                       dire)  # obtain coordinates of current cell (tuple)
                # print("searching ", location)
                # next direction if board limit is reached, discard tracked cells
                if (location[0] >= self.x) | (location[1] >= self.y):
                    tracked.clear()
                    # print("board limit reached, next direction")
                    break

                current_cell = self.board[location[0]][location[1]]  # obtain enum value of current cell

                # next direction if empty cell is reached, discard tracked cells
                if current_cell == Cell.EMPTY:
                    tracked.clear()
                    # print("empty cell reached, next direction")
                    break

                # next distance if opposite color is found, track
                if current_cell.value != c.value:
                    # print("opponent cell reached, tracking ", location)
                    tracked.append(location)
                    continue

                # next direction if same cell is reached, save tracked cells
                for location in tracked:
                    # print("saving ", tracked)
                    flip.append(location)

        # flip cells using location tuple as index
        for x, y in flip:
            # print("flipped ", x, y)
            self.board[x][y] = c
        self.board[m.x][m.y] = c

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
            (origin_cell[0], origin_cell[1] - distance),  # W
            (origin_cell[0] + distance, origin_cell[1] - distance),  # SW
            (origin_cell[0] + distance, origin_cell[1]),  # S
            (origin_cell[0] + distance, origin_cell[1] + distance),  # SE
            (origin_cell[0], origin_cell[1] + distance),  # E
            (origin_cell[0] - distance, origin_cell[1] + distance),  # NE
            (origin_cell[0] - distance, origin_cell[1]),  # N
            (origin_cell[0] - distance, origin_cell[1] - distance)  # NW
        )
        return location[direction]

    def update_score(self):
        """
        Iterates through the board to count the number of cells each player has
        :return: none
        """
        self.order[0].score = 0
        self.order[1].score = 0

        # iterates through the board
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j].value == 1:
                    self.order[0].score = self.order[0].score + 1  # Updates Player One's score
                if self.board[i][j].value == 2:
                    self.order[1].score = self.order[1].score + 1  # Updates Player Two's score

    def is_board_filled(self) -> bool:
        """
        Checks if the board is full
        :return: whether or not the board is completely filled (boolean)
        """
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j].value == 0:
                    return False
        return True

    def has_game_ended(self) -> bool:
        """
        Checks if the game has ended
        :return: whether or not the game has ended (boolean)
        """
        return (not ((self.valid_moves_avail(self.order[0])) or (self.valid_moves_avail(self.order[1])))) \
               or self.is_board_filled()

    def display_winner(self) -> int:
        """
        Returns a number representative of the player who won the game
        :return: a 1 if player one has the most points, a 2 if player two does, and a 0 if they tied
        """
        if self.order[0].score > self.order[1].score:
            return 1
        elif self.order[0].score < self.order[1].score:
            return 2
        else:
            return 0

    def get_active_player(self):
        """
        Returns the player whose turn it is
        :return: The player whose turn it currently is
        """
        return self.active_player

    def switch_players(self, player: AbstractPlayer):
        """
        Changes the currently active player to the other player
        :param player: The player whose turn it currently is
        :return: none
        """
        # Checks if the given player is Player One
        if player == self.order[0]:
            self.active_player = self.order[1]  # Passes play to Player Two
        else:
            self.active_player = self.order[0]  # Passes play to Player One
