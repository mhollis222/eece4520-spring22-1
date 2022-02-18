from abc import abstractmethod, ABC
from Model.game import Game
from Model import abstract_player


class AbstractView(ABC):
    def __init__(self, model: Game):
        self.model = model

    def __init__(self, board_view):
        self.board_view = board_view

    @abstractmethod
    def display_board(self):
        """
        Prints the game board and fills in pieces as game goes on
        :return: none
        """
        pass

    @abstractmethod
    def display_current_player(self, player: abstract_player):
        """
        Prints a message to indicate current player's turn
        :param player: Number representative of the player who is up (int)
        :return: non
        """
        pass

    @abstractmethod
    def get_move(self):
        """
        Takes in user input for x and y
        :return: x and y
        """
        pass

    @abstractmethod
    def display_invalid_moves(self, player):
        """
        Prints message indicating that move made was invalid
        :param player: Number representative of the player who made the invalid move (int)
        :return: none
        """
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