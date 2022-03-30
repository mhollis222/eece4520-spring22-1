import tkinter as tk
from tkinter import messagebox
from Model.database import Database
from home_window import HomeWindow
import configparser


from pathlib import Path
path_parent = Path(__file__).resolve().parents[3]
preference_path = path_parent.joinpath('preferences.ini').as_posix()


class SignUpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # special options to save comments on writes (i hope)
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(preference_path)

        self.title("Registration Page")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=50, weight=1)
        self.columnconfigure([0, 1], minsize=50, weight=1)
        self.configure(bg='green')

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        # title
        self.register_label = tk.Label(self, text='Sign Up Page', fg='white', font=("Arial", 35, "bold"), bg='green')
        self.register_label.grid(row=1, columnspan=2, sticky=tk.N)
        # username
        self.new_username_label = tk.Label(self, text='Username:', bg='green', font=("Arial", 18), fg='white')
        self.new_username_label.grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        self.new_username_entry = tk.Entry(self, font=("Arial", 18))
        self.new_username_entry.grid(row=2, column=1, sticky='nw', padx=15, pady=5)
        # password
        self.new_password_label = tk.Label(self, text='Password:', bg='green', font=("Arial", 18), fg='white')
        self.new_password_label.grid(row=3, column=0, sticky='ne', padx=5, pady=5)
        self.new_password_entry = tk.Entry(self, show='*', font=("Arial", 18))
        self.new_password_entry.grid(row=3, column=1, sticky='nw', padx=15, pady=5)
        # retype password
        self.retype_password_label = tk.Label(self, text='Confirm Password:', bg='green', font=("Arial", 18),
                                              fg='white')
        self.retype_password_label.grid(row=4, column=0, sticky='ne', padx=5, pady=5)
        self.retype_password_entry = tk.Entry(self, show='*', font=("Arial", 18))
        self.retype_password_entry.grid(row=4, column=1, sticky='nw', padx=15, pady=5)
        # register button
        self.register_button = tk.Button(self, text='Register', width=20, height=2, font=("Arial", 15),
                                         command=self.register)
        self.register_button.grid(row=4, columnspan=2, padx=5, pady=50, sticky='s')

    def open_login(self):
        """Navigates to the login page"""
        self.destroy()
        self.master.deiconify()

    def open_home(self, username):
        """Navigates to the home page"""
        self.config['User']['username'] = username
        self.save_preferences()
        home_win = HomeWindow(self)
        home_win.focus_force()
        self.withdraw()

    def register(self):
        """Attempts to write a new user object to the database"""
        db = Database('localhost', 'reversi', 'eece4520')
        if self.new_username_entry.get() == '' :
            messagebox.showerror('Register failure', 'Username cannot be empty.')
        elif self.new_password_entry.get() == '':
            messagebox.showerror('Register failure', 'Password cannot be empty.')
        elif db.write_user(self.new_username_entry.get(), self.new_password_entry.get()) == -1:
            print("registration failed")
            messagebox.showerror('Register failure', 'Username already exists.')
        elif self.new_password_entry.get() != self.retype_password_entry.get():
            print("Password entries do not match.")
            messagebox.showerror('Mismatched Passwords', 'Password entries do not match.')
        else:
            self.open_home(self.new_username_entry.get())

    def save_preferences(self) -> bool:
        """
        Stores the desired settings dict as a yaml file at `settings_path`
        :param settings: the settings to be stored.
        :return: success of operation
        """
        with open(preference_path, 'w') as f:
            self.config.write(f)
