from View.abstract_view import AbstractView
from Model.game import Game
from Model.abstract_player import AbstractPlayer
from tkinter import messagebox
from game_window import GameWindow
import tkinter as tk
# from termcolor import colored


class GUIView(AbstractView):

    def __init__(self, model: Game): # , p1_color: str, p2_color: str
        super().__init__(model)
        self.model = model
        # self.p1_color = p1_color
        # self.p2_color = p2_color
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.i = None
        self.j = None


    def display_board(self, valid_moves: list):
        """
        Prints a 8 by 8 board and fills in pieces as game goes on
        :return: none
        """

        self.board_frame = tk.Frame(self, width=600, height=600)
        self.board_frame.grid(row=1, column=0, columnspan=3)

        for i in range(8):
            self.board_frame.rowconfigure(i, minsize=75)
            self.board_frame.columnconfigure(i, minsize=75)

        for i in range(8):
            for j in range(8):
                # if # empty

                # elif # player 1

                # else # player 2
                # self.black_dot = Image.open('black-circle.png')
                # self.black_dot = self.black_dot.resize((175, 175))
                # self.black_dot = ImageTk.PhotoImage(self.black_dot)
                # self.button = tk.Button(self, bg='green', image=self.black_dot, text=f'({i},{j})',
                #                    command=lambda arg=(i, j): self.button_clicked(arg))
                self.board_frame.button = tk.Button(self, bg='black', text=f'({i},{j})',
                                   command=lambda arg=(i, j): self.set_move(arg))
                self.board_frame.button.grid(row=i, column=j, sticky='nsew')
        # game_win = GameWindow(self.master)
        # game_win.focus_force()
        # self.destroy()




    def display_current_player(self, player: AbstractPlayer):
        """
        Prints a message to indicate current player's turn
        :param player: Number representative of the player who is up (int)
        :return: non
        """

        # CurrentPlayerStatus.current_player(str(player))
        print("Player " + str(player.identifier) + " (" + str(player) + "'s) turn!")

        self.current_player = tk.Label(text="Player " + str(player.identifier) + " (" + str(player) + "'s) turn!",
                                       fg='black', font=('Arial', 20))
        self.current_player.grid(row=4, column=0, columnspan=3)

    def set_move(self, x, y):
        self.i = x
        self.j = y

    def get_move(self):
        """
        Takes in user input for x and y
        :return: x and y
        """
        if self.i==None and self.j==None

        return self.i, self.j

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

        messagebox.showerror('Invalid Move!', 'Please pick another spot!')

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
        # CurrentPlayerStatus.current_score1(str(self.model.order[0].score))
        # CurrentPlayerStatus.current_score2(str(self.model.order[1].score))

        print(str(self.model.order[0].name) + ": " + str(self.model.order[0].score))
        print(str(self.model.order[1].name) + ": " + str(self.model.order[1].score))

    def display_end_of_game(self):
        """
        Alerts the players that the game is over
        :return: none
        """
        print("\n")
        print("Game Over!")