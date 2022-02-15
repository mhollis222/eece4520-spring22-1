from Model.Game import Game
from View.text_view import TextView

class GameController:

    def __init__(self, model: Game, view: TextView):
        self.model = model
        self.view = view

    def play_game(self):
        terminated = self.model.running

        while not terminated:
            self.view.displayBoard()
            self.view.displaycurrentPlayer()

            row, col = self.view.getMove()
            # while not self.model.is_legal_move(row, col):
                # self.view.is_illegal_move()
                # self.view.get_move()

            # self.model.make_move(row, col)
            # if self.model.has_game_ended():
                # terminated = True
            # else:
                # self.model.switch_turn()


        # self.view.display_board()
        # winner = self.model.get_winner()
        # self.view.display_winner(winner)
