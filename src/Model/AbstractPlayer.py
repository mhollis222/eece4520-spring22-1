from abc import ABC


class AbstractPlayer(ABC):
    def __init__(self, name: str):
        self.score = 2  # number of pieces the player has on board
        self.name = name  # name of player
        self.identifier = 0  # number representative of whether or not they are Player One or Player Two

    def __str__(self) -> str:
        return self.name
