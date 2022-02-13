from Model.Game import Game
# from View.Game_View import GameView

class GameController:

    def __init__(self, model: Game, view: GameView):
        self.model = model
        self.view = view

    def play_game(self):
        terminated = False

        while not terminated:
            self.view.display_board()
            # self.view.display_current_player()

            # row, col = self.view.get_move()
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
