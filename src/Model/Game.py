from AbstractPlayer import AbstractPlayer
from enum import Enum
from random import random
from Move import Move


class Cell(Enum):
    EMPTY = 0
    P1 = 1
    P2 = 2


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

    def coinFlip(self) -> [AbstractPlayer, AbstractPlayer]:
        """
        simulates a coin flip to decide which player goes first
        :return: the player to go first
        """
        return [self.p1, self.p2] if random() > 0.5 else [self.p2, self.p1]

    def validateMove(self, move: Move, play: AbstractPlayer) -> bool:
        """
        makes sure the desired move is in fact possible.
        :param move: The player requested move
        :param play: Player making move
        :return: valid?
        """
        return True

    def start(self) -> None:
        """
        Starts a game
        :return: None
        """
        self.order = self.coinFlip()
        self.running = True
        self.loop()

    def updateBoard(self, m: Move, c: Cell) -> None:
        """
        Updates the board after a valid move has been made.
        :param m: move
        :param c: the type of piece to be placed
        :return: None
        """

    def loop(self) -> None:
        """
        Main loop for game
        :return: None
        """
        while self.running:
            valid = False
            move = None

            # loop until the player picks a valid move
            # Functionality will probably change with the addition of a front end
            # Can probably break this into a helper fn
            while not valid:
                move = self.order[0].getMove()
                valid = self.validateMove(move, self.order[0])

            self.updateBoard(move, Cell.P1)

            valid = False
            move = None

            # loop until the player picks a valid move
            # Functionality will probably change with the addition of a front end
            while not valid:
                move = self.order[1].getMove()
                valid = self.validateMove(move, self.order[1])

            self.updateBoard(move, Cell.P2)

            self.round += 1
            print("finished round " + str(self.round))
            if self.round == 5:
                self.running = False

