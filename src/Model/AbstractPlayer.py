from abc import abstractmethod, ABC
from Move import Move


class AbstractPlayer(ABC):
    def __init__(self, name: str):
        self.score = 2
        self.name = name
        self.identifier = 0

    @abstractmethod
    def getMove(self) -> Move:
        pass

    def __str__(self) -> str:
        return self.name
