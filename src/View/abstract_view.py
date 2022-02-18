from abc import abstractmethod, ABC
from Model.Game import Game
from Model import AbstractPlayer


class AbstractView(ABC):
    def __init__(self, model: Game):
        self.model = model

    def __init__(self, board_view):
        self.board_view = board_view

    @abstractmethod
    def display_board(self):
        pass

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
        """
        Prints who won the game
        :param winner: Number representative of the player who won the game (int)
        :return: none
        """
        pass

    @abstractmethod
    def display_player_skipped(self, player):
        """
        Alerts player their turn has been skipped via print statement
        :param player: Player whose turn's been skipped
        :return: none
        """
        pass

    @abstractmethod
    def display_score(self):
        """
        Displays the current score of both players alongside their names
        :return: none
        """
        pass

    @abstractmethod
    def display_end_of_game(self):
        """
        Alerts the players that the game is over
        :return: none
        """
        pass
