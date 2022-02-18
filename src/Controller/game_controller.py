from Model.Game import Game, Cell
from Model.Move import Move
from View.abstract_view import AbstractView


class GameController:

    def __init__(self, model: Game, view: AbstractView):
        self.model = model
        self.view = view

    def play_game(self):
        """
         Simulates a game between two players
         """
        self.model.start()  # Initializes game

        while not self.model.has_game_ended():

            player = self.model.get_active_player()  # the player whose turn it is

            # Checks if there are any available moves for the current player
            if self.model.valid_moves_avail(player):
                self.view.display_board()
                self.view.display_score()
                self.view.display_current_player(player)

                x, y = self.view.get_move()  # Asks and retrieves the user for their desired coordinates

                attempt = Move(x, y)

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
