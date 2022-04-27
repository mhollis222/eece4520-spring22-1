import tkinter as tk
from PIL import Image, ImageTk
from Model.ai_player import AIPlayer
from Controller.game_controller import GameController
from View.UI.gui_board import GuiBoard
from Model.human_player import HumanPlayer
from View.UI.player_color import ChoosePlayerColor
from View.UI.board_size import TempWindow
from View.UI.board_align import AlignmentWindow
import configparser
from Controller.client import ReversiClient
from Model.game import Game
from Model.game_decorator_ai import GameDecoratorAI
from Controller.message import ReversiMessage as msg
from pathlib import Path
from Model.online_player import OnlinePlayer
from View.UI.matchmaking_error_window import MatchmakingErrorWindow

path_parent = Path(__file__).resolve().parents[3]
settings_path = path_parent.joinpath('settings.ini').as_posix()
preference_path = path_parent.joinpath('preferences.ini').as_posix()


def apply_path(path):
    return Path(__file__).resolve().parents[0].joinpath(path).as_posix()


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client = ReversiClient()
        self.title("Settings Window")
        self.geometry("2000x2000")
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(preference_path)
        self.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')
        self.config_settings = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config_settings.read(settings_path)

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')

        # title
        self.label1 = tk.Label(self, text='Settings', fg='white', font=("Arial", 55, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)

        # board size
        self.size_image = Image.open(apply_path('images/dimension.png'))
        self.size_image = self.size_image.resize((220, 165))
        self.size_image = ImageTk.PhotoImage(self.size_image)
        self.size_button = tk.Button(self, width=400, height=250, text="Board Size", image=self.size_image,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.board_size)
        self.size_button.grid(row=1, column=0, padx=50, sticky='s')

        # color button
        self.color_image = Image.open(apply_path('images/color.png'))
        self.color_image = self.color_image.resize((175, 175))
        self.color_image = ImageTk.PhotoImage(self.color_image)
        self.color_button = tk.Button(self, width=400, height=250, text="Color",
                                      image=self.color_image, bg='#41ab24',
                                      activebackground='green', compound=tk.TOP, fg='white',
                                      font=("Arial", 17), command=self.open_colors)
        self.color_button.grid(row=1, column=1, padx=50, sticky='s')

        # board alignment
        self.board_image = Image.open(apply_path('images/startboard.jpg'))
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
        if self.config_settings['Model']['mode'] == 'local':
            self.play_local()
        elif self.config_settings['Model']['mode'] == 'match' and self.config_settings['Model']['save'] == 'no':
            self.play_match()
        elif self.config_settings['Model']['mode'] == 'online':
            self.play_online()
        elif self.config_settings['Model']['mode'] == 'match' and self.config_settings['Model']['save'] == 'yes':
            self.play_recover()
        else:
            self.play_ai()

    def play_local(self):
        """Starts a game locally for the user"""
        player1 = HumanPlayer(self.config['User']['username'])
        player2 = HumanPlayer("Guest")
        controller = GameController(player1, player2, False)
        controller.save_settings()
        controller.setup()
        controller.play_game()
        game_win = GuiBoard(self)
        game_win.focus_force()
        self.withdraw()

    def play_ai(self):
        player1 = HumanPlayer(self.config['User']['username'])
        player2 = AIPlayer("Computer", int(self.config_settings['Model']['ai_difficulty']))
        game = Game(player1, player2)
        dec = GameDecoratorAI(game)
        game.start()
        player2.add_simulator(dec)
        player2.add_opp(player1)
        controller = GameController(player1, player2, True)
        controller.save_settings()
        controller.setup()
        game_win = GuiBoard(self)
        game_win.focus_force()
        self.withdraw()

    def play_match(self):
        # try:
        self.client.send_request(msg('get_elo', ['PLAY MATCH SELECTED']))
        human_username = self.client.username
        human_elo = self.client.send_request(msg('get_elo', [human_username]))
        details = self.client.send_request(msg('request_game', [human_username, human_elo]))
        resp = 'TIMEOUT'
        count = 0
        while resp == 'TIMEOUT' and count < 12:
            resp = self.client.send_request(msg('rcv_message', [human_username]))
            count += 1
        game_id = resp[1]
        opponent_username = resp[0]
        order = resp[2]
        player1 = HumanPlayer(human_username)
        player2 = OnlinePlayer(opponent_username, game_id, human_username)
        if order[0] == human_username:
            g_order = [player1, player2]
        else:
            g_order = [player2, player1]
        controller = GameController(player1, player2, False, game_id, False, g_order=g_order)
        # anything below here never runs..
        controller.save_settings()
        controller.setup()
        game_win = GuiBoard(self)
        game_win.focus_force()
        self.withdraw()
        self.withdraw()
        # except BaseException as e:
        #     error_win = MatchmakingErrorWindow(self)
        #     error_win.focus_force()
        #     self.withdraw()

    def play_recover(self):
        human_username = self.client.username
        game = self.client.send_request(msg('get_game_by_user', [human_username]))
        self.client.send_request(msg('get_elo', ['PRE-CHECK']))
        if not game:
            return self.play_match()
        self.client.send_request(msg('get_elo', ['POST-CHECK']))
        game_id = game[0]
        participants = self.client.send_request(msg('get_game_participants', [game_id]))
        opponent_username = ""
        for player in participants:
            if player != human_username:
                opponent_username = player
        self.client.send_request(msg('challenge', [human_username, opponent_username]))
        resp = 'TIMEOUT'
        count = 0
        while resp == 'TIMEOUT' and count < 12:
            resp = self.client.send_request(msg('rcv_message', [human_username]))
            count += 1
        order = self.client.send_request(msg('get_game_state', [game_id]))[1]
        player1 = HumanPlayer(human_username)
        player2 = OnlinePlayer(opponent_username, game_id, human_username)
        if order[0] == human_username:
            g_order = [player1, player2]
        else:
            g_order = [player2, player1]
        controller = GameController(player1, player2, False, game_id, reconstruct=True, g_order=g_order)
        controller.save_settings()
        controller.setup()
        game_win = GuiBoard(self)
        game_win.focus_force()
        self.withdraw()
        self.withdraw()
