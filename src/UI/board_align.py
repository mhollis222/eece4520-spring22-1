import tkinter as tk
import configparser
from tkinter import messagebox

settings_path = '../../settings.ini'


class AlignmentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # special options to save comments on writes (i hope)
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)
        self.title("Board Alignment Window")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')

        # title
        self.label1 = tk.Label(self, text='Should the game start in the middle?', fg='white',
                               font=("Arial", 35, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)

        self.yes_button = tk.Button(self, text='Yes', width=30, height=2,
                                           fg='black', font=("Arial", 15), command=self.agree)
        self.yes_button.grid(row=1, column=0, sticky='ne', pady=90)

        self.no_button = tk.Button(self, text='No', width=30, height=2,
                                           fg='black', font=("Arial", 15), command=self.disagree)
        self.no_button.grid(row=1, column=2, sticky='nw', pady=90)


    def open_login(self):
        self.destroy()
        self.master.deiconify()  # show the root window

    def save_preferences(self) -> bool:
        """
        Stores the desired settings dict as a yaml file at `settings_path`
        :param settings: the settings to be stored.
        :return: success of operation
        """
        with open(settings_path, 'w') as f:
            self.config.write(f)

    def agree(self):
        self.config['Model']['start_filled'] = 'True'
        self.save_preferences()
        messagebox.showerror("", "Game rules have successfully been updated")

    def disagree(self):
        self.config['Model']['start_filled'] = 'False'
        self.save_preferences()
        messagebox.showerror("", "Game rules have successfully been updated")
