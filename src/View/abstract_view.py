from abc import abstractmethod, ABC


class AbstractView(ABC):
    def __init__(self, board):
        self.board = board

    @abstractmethod
    def display_board(self):
        pass

    @abstractmethod
    def display_current_player(self, player):
        pass

    @abstractmethod
    def get_move(self):
        pass

    @abstractmethod
    def display_valid_moves(self):
        pass

    @abstractmethod
    def display_invalid_moves(self):
        pass

    @abstractmethod
    def display_winner(self, winner):
        pass
