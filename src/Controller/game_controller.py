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
        self.model.start()
        end = 0

        while self.model.has_game_ended():
            current_player = 0

            while current_player <= 1 and end < 2:
                player = self.model.order[current_player]

                if self.model.valid_moves_avail(player):
                    self.view.display_board()
                    self.view.display_score()
                    self.view.display_current_player(player)

                    x, y = self.view.get_move()

                    attempt = Move(x, y)

                    while not self.model.validate_move(attempt, self.model.order[current_player]):
                        self.view.display_invalid_moves()
                        x, y = self.view.get_move()
                        attempt = Move(x, y)

                    if current_player == 0:
                        self.model.update_board(attempt, Cell.BLACK)
                    else:
                        self.model.update_board(attempt, Cell.WHITE)

                    self.model.update_score()

                    if not self.model.has_game_ended():
                        self.view.display_winner(self.model.display_winner())
                    else:
                        current_player = current_player + 1

                else:
                    if current_player <= 1:
                        self.view.display_player_skipped(self.model.order[current_player])
                        end = end + 1
                        if end == 2:
                            print("Game Over!")
                            self.view.display_board()
                            self.view.display_winner(self.model.display_winner())
                            self.view.display_score()

                    current_player = current_player + 1
