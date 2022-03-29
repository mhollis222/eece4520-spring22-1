from abc import ABC, abstractmethod
from Model.move import Move
from Model.abstract_player import AbstractPlayer


class AbstractGame(ABC):
    @abstractmethod
    def get_order(self):
        pass

    @abstractmethod
    def validate_move(self, move: Move, play: AbstractPlayer):
        pass

    @abstractmethod
    def get_valid_moves(self, play: AbstractPlayer):
        pass

    @abstractmethod
    def search(self, move: tuple, identity: int):
        pass

    @abstractmethod
    def valid_moves_avail(self, play: AbstractPlayer):
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def get_board(self):
        pass

    @abstractmethod
    def update_board(self, m: Move, c) -> None:
        pass

    @abstractmethod
    def update_score(self):
        pass

    @abstractmethod
    def is_board_filled(self) -> bool:
        pass

    @abstractmethod
    def has_game_ended(self) -> bool:
        pass

    @abstractmethod
    def display_winner(self) -> int:
        pass

    @abstractmethod
    def get_active_player(self) -> AbstractPlayer:
        pass

    @abstractmethod
    def switch_players(self, player: AbstractPlayer):
        pass

    @abstractmethod
    def get_moves_sim(self, moves, player):
        pass
