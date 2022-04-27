import tkinter as tk
from Controller.client import ReversiClient
from Controller.message import ReversiMessage as msg
from tkinter import messagebox
from View.UI.settings_window import SettingsWindow
import configparser
from Controller.client import ReversiClient

from pathlib import Path
path_parent = Path(__file__).resolve().parents[3]
preference_path = path_parent.joinpath('preferences.ini').as_posix()


class OnlineWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.client = ReversiClient()
        self.title('Online Challenge Page')
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(preference_path)
        self.client = ReversiClient()
        self.player = None
        self.human_username = None
        self.human_elo = None
        self.opponent_username = None
        self.opponent_elo = None

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_root)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        # title
        self.label1 = tk.Label(self, text='Challenge a User Online', fg='white', font=("Arial", 30, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)
        # list of online players
        self.players = tuple(self.client.send_request(msg('get_players', []))[0])
        self.players_var = tk.StringVar(value=self.players)
        self.listbox = tk.Listbox(listvariable=self.players_var)
        self.listbox.grid(row=1, columnspan=3, sticky=tk.S)
        # chosen player
        self.chosen_label = tk.Label(self, text='Opponent:', bg='green', font=("Arial", 20), fg='white')
        self.chosen_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.chosen_entry = tk.Entry(self, font=("Arial", 20))
        self.chosen_entry.grid(row=2, column=1, sticky=tk.W, padx=15, pady=5)
        # self.listbox.bind('<<ListboxSelect>>', self.player_selected)
        # challenge button
        self.challenge_button = tk.Button(self, text='Challenge', width=30, height=2, font=("Arial", 15),
                                          command=self.challenge)
        self.challenge_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.N)

    def open_root(self):
        """Naviagtes to the login page"""
        self.destroy()
        self.master.deiconify()  # show the root window

    def player_selected(self, event):
        selected_index = self.listbox.curselection()[0]
        self.player = self.listbox.get(selected_index)

    def challenge(self):
        if self.player is None:
            messagebox.showerror("", "You must select a player to challenge")
        else:
            self.player = self.chosen_entry.get()

            if self.player not in self.client.send_request(msg('get_players', []))[0]:
                self.human_username = self.client.username
                self.human_elo = self.client.send_request(msg('get_elo', [self.human_username]))
                self.opponent_username = self.player
                self.opponent_elo = self.client.send_request(msg('get_elo', [self.player]))
                details = self.client.send_request(msg('challenge', [self.human_username, self.opponent_username]))
                settings_options_win = SettingsWindow(self)
                settings_options_win.focus_force()
                self.withdraw()
            else:
                messagebox.showerror("", "Invalid Opponent. Please try again")



