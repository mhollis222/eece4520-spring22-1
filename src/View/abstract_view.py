from abc import abstractmethod, ABC
from Model.Game import Game
from Model import AbstractPlayer


class AbstractView(ABC):
    def __init__(self, model: Game):
        self.model = model

    @abstractmethod
    def display_board(self):
        pass

    def __init__(self, board_view):
        self.board_view = board_view

    @abstractmethod
    def display_current_player(self, player: AbstractPlayer):
        pass

    @abstractmethod
    def get_move(self):
        pass

    @abstractmethod
    def display_invalid_moves(self, player):
        pass

    @abstractmethod
    def display_winner(self, winner):
        pass

    @abstractmethod
    def display_player_skipped(self, player):
        pass

    @abstractmethod
    def display_score(self):
        pass

    @abstractmethod
    def display_end_of_game(self):
        pass