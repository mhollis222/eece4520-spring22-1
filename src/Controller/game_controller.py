from Model.Game import Game, Cell
from Model.Move import Move
from View.abstract_view import AbstractView

class GameController:

    def __init__(self, model: Game, view: AbstractView):
        self.model = model
        self.view = view

    def play_game(self):
        self.model.start()

        end = 0
        while self.model.running:
            counter = 0
            while counter <= 1 and end < 2:

                player = self.model.order[counter]

                if self.model.valid_moves_avail(player):
                    self.view.display_board()
                    self.view.display_current_player(player)

                    x, y = self.view.get_move()

                    attempt = Move(x, y)

                    while not self.model.validate_move(attempt, self.model.order[counter]):
                        self.view.display_invalid_moves()
                        x, y = self.view.get_move()
                        attempt = Move(x, y)

                    if counter == 0:
                        self.model.update_board(attempt, Cell.BLACK)
                    else:
                        self.model.update_board(attempt, Cell.WHITE)

                    if not self.model.running:
                        self.view.display_winner(counter)
                    else:
                        counter = counter + 1

                else:
                    counter = counter + 1
                    if not counter > 1:
                        self.view.display_player_skipped(self.model.order[counter])
                        end = end + 1
                        if end == 2:
                            print("Game Over")
                            self.view.display_winner(counter)
