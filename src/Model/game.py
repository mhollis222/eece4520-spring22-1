from abstract_player import AbstractPlayer
from enum import Enum
from random import random
from move import Move
from abstract_game import AbstractGame


# the more I think about this, the less I think we actually need an enum here.
# I don't think it detracts anything, but I'm not sure what advantage we actually get from it.
# the only real downside is that flipping involves an extra if statement when we could just use
# (identity + 2) % 2 + 1 to flip it if it was just an int
class Cell(Enum):
    EMPTY = 0  # Empty Cell
    BLACK = 1  # Player One's Piece
    WHITE = 2  # Player Two's Piece


class Game(AbstractGame):

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
        if self.get_valid_moves(play).count(move.get_coords()) > 0:
            return True
        return False

    def get_valid_moves(self, play: AbstractPlayer) -> list:
        """
        obtain cell locations for valid moves
        :param play: Player making move
        :return: list of locations on board (list:tuple)
        """
        valid = []
        # Should this be based on the history or live pieces
        live_pieces = [(x, y) for x in range(self.x) for y in range(self.y) if
                       self.board[y][x].value == play.identifier]
        for move in live_pieces:
            valid = valid + self.search(move, play.identifier)
        return valid

    def search(self, move: tuple, identity: int) -> list:
        """
        Searches for possible moves in all directions from a radial point
        :param move: Starting point
        :param identity: Current Player
        :return: List of viable moves
        """
        valid = [self._search_help(move, identity, dx=1, dy=0), self._search_help(move, identity, dx=0, dy=1),
                 self._search_help(move, identity, dx=-1, dy=0), self._search_help(move, identity, dx=0, dy=-1),
                 self._search_help(move, identity, dx=-1, dy=-1), self._search_help(move, identity, dx=1, dy=-1),
                 self._search_help(move, identity, dx=-1, dy=1), self._search_help(move, identity, dx=1, dy=1)]

        return [x for x in valid if x is not None]

    def _search_help(self, move: tuple, identity: int, dx, dy) -> tuple:
        """
        Helper function for finding possible moves in a certain direction
        :param move: Starting point
        :param identity: Current player
        :param dx: Constant shift in the x direction
        :param dy: Constant shift in the y direction
        :return: List of possible moves in a certain direction
        """
        (x, y) = move
        x = x + dx
        y = y + dy

        if x in range(1, self.x - 1) and y in range(1, self.y - 1):
            # funny math to alternate between 1 and 2
            if self.board[y][x].value == (identity + 2) % 2 + 1:
                while x in range(1, self.x - 1) and y in range(1, self.y - 1):
                    x = x + dx
                    y = y + dy
                    # If we hit our own piece before an empty square, no valid move
                    if self.board[y][x].value == identity:
                        return None
                    if self.board[y][x] == Cell.EMPTY:
                        return x, y

        return None

    def valid_moves_avail(self, play: AbstractPlayer) -> bool:
        """
        determine if active player has moves available
        :param play: Player making move
        :return: moves available? (boolean)
        """
        # list evaluates to False if empty
        return bool(self.get_valid_moves(play))

    def start(self) -> None:
        """
        Initializes a game
        :return: None
        """
        self.order = self._coin_flip()
        self.active_player = self.order[0]
        self.board[int(self.y/2) - 1][int(self.x/2) - 1] = Cell.WHITE
        self.board[int(self.y/2) - 1][int(self.x/2)] = Cell.BLACK
        self.board[int(self.y/2)][int(self.x/2) - 1] = Cell.BLACK
        self.board[int(self.y/2)][int(self.x/2)] = Cell.WHITE

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
        x, y = m.get_coords()
        self.board[y][x] = c
        # Call all 8 directions
        to_flip = self._flip_help(m, c, dx=1, dy=0) + \
                  self._flip_help(m, c, dx=0, dy=1) + \
                  self._flip_help(m, c, dx=-1, dy=0) + \
                  self._flip_help(m, c, dx=0, dy=-1) + \
                  self._flip_help(m, c, dx=-1, dy=-1) + \
                  self._flip_help(m, c, dx=1, dy=-1) + \
                  self._flip_help(m, c, dx=-1, dy=1) + \
                  self._flip_help(m, c, dx=1, dy=1)

        for x, y in to_flip:
            self.board[y][x] = c

    def _flip_help(self, m: Move, identity: Cell, dx: int, dy: int):
        """
        Helper to decide which cells need to be flipped in a certain direction
        :param m: The piece being placed
        :param identity: Identity of current player
        :param dx: constant shift in x direction
        :param dy: constant shift in y direction
        :return: List of cells to be flipped
        """
        visited = []
        x, y = m.get_coords()
        x = x + dx
        y = y + dy
        while x in range(self.x) and y in range(self.y):
            # Once we hit our own piece we're done
            if self.board[y][x].value == identity.value:
                return visited
            # If we hit an empty cell there is nothing to flip
            elif self.board[y][x] == Cell.EMPTY:
                return []
            visited.append((x, y))
            x = x + dx
            y = y + dy

        # Here in the event that a piece is placed on the edge, since while loop won't trigger
        return []

    # deprecated?
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

    def get_active_player(self) -> AbstractPlayer:
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
