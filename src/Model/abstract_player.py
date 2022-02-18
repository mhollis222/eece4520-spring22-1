from abc import abstractmethod, ABC


class AbstractPlayer(ABC):
    def __init__(self, name: str):
        self.score = 2  # number of pieces the player has on board
        self.name = name  # name of player
        self.identifier = 0  # number representative of whether or not they are Player One or Player Two

    def __str__(self) -> str:
        return self.name

    @staticmethod
    @abstractmethod
    def make_move(row, column):
        """
        Declares a move request to be made within active game.
        :return: Move(int, int)
        """
        pass
