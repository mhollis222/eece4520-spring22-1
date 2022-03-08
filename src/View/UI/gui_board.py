from View.abstract_view import AbstractView
from Model.game import Game
from Model.abstract_player import AbstractPlayer
from tkinter import messagebox
import tkinter as tk
from View.UI.reversi_button import ReversiButton


# Constants
# DEFAULT_BOARD = 8
# BOARD_SIZE = DEFAULT_BOARD * 100
# BACKGROUND_COLOR = 'grey'
# BORDER_COLOR = 'black'
# BOARD_COLOR = 'green'


class GuiBoard(AbstractView):

    def __init__(self, model: Game, p1_color: str, p2_color: str, controller):
        super().__init__(model)
        self.model = model
        self.controller = controller
        self.p1_color = p1_color
        self.p2_color = p2_color
        self.valid_color = 'red'
        self.empty_color = 'green'
        self.root = tk.Tk()
        self.root.geometry("1000x1000")
        self.root.rowconfigure(list(range(len(self.model.get_board()) + 3)), minsize=50, weight=1)
        self.root.columnconfigure(list(range(len(self.model.get_board()[0]))), minsize=50, weight=1)
        self.board_frame = tk.Frame(self.root, width=600, height=600)
        self.board_frame.grid(row=0, column=0, columnspan=len(self.model.get_board()[0]), rowspan=len(self.model.get_board()))

    def display_board(self, valid_moves: list):
        self.board_frame.grid_forget()
        board_view = self.model.get_board()


        for x in range(len(board_view)):
            self.board_frame.rowconfigure(x, minsize=75)
            self.board_frame.columnconfigure(x, minsize=75)

        for i, x in enumerate(board_view):
            for y in range(len(board_view[0])):
                if (y, i) in valid_moves:
                    button = ReversiButton(i, y, '0_0', callback=self.controller.advance, state=tk.ACTIVE, color=self.valid_color)
                    button.grid(row=i, column=y, sticky='nsew')
                elif x[y].value == 0:
                    button = ReversiButton(i, y, 'empty', callback=self.controller.advance, state=tk.DISABLED, color=self.empty_color)
                    button.grid(row=i, column=y, sticky='nsew')
                elif x[y].value == 1:
                    button = ReversiButton(i, y, 'p1', callback=self.controller.advance, state=tk.DISABLED, color=self.p1_color)
                    button.grid(row=i, column=y, sticky='nsew')
                else:
                    button = ReversiButton(i, y, 'p2', callback=self.controller.advance, state=tk.DISABLED, color=self.p2_color)
                    button.grid(row=i, column=y, sticky='nsew')

    def display_current_player(self, player: AbstractPlayer):
        """
        Prints a message to indicate current player's turn
        :param player: Number representative of the player who is up (int)
        :return: non
        """
        self.current_player = tk.Label(text="Player " + str(player.identifier) + " (" + str(player) + "'s) turn!",
                                       fg='black', font=('Arial', 20))
        self.current_player.grid(row=10, column=2, columnspan=3)


    def get_move(self):
        """
        Takes in user input for x and y
        :return: x and y
        """

        return self.x.get(), self.y.get()

    def display_invalid_moves(self, player):
        """
        Prints message indicating that move made was invalid
        :param player: Number representative of the player who made the invalid move (int)
        :return: none
        """
        messagebox.showerror('Player Skipped!')

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

        self.score_one = tk.Label(text=str(self.model.order[0].name) + ": " + str(self.model.order[0].score),
                                  fg='black', font=('Arial', 20))
        self.score_one.grid(row=9, column=0, columnspan=3)
        self.score_two = tk.Label(text=str(self.model.order[1].name) + ": " + str(self.model.order[1].score),
                                  fg='black', font=('Arial', 20))
        self.score_two.grid(row=9, column=4, columnspan=3)

    def display_end_of_game(self):
        """
        Alerts the players that the game is over
        :return: none
        """
        self.game_end = tk.Label(text="GAME SET!", fg='black', font=('Arial', 50))
        self.game_end.grid(row=3, column=2, columnspan=5)
