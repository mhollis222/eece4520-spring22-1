import tkinter as tk
from Controller.client import ReversiClient
from View.UI.settings_window import SettingsWindow
from tkinter import messagebox
import configparser

from pathlib import Path
path_parent = Path(__file__).resolve().parents[3]
settings_path = path_parent.joinpath('settings.ini').as_posix()


class MatchmakingOptionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title('Matchmaking Options Page')
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)
        self.client = ReversiClient()
        self.player = None

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_root)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        # first line
        self.label1 = tk.Label(self, text='Do you wish to resume the previous game,', fg='white',
                               font=("Arial", 30, "bold"), bg='green')
        self.label1.grid(row=1, columnspan=3, sticky=tk.S)
        # yes button
        self.challenge_button = tk.Button(self, text='Yes', width=30, height=2, font=("Arial", 15),
                                          command=self.save)
        self.challenge_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # no button
        self.challenge_button = tk.Button(self, text='No', width=30, height=2, font=("Arial", 15),
                                          command=self.no_save)
        self.challenge_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

    def open_root(self):
        """Naviagtes to the login page"""
        self.destroy()
        self.master.deiconify()  # show the root window

    def save(self):
        self.config['Model']['save'] = 'yes'
        self.save_preferences()
        settings_options_win = SettingsWindow(self)
        settings_options_win.focus_force()
        self.withdraw()

    def no_save(self):
        self.config['Model']['save'] = 'no'
        self.save_preferences()
        settings_options_win = SettingsWindow(self)
        settings_options_win.focus_force()
        self.withdraw()

