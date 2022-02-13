from abstract_view import AbstractView


class TextView:

    def displayBoard(BoardView):

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
