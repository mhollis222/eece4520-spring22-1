import tkinter as tk
from PIL import Image, ImageTk
from game_controller import GameController
from gui_board import GuiBoard
from human_player import HumanPlayer
from player_color import ChoosePlayerColor
from board_size import TempWindow
from board_align import AlignmentWindow
import configparser


preferences_path = '../../preferences.ini'


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings Window")
        self.geometry("2000x2000")
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(preferences_path)
        self.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')

        # title
        self.label1 = tk.Label(self, text='Settings', fg='white', font=("Arial", 55, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)

        # board size
        self.size_image = Image.open('../View/UI/images/dimension.png')
        self.size_image = self.size_image.resize((220, 165))
        self.size_image = ImageTk.PhotoImage(self.size_image)
        self.size_button = tk.Button(self, width=400, height=250, text="Board Size", image=self.size_image,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.board_size)
        self.size_button.grid(row=1, column=0, padx=50, sticky='s')

        # color button
        self.color_image = Image.open('../View/UI/images/color.png')
        self.color_image = self.color_image.resize((175, 175))
        self.color_image = ImageTk.PhotoImage(self.color_image)
        self.color_button = tk.Button(self, width=400, height=250, text="Color",
                                      image=self.color_image, bg='#41ab24',
                                      activebackground='green', compound=tk.TOP, fg='white',
                                      font=("Arial", 17), command=self.open_colors)
        self.color_button.grid(row=1, column=1, padx=50, sticky='s')

        # board alignment
        self.board_image = Image.open('../View/UI/images/startboard.jpg')
        self.board_image = self.board_image.resize((170, 170))
        self.board_image = ImageTk.PhotoImage(self.board_image)
        self.board_button = tk.Button(self, width=400, height=250, text="Alignment", image=self.board_image,
                                      bg='#41ab24', activebackground='green', compound=tk.TOP, fg='white',
                                      font=("Arial", 17), command=self.board_alignment)
        self.board_button.grid(row=1, column=2, padx=50, sticky='s')

        # Start Game
        self.guest_play_button = tk.Button(self, text='Start Game', width=30, height=2,
                                           fg='black', font=("Arial", 15), command=self.start_game)
        self.guest_play_button.grid(row=2, columnspan=4, sticky='n', pady=90)

    # show the root window
    def open_login(self):
        """Navigates to login page"""
        self.destroy()
        self.master.deiconify()

    # function call to change board size 
    def board_size(self):
        """Allows user to change board size"""
        board = TempWindow(self)
        board.focus_force()
        self.withdraw()

    # function call to change colors
    def open_colors(self):
        color_win = ChoosePlayerColor(self)
        color_win.focus_force()
        self.withdraw()

    # function call to change board alignment
    def board_alignment(self):
        """Allows user to set the rules of game"""
        board = AlignmentWindow(self)
        board.focus_force()
        self.withdraw()

    # function call to start game
    def start_game(self):
        """Starts a game locally for the user"""
        player1 = HumanPlayer(self.config['User']['username'])
        player2 = HumanPlayer("Guest")
        controller = GameController(player1, player2)
        controller.save_settings()
        controller.setup()
        controller.play_game()
        game_win = GuiBoard(self)
        game_win.focus_force()
        self.withdraw()