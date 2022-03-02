from View.abstract_view import AbstractView
from Model.game import Game
from Model.abstract_player import AbstractPlayer
import tkinter as tk


# Constants
DEFAULT_BOARD = 8
BOARD_SIZE = DEFAULT_BOARD * 100
BACKGROUND_COLOR = 'grey'
BORDER_COLOR = 'black'
BOARD_COLOR = 'green'

class gui_board(AbstractView):

    def __init__(self, model: Game):
        super().__init__(model)
        self.model = model
        self.root = tk.Tk()
        self.root.geometry(str(BOARD_SIZE) + 'x' + str(BOARD_SIZE))
        self.root.configure(background=BACKGROUND_COLOR)

    def display_board(self, valid_moves: list):
        board_view = self.model.get_board()
        # main_frame = tk.Frame(self.root, bg='white', width=100, height=100)
        for i, x in enumerate(board_view):
            for y in range(DEFAULT_BOARD):
                if (y, i) in valid_moves:
                    board_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1, bg=BORDER_COLOR)
                    board_frame.grid(row=i, column=y)
                    board_button = tk.Button(master=board_frame, bg=BOARD_COLOR, width=int(BOARD_SIZE / 200),
                                             height=int(BOARD_SIZE / 400), text=' X')
                    board_button.pack()
                elif x[y].value == 0:
                    board_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1, bg=BORDER_COLOR)
                    board_frame.grid(row=i, column=y)
                    board_button = tk.Button(master=board_frame, bg=BOARD_COLOR, width=int(BOARD_SIZE / 200),
                                             height=int(BOARD_SIZE / 400))
                    board_button.pack()
                else:
                    board_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1, bg=BORDER_COLOR)
                    board_frame.grid(row=i, column=y)
                    board_button = tk.Button(master=board_frame, bg=BOARD_COLOR, width=int(BOARD_SIZE / 200),
                                             height=int(BOARD_SIZE / 400))
                    board_button.pack()


        # # constants for drawing board borders
        # horizontal_line = '   +---+---+---+---+---+---+---+---+'
        #
        # # nested for loop to draw in board
        # print('     1   2   3   4   5   6   7   8')
        # print(horizontal_line)
        # for i, x in enumerate(board_view):
        #     print(i + 1, end='  ')
        #     for y in range(8):
        #         if (y, i) in valid_moves:
        #             print('| .', end=' ')
        #         elif x[y].value == 0:
        #             print('|  ', end=' ')
        #         else:
        #             print('| %s' % x[y].value, end=' ')
        #     print("|")
        # print(horizontal_line)

    def display_current_player(self, player: AbstractPlayer):
        """
        Prints a message to indicate current player's turn
        :param player: Number representative of the player who is up (int)
        :return: non
        """
        print("Player " + str(player.identifier) + " (" + str(player) + "'s) turn!")

        player_frame = tk.Frame(self.root, width=BOARD_SIZE, height=50)
        player_frame.pack(side=tk.BOTTOM)

        player_label = tk.Label(master=player_frame,
                                text="Player " + str(player.identifier) + " (" + str(player) + "'s) turn!")

    def get_move(self):
        """
        Takes in user input for x and y
        :return: x and y
        """
        while True:
            move = input('Enter your move (row, column): ')
            move = move.split(',')
            try:
                # Flipped since we ask for `row, col`: row -> y, col -> x
                x = int(move[1]) - 1
                y = int(move[0]) - 1
                break
            except ValueError:
                print("Could not convert data to an integer.")
        return x, y

    def display_invalid_moves(self, player):
        """
        Prints message indicating that move made was invalid
        :param player: Number representative of the player who made the invalid move (int)
        :return: none
        """
        print("Invalid move, please pick another spot.")
        print("Try these instead:")
        for i in self.model.get_valid_moves(player):
            print("(", i[1] + 1, ",", i[0] + 1, end=" ) ", )
        print("\n")

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
