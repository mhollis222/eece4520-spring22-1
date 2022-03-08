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
        self.valid_color = 'yellow'
        self.empty_color = 'green'
        self.root = tk.Tk()
        self.root.title('Reversi')
        self.root.geometry("2000x2000")
        self.root.rowconfigure(0, minsize=600, weight=1)
        self.root.rowconfigure(1, minsize=100, weight=1)
        self.root.rowconfigure(2, minsize=100, weight=1)
        self.root.columnconfigure(0, minsize=600, weight=1)
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=0, column=0, sticky='NWES')
        self.notice_frame = tk.Frame(self.root)
        self.notice_frame.grid(row=1, column=0, sticky='NWES')
        self.score_frame = tk.Frame(self.root)
        self.score_frame.grid(row=2, column=0, sticky='NWES')

    def display_board(self, valid_moves: list):
        self.board_frame.destroy()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=0, column=0, sticky='NWES')
        board_view = self.model.get_board()

        for x in range(len(board_view)):
            self.board_frame.rowconfigure(x, minsize=75, weight=1)
            self.board_frame.columnconfigure(x, minsize=75, weight=1)

        for i, x in enumerate(board_view):
            for y in range(len(board_view[0])):
                if (y, i) in valid_moves:
                    button = ReversiButton(self.board_frame, i, y, '', callback=self.controller.advance,
                                           state=tk.ACTIVE, color=self.valid_color)
                    button.grid(row=i, column=y, sticky='nsew')
                elif x[y].value == 0:
                    button = ReversiButton(self.board_frame, i, y, '', callback=self.controller.advance,
                                           state=tk.DISABLED, color=self.empty_color)
                    button.grid(row=i, column=y, sticky='nsew')
                elif x[y].value == 1:
                    button = ReversiButton(self.board_frame, i, y, '', callback=self.controller.advance,
                                           state=tk.DISABLED, color=self.p1_color)
                    button.grid(row=i, column=y, sticky='nsew')
                else:
                    button = ReversiButton(self.board_frame, i, y, '', callback=self.controller.advance,
                                           state=tk.DISABLED, color=self.p2_color)
                    button.grid(row=i, column=y, sticky='nsew')

    def display_current_player(self, player: AbstractPlayer):
        """
        Prints a message to indicate current player's turn
        :param player: Number representative of the player who is up (int)
        :return: none
        """
        self.notice_frame.destroy()
        self.notice_frame = tk.Frame(self.root, bg='#343434')
        self.notice_frame.grid(row=1, column=0, sticky='NWES')
        color = self.p1_color if player.identifier == 1 else self.p2_color
        current_player = tk.Label(self.notice_frame, text=str(player) + "'s turn! (" + color + ')',
                                       bg='#343434', fg='white', font=('Arial', 20), pady=30)
        current_player.pack()

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
        self.notice_frame.destroy()
        self.notice_frame = tk.Frame(self.root, bg='#343434')
        self.notice_frame.grid(row=1, column=0, sticky='NWES')
        if winner == 1:
            # print(str(self.model.order[0].name) + " wins!")
            winner_one = tk.Label(self.notice_frame, text=str(self.model.order[0].name) + " wins!", fg='yellow',
                                  bg='#343434', font=('Arial', 50), pady=30)
            winner_one.pack()
        elif winner == 2:
            # print(str(self.model.order[1].name) + " wins!")  # player O
            winner_two = tk.Label(self.notice_frame, text=str(self.model.order[1].name) + " wins!",
                                  bg='#343434', fg='yellow', font=('Arial', 50), pady=30)
            winner_two.pack()
        else:
            winner_tie = tk.Label(self.notice_frame, text="TIE GAME!", fg='yellow', font=('Arial', 50), pady=30)
            winner_tie.pack()

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
        self.score_frame.destroy()
        self.score_frame = tk.Frame(self.root, bg='#343434')
        self.score_frame.columnconfigure(0, minsize=300, weight=1)
        self.score_frame.columnconfigure(1, minsize=300, weight=1)
        self.score_frame.grid(row=2, column=0, sticky='NWES')

        self.score_frame.score_one = tk.Label(self.score_frame,
                                              text=str(self.model.order[0].name) + ": " +
                                                   str(self.model.order[0].score), bg='#343434',
                                              fg='white', font=('Arial', 20))
        self.score_frame.score_one.grid(row=2, column=0, columnspan=2, sticky='w', padx=75)
        self.score_frame.score_two = tk.Label(self.score_frame,
                                              text=str(self.model.order[1].name) + ": " +
                                                   str(self.model.order[1].score), fg='white', font=('Arial', 20),
                                              bg='#343434')
        self.score_frame.score_two.grid(row=2, column=0, columnspan=2, sticky='ne', padx=100)

    def display_end_of_game(self):
        """
        Alerts the players that the game is over
        :return: none
        """
        pass
