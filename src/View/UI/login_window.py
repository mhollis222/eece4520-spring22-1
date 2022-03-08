import tkinter as tk
from tkinter import messagebox
from game_window import GameWindow

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Login')

        self.resizable(0, 0)

        # username
        self.username_label = tk.Label(self, text='Username:')
        self.username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)

        # password
        self.password_label = tk.Label(self, text='Password:')
        self.password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

        # login button
        self.frame = tk.Frame(self)
        self.frame.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        self.login_button = tk.Button(self.frame, text='Login', width=5, command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button = tk.Button(self.frame, text='Cancel', width=5, command=self.close_window)
        self.cancel_button.pack(side=tk.LEFT)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def login(self):
        game_win = GameWindow(self.master)
        game_win.focus_force()
        self.destroy()
        # username = self.username_entry.get()
        # password = self.password_entry.get()
        #
        # if username == 'test' and password == '123456':
        #     game_win = GameWindow(self.master)
        #     game_win.focus_force()
        #     self.destroy()
        # else:
        #     messagebox.showerror('Login failure', 'Username or password is incorrect')

    def close_window(self):
        self.destroy()
        self.master.deiconify()  # show the root window






