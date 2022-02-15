from abc import abstractmethod, ABC


class AbstractView(ABC):
    def __init__(self, board):
        self.board = board

    @abstractmethod
    def displayBoard(self):
        pass



    def __init__(self, board_view):
        self.board_view = board_view

    @abstractmethod
    def displaycurrentPlayer(self, player):
        pass

    @abstractmethod
    def displayvalidMoves(self):
        pass

    @abstractmethod
    def displayinvalidMoves(self):
        pass

    @abstractmethod
    def getMove(self):
        pass

    @abstractmethod
    def displayWinner(self, winner):
        pass

