from abc import abstractmethod, ABC
from Model.move import Move


class AbstractPlayer(ABC):
    def __init__(self, name: str):
        self.score = 2  # number of pieces the player has on board
        self.name = name  # name of player
        self.identifier = 0  # number representative of whether or not they are Player One or Player Two
        self.history = []

    def __str__(self) -> str:
        return self.name

    @abstractmethod
    def make_move(self, row, column):
        """
        Declares a move request to be made within active game.
        :return: Move(int, int)
        """
        pass

    def add_move(self, move: Move) -> None:
        self.history.append(move)
