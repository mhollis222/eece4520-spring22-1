import tkinter as tk
from tkinter import messagebox
from View.UI.signup_window import SignUpWindow
from View.UI.guest_play_options_window import GuestOptionsWindow
from View.UI.home_window import HomeWindow
from Controller.client import ReversiClient
from Controller.message import ReversiMessage as msg
import configparser


from pathlib import Path
path_parent = Path(__file__).resolve().parents[3]
preference_path = path_parent.joinpath('preferences.ini').as_posix()


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # special options to save comments on writes
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(preference_path)
        # self.setup()

        self.client = ReversiClient()

        self.title('Login Page')
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
        self.columnconfigure([0, 1], minsize=50, weight=1)
        self.configure(bg='green')

        # title
        self.label1 = tk.Label(self, text='Reversi', fg='white', font=("Arial", 55, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=2, sticky=tk.S)
        # username
        self.username_label = tk.Label(self, text='Username:', bg='green', font=("Arial", 20), fg='white')
        self.username_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 20))
        self.username_entry.grid(row=1, column=1, sticky=tk.W, padx=15, pady=5)
        # password
        self.password_label = tk.Label(self, text='Password:', bg='green', font=("Arial", 20), fg='white')
        self.password_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show='*', font=("Arial", 20))
        self.password_entry.grid(row=2, column=1, sticky=tk.W, padx=15, pady=5)
        # login button
        self.login_button = tk.Button(self, text='Login', width=30, height=2, font=("Arial", 15),
                                      command=self.login)
        self.login_button.grid(row=3, columnspan=2, padx=5, pady=5)
        self.login_button.bind(self, '<Enter>', self.login)
        # register link
        self.register_link = tk.Button(self, text='Not a member? Sign Up', fg='white', font=("Arial", 15), bg='green',
                                       activebackground='green', relief='flat', bd=0, command=self.open_signup)
        self.register_link.grid(row=4, columnspan=2, sticky=tk.N)
        # OR label
        self.or_label = tk.Label(self, text='-OR-', fg='white', font=("Arial", 15, "bold"), bg='green')
        self.or_label.grid(row=5, columnspan=2, sticky=tk.N)
        # Play as Guest button
        self.guest_play_button = tk.Button(self, text='Play as Guest', width=30, height=2,
                                           fg='black', font=("Arial", 15), command=self.open_guest_options)
        self.guest_play_button.grid(row=5, columnspan=2, sticky='n', pady=90)

    def login(self):
        """Attempts to successfully log into the database with the provided username and password"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.client.send_request(msg('log_in', [username, password]))[0]:
            self.config['User']['username'] = username
            self.save_preferences()
            self.client.username = username
            print("login successful")
            home_win = HomeWindow(self)
            home_win.focus_force()
            self.withdraw()
        else:
            messagebox.showerror('Login failure', 'Invalid Credentials')

    def close_window(self):
        """Closes the GUI window"""
        self.destroy()
        self.master.deiconify()  # show the root window

    def open_signup(self):
        """Naviagtes to the sign up page"""
        signup_win = SignUpWindow(self)
        signup_win.focus_force()
        self.withdraw()

    def open_guest_options(self):
        """Naviagtes to the game options window for guests"""
        guest_options_win = GuestOptionsWindow(self)
        guest_options_win.focus_force()
        self.withdraw()

    def save_preferences(self) -> bool:
        """
        Stores the desired settings dict as a yaml file at `settings_path`
        :param settings: the settings to be stored.
        :return: success of operation
        """
        with open(preference_path, 'w') as f:
            self.config.write(f)
