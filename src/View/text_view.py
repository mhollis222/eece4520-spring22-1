from View.abstract_view import AbstractView
from Model.Game import Game
from Model.AbstractPlayer import AbstractPlayer


class TextView(AbstractView):

    def __init__(self, model: Game):
        super().__init__(model)
        self.model = model

    def display_board(self):
        board_view = self.model.get_board()

        # constants for drawing board borders
        horizontal_line = '   +---+---+---+---+---+---+---+---+'

        # nested for loop to draw in board
        print('     1   2   3   4   5   6   7   8')
        print(horizontal_line)
        for i, x in enumerate(board_view):
            print(i+1, end='  ')
            for y in range(8):
                if x[y].value == 0:
                    print('|  ', end=' ')
                else:
                    print('| %s' % x[y].value, end=' ')
            print("|")
        print(horizontal_line)

    def display_current_player(self, player: AbstractPlayer):
<<<<<<< HEAD
        print("Player " + str(player.identifier) + " (" + str(player) + "'s) turn!")
=======
        print(str(player) + "'s turn! (" + str(player.identifier) + ')')
>>>>>>> a4b586b40d4e393121f6f2422e6714cde84bef76

    def get_move(self):
        move = input('Enter your move (row, column): ')
        move = move.split(',')
        x = int(move[0]) - 1
        y = int(move[1]) - 1

        return x, y

    def display_valid_moves(self, player: AbstractPlayer):
        print("Valid moves:", self.model.get_valid_moves(player))

    def display_invalid_moves(self):
        print("Invalid move, please pick another spot.")

    def display_winner(self, winner):
        if winner == 1:
            print(str(self.model.p1.name) + " wins!") # player X
        else:
            print(str(self.model.p2.name) + " wins!")  # player X

    def display_player_skipped(self, player: AbstractPlayer):
        print(" ")
        # print(str(player) + "'s turn has been skipped!")
        # game explicitly states which player's turn is next

    def display_score(self):
        print(str(self.model.p1.name) + ": " + str(self.model.p1.score))
        print(str(self.model.p2.name) + ": " + str(self.model.p2.score))