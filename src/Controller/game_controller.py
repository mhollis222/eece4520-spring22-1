import tkinter
from Model.game import Game, Cell
from Model.move import Move
from Model.abstract_player import AbstractPlayer
from View.textual_view import TextualView
from View.UI.gui_board import GuiBoard
import configparser

settings_path = '../../settings.ini'


class GameController:

    def __init__(self, p1: AbstractPlayer, p2: AbstractPlayer):
        self.model = None
        self.view = None
        self.p1 = p1
        self.p2 = p2
        # special options to save comments on writes (i hope)
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)
        self.setup()

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
                # TODO: combine into fn
                self.view.display_board(self.model.get_valid_moves(player))
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

                # add the move to the player history
                self.model.get_active_player().add_move(attempt)

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

    def advance(self, button):
        # Get the current player
        player = self.model.get_active_player()
        # Disable the button
        button['state'] = tkinter.DISABLED
        # Get the move
        x, y = button.x, button.y
        attempt = Move(y, x)
        self.model.validate_move(attempt, player)
        # update the model
        if player == self.model.order[0]:
            self.model.update_board(attempt, Cell.BLACK)
        else:
            self.model.update_board(attempt, Cell.WHITE)
        # Update the score
        self.model.update_score()
        # Checks if the game has ended
        if self.model.has_game_ended():
            self.view.display_board([])
            self.view.display_end_of_game()
            self.view.display_winner(self.model.display_winner())
        else:
            self.model.switch_players(player)  # Passes play to the other player
            # Update the board
            self.view.display_board(self.model.get_valid_moves(self.model.get_active_player()))
        #self.model.debug()




    def save_settings(self) -> bool:
        """
        Stores the desired settings dict as a yaml file at `settings_path`
        :param settings: the settings to be stored.
        :return: success of operation
        """
        try:
            with open(settings_path, 'w') as f:
                self.config.write(f)
            return True
        except IOError:
            return False

    def setup(self) -> None:
        """
        Initializes the view and model based on the loaded settings.
        :param settings: settings loaded from Settings.YAML
        :return: None
        """
        # Make the game object
        width = self.config.getint('Model', 'board_width')
        height = self.config.getint('Model', 'board_height')

        # Currently, unused
        # ai_difficult = self.config.getint('Model', 'AI_difficulty')
        # start_filled = self.config.getboolean('Model', 'start_filled')
        # debug = self.config.getboolean('Misc', 'debug')

        self.model = Game(self.p1, self.p2, width, height)

        view_type = self.config['View']['style']
        p1_col = self.config['View']['p1_color']
        p2_col = self.config['View']['p2_color']

        if view_type == 'textual':
            self.view = TextualView(self.model, p1_col, p2_col)
        elif view_type == 'gui':
            self.view = GuiBoard(self.model, p1_col, p2_col, self)
            self.model.start()
            self.view.display_board(self.model.get_valid_moves(self.model.get_active_player()))
            self.view.root.mainloop()


