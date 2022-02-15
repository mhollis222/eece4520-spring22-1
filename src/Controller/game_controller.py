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
                # self.view.display_board(self.model)
                self.view.display_current_player(self.model.order[counter])
                x, y = self.view.get_move()

                attemptedMove = Move(x, y)

                while not self.model.validateMove(attemptedMove):
                    self.view.display_invalid_moves()
                    self.view.get_move()

                if counter == 0:
                    self.model.updateBoard(attemptedMove, Cell.P1)
                else:
                    self.model.updateBoard(attemptedMove, Cell.P2)

                if not self.model.running:
                    self.view.display_winner(0)
                else:
                    counter = counter + 1



        # terminated = self.model.running
        #
        # while not terminated:
        #     self.view.displayBoard()
        #     self.view.displaycurrentPlayer()
        #
        #     row, col = self.view.getMove()
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
