from View.abstract_view import AbstractView
from Model.Game import Game


class TextView(AbstractView):

    def display_board(self, model: Game):
        BoardView = model.getBoard()

        # constants for drawing board borders
        horizontalLine = '  +---+---+---+---+---+---+---+---+'
        verticalLine = '  |   |   |   |   |   |   |   |   |'

        # nested for loop to draw in board
        print('    1   2   3   4   5   6   7   8')
        print(horizontalLine)
        for i in range(8):
            print(verticalLine)
            print(i + 1, end=' ')

            for j in range(8):
                print('| %s' % (BoardView[i][j]), end=' ')
                print('|')
                print(verticalLine)
                print(horizontalLine)

    def display_current_player(self, player):
        print(str(player) + "'s turn!")

    def get_move(self):
        move = input('Enter your move (x, y): ')
        move = move.split(',')
        x = int(move[0]) - 1
        y = int(move[1]) - 1

        return x, y

    def display_valid_moves(self):
        pass

    def display_invalid_moves(self):
        print("Invalid move, please pick another spot.")

    def display_winner(self, winner):
        if winner == 1:
            print("X wins")
        else:
            print("O wins")

