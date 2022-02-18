from View.abstract_view import AbstractView
from Model.Game import Game
from Model.AbstractPlayer import AbstractPlayer


class TextView(AbstractView):

    def __init__(self, model: Game):
        super().__init__(model)
        self.model = model

    def display_board(self):
        """
        Prints a 8 by 8 board and fills in pieces as game goes on
        :return: none
        """
        board_view = self.model.get_board()

        # constants for drawing board borders
        horizontal_line = '   +---+---+---+---+---+---+---+---+'

        # nested for loop to draw in board
        print('     1   2   3   4   5   6   7   8')
        print(horizontal_line)
        for i, x in enumerate(board_view):
            print(i + 1, end='  ')
            for y in range(8):
                if x[y].value == 0:
                    print('|  ', end=' ')
                else:
                    print('| %s' % x[y].value, end=' ')
            print("|")
        print(horizontal_line)

    def display_current_player(self, player: AbstractPlayer):
        """
        Prints a message to indicate current player's turn
        :param player: Number representative of the player who is up (int)
        :return: non
        """
        print("Player " + str(player.identifier) + " (" + str(player) + "'s) turn!")

    def get_move(self):
        """
        Takes in user input for x and y
        :return: x and y
        """
        move = input('Enter your move (row, column): ')
        move = move.split(',')
        x = int(move[0]) - 1
        y = int(move[1]) - 1

        return x, y

    def display_invalid_moves(self, player):
        """
        Prints message indicating that move made was invalid
        :param player: Number representative of the player who made the invalid move (int)
        :return: none
        """
        print("Invalid move, please pick another spot.")
        print("Try these instead:")
        print(str(self.model.get_valid_moves(player)))

    def display_winner(self, winner):
        """
        Prints who won the game
        :param winner: Number representative of the player who won the game (int)
        :return: none
        """
        if winner == 1:
            print(str(self.model.order[0].name) + " wins!")  # player X
        elif winner == 2:
            print(str(self.model.order[1].name) + " wins!")  # player O
        else:
            print("Tie Game!")

    def display_player_skipped(self, player: AbstractPlayer):
        """
        Alerts player their turn has been skipped via print statement
        :param player: Player whose turn's been skipped
        :return: none
        """
        print(" ")
        print(str(player) + "'s turn has been skipped!")

    def display_score(self):
        """
        Displays the current score of both players alongside their names
        :return: none
        """
        print(str(self.model.order[0].name) + ": " + str(self.model.order[0].score))
        print(str(self.model.order[1].name) + ": " + str(self.model.order[1].score))

    def display_end_of_game(self):
        """
        Alerts the players that the game is over
        :return: none
        """
        print("\n")
        print("Game Over!")
