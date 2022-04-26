import time

from Model.game import Game, Cell
from Model.move import Move
from Model.abstract_player import AbstractPlayer
from Model.game_decorator_ai import GameDecoratorAI
from Model.game_decorator_online import GameDecoratorOnline
from View.textual_view import TextualView
from View.UI.gui_board import GuiBoard
from Controller.client import ReversiClient
from Controller.message import ReversiMessage as msg
import configparser

from pathlib import Path

path_parent = Path(__file__).resolve().parents[2]
settings_path = path_parent.joinpath('settings.ini').as_posix()


class GameFactory:
    from Model.abstract_game import AbstractGame

    @staticmethod
    def get_game(game_type: str, p1: AbstractPlayer, p2: AbstractPlayer, width: int, height: int, g_order: list) -> AbstractGame:
        if game_type == 'local':
            return Game(p1, p2, width, height)
        elif game_type == 'AI':
            return GameDecoratorAI(Game(p1, p2, width, height))
        elif game_type == 'online':
            game = Game(p1, p2, width, height)
            return GameDecoratorOnline(game, g_order)
        raise ValueError('Unknown game type')


class GameController:

    def __init__(self, p1: AbstractPlayer, p2: AbstractPlayer, ai: bool = False, game_id=0, reconstruct=False, g_order=None):
        self.model = None
        self.view = None
        self.p1 = p1
        self.p2 = p2
        # special options to save comments on writes (i hope)
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)
        self.ai = ai
        self.simulator = None
        self.client = ReversiClient()
        self.game_id = game_id
        self.last_move = None
        self.reconstruct = reconstruct
        self.g_order = g_order
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
                if self.model.get_active_player() == self.model.get_order()[0]:
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

    # the following code should execute on both clients BUT the database should only be updated once
    def game_update(self):
        """
        Checks online game information for completed game and sends to server so database can be updated accordingly
        :return: none
        """
        players = [self.model.get_order()[0], self.model.get_order()[1]]
        if players[0].score > players[1].score:
            hs = players[0]
            ls = players[1]
        else:
            hs = players[1]
            ls = players[0]

        if hs.type() == 'Human':
            winner = self.p1.name
            loser = self.p2.name
        else:
            winner = self.p2.name
            loser = self.p1.name

        opponent_expected_win = self.client.send_request(msg('expected_win', [self.p2.name]))[0]
        client_expected_win = self.client.send_request(msg('expected_win', [self.p1.name]))[0]

        if winner == self.p1.name:
            winner_expected_win = client_expected_win
            loser_expected_win = opponent_expected_win
        else:
            winner_expected_win = opponent_expected_win
            loser_expected_win = client_expected_win

        if self.model.display_winner == 0:
            win_res = 0.5
            los_res = 0.5
        else:
            win_res = 1
            los_res = 0
        winner_elo = self.client.send_request(msg('updated_elo', [win_res, winner_expected_win]))[0]
        loser_elo = self.client.send_request(msg('updated_elo', [los_res, loser_expected_win]))[0]

        winner_hs = hs.score
        loser_hs = ls.score

        self.client.send_request(msg('update_game_complete', [self.game_id, winner, winner_elo, winner_hs,
                                                              loser, loser_elo, loser_hs]))

    def advance(self, button):
        """
        Calls all GUI functions when board is clicked. Steps through one cycle of the game loop with each call.
        :param button:
        :return: none
        """
        ai_turn = False
        network_turn = False
        # Get the current player
        player = self.model.get_active_player()
        # Get the move
        if player.type() == 'AI':
            print("AI TURN")
            ai_turn = True
            move = player.make_move(0, 0)
            attempt = Move(move[0], move[1])
        elif player.type() == 'Online':
            network_turn = True
            move = 'TIMEOUT'
            while move == 'TIMEOUT':
                move = player.get_move()
            attempt = move
        else:
            x, y = button.x, button.y
            attempt = Move(y, x)
            self.last_move = attempt
            if type(self.model) == GameDecoratorOnline:
                self.client.send_request(msg('update_game_state', [self.game_id, self.p1.name, attempt]))
                ret = self.p2.send_move(attempt)

        if player.name == self.model.get_order()[0].name:
            self.model.update_board(attempt, Cell.BLACK)
        else:
            self.model.update_board(attempt, Cell.WHITE)

        self.model.update_score()

        if self.model.has_game_ended():
            print("Game ended")
            self.view.display_board([])
            self.view.display_score()
            self.view.display_winner(self.model.display_winner())

            if type(self.model) == GameDecoratorOnline:
                self.game_update()
        else:
            self.model.switch_players(player)  # Passes play to the other player
            new_player = self.model.get_active_player()
            # Update the board
            moves = self.model.get_valid_moves(new_player)
            if len(moves) == 0:
                self.model.switch_players(new_player)
            self.view.display_board(moves)
            self.view.display_score()
            self.view.display_current_player(new_player)
            time.sleep(2)
            if not ai_turn and not network_turn:
                self.advance(None)

    def save_settings(self) -> bool:
        """
        Stores the internal settings dict as a .ini file at `settings_path`
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
        ai_difficult = self.config.getint('Model', 'AI_difficulty')

        if self.ai:
            game_type = 'AI'
            decorator = GameFactory.get_game(game_type, self.p1, self.p2, width, height, self.g_order)
            self.model = decorator.get_game()
            self.p2.add_simulator(decorator)
        elif self.p2.type() == 'Online':
            game_type = 'online'
            self.model = GameFactory.get_game(game_type, self.p1, self.p2, width, height, self.g_order)
            self.client = ReversiClient()
        else:
            game_type = 'local'
            self.model = GameFactory.get_game(game_type, self.p1, self.p2, width, height, self.g_order)

        view_type = self.config['View']['style']
        p1_col = self.config['View']['p1_color']
        p2_col = self.config['View']['p2_color']

        if view_type == 'textual':
            self.view = TextualView(self.model, p1_col, p2_col)
        elif view_type == 'gui':
            self.view = GuiBoard(self.model, p1_col, p2_col, self)
            self.model.start()
            if type(self.model) == GameDecoratorOnline:
                if self.g_order[0].name == self.p1.name:
                    self.model.set_p1_ident(1)
                    self.model.set_p2_ident(2)
                else:
                    self.model.set_p1_ident(2)
                    self.model.set_p2_ident(1)
            # if self.reconstruct and self.model is GameDecoratorOnline:
            #     details = self.client.send_request(msg('get_game_state', [self.game_id]))
            #     self.model.reconstruct(state=details[0], last_active_player=details[1])
            self.view.display_board(self.model.get_valid_moves(self.model.get_active_player()))
            self.view.display_score()
            self.view.display_current_player(self.model.get_active_player())
            if self.model.get_active_player().type() == 'AI' or self.model.get_active_player().type() == 'Online':
                self.advance(None)
            self.view.root.mainloop()
