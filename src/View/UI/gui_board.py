from View.abstract_view import AbstractView
from Model.game import Game
from Model.abstract_player import AbstractPlayer
from tkinter import messagebox
import tkinter as tk


# Constants
# DEFAULT_BOARD = 8
# BOARD_SIZE = DEFAULT_BOARD * 100
# BACKGROUND_COLOR = 'grey'
# BORDER_COLOR = 'black'
# BOARD_COLOR = 'green'

class GuiBoard(AbstractView):

    def __init__(self, model: Game):
        super().__init__(model)
        self.model = model
        self.root = tk.Tk()
        self.root.geometry("1000x1000")
        self.root.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=50, weight=1)
        self.root.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=50, weight=1)
        self.x = None
        self.y = None

    def display_board(self, valid_moves: list):

        board_view = self.model.get_board()
        self.root.board_frame = tk.Frame(self.root, width=600, height=600)
        self.root.board_frame.grid(row=0, column=0, columnspan=8, rowspan=8)

        for x in range(8):
            self.root.board_frame.rowconfigure(x, minsize=75)
            self.root.board_frame.columnconfigure(x, minsize=75)

        for i, x in enumerate(board_view):
            for y in range(8):
                if (y, i) in valid_moves:
                    self.root.board_frame.button = tk.Button(self.root, bg='red')
                    self.root.board_frame.button.grid(row=i, column=y, sticky='nsew')
                elif x[y].value == 0:
                    self.root.board_frame.button = tk.Button(self.root, bg='green')
                    self.root.board_frame.button.grid(row=i, column=y, sticky='nsew')
                else:
                    if x[y].value == 1:
                        self.root.board_frame.button = tk.Button(self.root, bg='black')
                        self.root.board_frame.button.grid(row=i, column=y, sticky='nsew')
                    else:
                        self.root.board_frame.button = tk.Button(self.root, bg='white')
                        self.root.board_frame.button.grid(row=i, column=y, sticky='nsew')

    def display_current_player(self, player: AbstractPlayer):
        """
        Prints a message to indicate current player's turn
        :param player: Number representative of the player who is up (int)
        :return: non
        """
        self.current_player = tk.Label(text="Player " + str(player.identifier) + " (" + str(player) + "'s) turn!",
                                       fg='black', font=('Arial', 20))
        self.current_player.grid(row=10, column=2, columnspan=3)

    def set_move(self, i, j):
        self.x = i
        self.y = j

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

        # return self.x, self.y

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
            # print(str(self.model.order[0].name) + " wins!")
            self.winner_one = tk.Label(text="STEVE WINS!", fg='black', font=('Arial', 50))
            self.winner_one.grid(row=3, column=1, columnspan=6)
        elif winner == 2:
            # print(str(self.model.order[1].name) + " wins!")  # player O
            self.winner_two = tk.Label(text="JILL WINS!", fg='black', font=('Arial', 50))
            self.winner_two.grid(row=3, column=1, columnspan=6)
        else:
            self.winner_tie = tk.Label(text="TIE GAME!", fg='black', font=('Arial', 50))
            self.winner_tie.grid(row=3, column=1, columnspan=6)

    def display_player_skipped(self, player: AbstractPlayer):
        """
        Alerts player their turn has been skipped via print statement
        :param player: Player whose turn's been skipped
        :return: none
        """
        messagebox.showerror('Player Skipped!')

    def display_score(self):
        """
        Displays the current score of both players alongside their names
        :return: none
        """
        # print(str(self.model.order[0].name) + ": " + str(self.model.order[0].score))
        # print(str(self.model.order[1].name) + ": " + str(self.model.order[1].score))

        self.score_one = tk.Label(text="Jill's Score: 10",
                                       fg='black', font=('Arial', 20))
        self.score_one.grid(row=9, column=0, columnspan=3)
        self.score_two = tk.Label(text="Steve's Score: 20",
                                       fg='black', font=('Arial', 20))
        self.score_two.grid(row=9, column=4, columnspan=3)
    def display_end_of_game(self):
        """
        Alerts the players that the game is over
        :return: none
        """
        self.game_end = tk.Label(text="GAME SET!", fg='black', font=('Arial', 50))
        self.game_end.grid(row=3, column=2, columnspan=5)
