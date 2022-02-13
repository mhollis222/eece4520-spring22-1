from Model.Game import Game

# TODO: Make an abstractView class, and have this one implement it
# TODO: restarting the board should realistically be handled by the controller
# TODO: also something to keep in mind is it might be nice to have the numbering
#  for coordinates printed alongside the board



class TextView:

    def drawBoard(board: Game):

        # constants for drawing board borders
        horizontalLine = ' +---+---+---+---+---+---+---+---+'
        verticalLine = ' |   |   |   |   |   |   |   |   |'

        # nested for loop to draw in board
        print(horizontalLine)
        # TODO: for the demo we can maybe get away with hard coding these values,
        #  but realistically this should be able render a board of any size
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
