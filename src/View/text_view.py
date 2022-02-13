from Model.Game import Game


class TextView:

    def drawBoard(board: Game):

        # constants for drawing board borders
        horizontalLine = ' +---+---+---+---+---+---+---+---+'
        verticalLine = ' |   |   |   |   |   |   |   |   |'

        # nested for loop to draw in board
        print(horizontalLine)
        for i in range(8):
            print(verticalLine)

            for j in range(8):
                print('| %s' % (board[i][j]), end=' ')
                print('|')
                print(verticalLine)
                print(horizontalLine)


def restartBoard(board):
    # fills entire board with blanks
    for i in range(8):
        for j in range(8):
            board[i][j] = ' '

    # Starting position
    board[3][3] = 'X'
    board[4][4] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
