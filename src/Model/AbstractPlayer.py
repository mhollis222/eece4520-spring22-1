from abc import abstractmethod, ABC
from Move import Move


# TODO: make abstract, haven't for flow test
class AbstractPlayer(ABC):
    def __init__(self, name: str):
        self.score = 0
        self.name = name

    @abstractmethod
    def getMove(self) -> Move:
        print(self.name + " choosing a move!")
        return Move(0, 0)

    def __str__(self) -> str:
        return self.name
