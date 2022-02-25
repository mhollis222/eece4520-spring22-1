from Model.game import Game, Cell
from Model.move import Move
from Model.abstract_player import AbstractPlayer
from View.textual_view import TextualView
import yaml

settings_path = '../../settings.YAML'


class GameController:

    def __init__(self, p1: AbstractPlayer, p2: AbstractPlayer):
        self.model = None
        self.view = None
        self.p1 = p1
        self.p2 = p2
        self.settings = self.load_settings()
        self.setup(self.settings)

    def play_game(self):
        """
        Simulates a local game between two human players
        :return: none
        """
        self.model.start()  # Initializes game

        while not self.model.has_game_ended():

            player = self.model.get_active_player()  # the player whose turn it is

            # Checks if there are any available moves for the current player
            if self.model.valid_moves_avail(player):
                self.view.display_board()
                self.view.display_score()
                self.view.display_current_player(player)

                r, c = self.view.get_move()  # Asks and retrieves the user for their desired coordinates

                attempt = player.make_move(r, c)

                # Checks if the given coordinate is a valid move
                while not self.model.validate_move(attempt, player):
                    # Alerts the player of their invalid attempt and asks them to re-enter
                    self.view.display_invalid_moves(player)
                    x, y = self.view.get_move()
                    attempt = Move(x, y)

                # Checks whose turn it is and updates the board with their corresponding piece
                if self.model.get_active_player() == self.model.order[0]:
                    self.model.update_board(attempt, Cell.BLACK)
                else:
                    self.model.update_board(attempt, Cell.WHITE)

                # Updates both of the players' scores
                self.model.update_score()

                # Checks if the game has ended
                if self.model.has_game_ended():
                    self.view.display_end_of_game()
                    self.view.display_board()
                    self.view.display_score()
                    self.view.display_winner(self.model.display_winner())
                else:
                    self.model.switch_players(player)  # Passes play to the other player

            else:
                self.view.display_player_skipped(player)  # Alerts user that their turn has been skipped
                self.model.switch_players(player)  # Passes play to the other player

    def load_settings(self) -> dict:
        with open(settings_path) as f:
            return yaml.safe_load(f)

    def setup(self, settings: dict) -> None:
        # Make the game object
        width = settings['Model']['board_width']
        height = settings['Model']['board_height']

        # Currently, unused
        # ai_difficult = settings['Model']['AI_difficulty']
        # start_filled = settings['Model']['start_filled']
        # debug = settings['Debug']

        self.model = Game(self.p1, self.p2, width, height)

        view_type = settings['View']['style']
        # Currently, unused
        # p1_col = settings['View']['p1_color']
        # p2_col = settings['View']['p2_color']

        if view_type == 'textual':
            self.view = TextualView(self.model)
        elif view_type == 'GUI':
            # dont have other option yet
            pass



