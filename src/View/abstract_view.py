from abc import abstractmethod, ABC
from Model.Game import Game


class AbstractView(ABC):
    def __init__(self, board: Game):
        self.board = board

    @abstractmethod
    def display_board(self, board: Game):
        pass

    def __init__(self, board_view):
        self.board_view = board_view

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

    @abstractmethod
    def display_player_skipped(self, player):
        pass