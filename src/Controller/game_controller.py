from Model.HumanPlayer import HumanPlayer
from Model.Game import Game, Cell
from Model.Move import Move
from View.abstract_view import AbstractView


class GameController:

    def __init__(self, model: Game, view: AbstractView):
        self.model = model
        self.view = view

    def play_game(self):
        self.model.start()

        while self.model.running:
            counter = 0

            while counter <= 1:
                if self.model.valid_moves_avail(self.model.order[counter]):
                    # self.view.display_board(self.model)
                    self.view.display_current_player(self.model.order[counter])
                    x, y = self.view.get_move()

                    attemptedMove = Move(x, y)

                    while not self.model.validate_move(attemptedMove, self.model.order[counter]):
                        self.view.display_invalid_moves()
                        self.view.get_move()

                    if counter == 0:
                        self.model.updateBoard(attemptedMove, Cell.BLACK)
                    else:
                        self.model.updateBoard(attemptedMove, Cell.WHITE)

                    if not self.model.running:
                        self.view.display_winner(counter)
                    else:
                        counter = counter + 1

                else:
                    counter = counter + 1
                    if not counter > 1:
                        self.view.display_player_skipped(self.model.order[counter])
