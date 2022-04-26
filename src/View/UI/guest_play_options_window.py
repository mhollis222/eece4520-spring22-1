import tkinter as tk
from PIL import Image, ImageTk
from View.UI.difficulty_window1 import AIDifficultyIWindow
from View.UI.settings_window import SettingsWindow
import configparser
from pathlib import Path
path_parent = Path(__file__).resolve().parents[3]
settings_path = path_parent.joinpath('settings.ini').as_posix()


def apply_path(path):
    return Path(__file__).resolve().parents[0].joinpath(path).as_posix()


class GuestOptionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Guest Play Options")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.columnconfigure([0, 1], minsize=50, weight=1)
        self.configure(bg='green')
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)



        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        # title
        self.guest_title = tk.Label(self, text='Who do you want to play?',
                                    font=("Arial", 35, "bold"), bg='green', fg='white')
        self.guest_title.grid(row=1, column=0, columnspan=2, sticky=tk.N)
        # play person button
        self.person_image = Image.open(apply_path('images/user.png'))
        self.person_image = self.person_image.resize((175, 175))
        self.person_image = ImageTk.PhotoImage(self.person_image)
        self.person_button = tk.Button(self, width=400, height=250, text="Local Player", image=self.person_image,
                                       compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                       font=("Arial", 17), command=self.open_settings_options)
        self.person_button.grid(row=1, column=0, padx=50, sticky='s')
        # play computer button
        self.computer_image = Image.open(apply_path('images/computer.png'))
        self.computer_image = self.computer_image.resize((175, 175))
        self.computer_image = ImageTk.PhotoImage(self.computer_image)
        self.computer_button = tk.Button(self, width=400, height=250, text="Computer",
                                         image=self.computer_image, bg='#41ab24',
                                         activebackground='green', compound=tk.TOP, fg='white', font=("Arial", 17),
                                         command=self.open_AI)
        self.computer_button.grid(row=1, column=1, padx=50, sticky='s')

    def open_login(self):
        """Naviagtes to the login page"""
        self.destroy()
        self.master.deiconify()  # show the root window

    def open_AI(self):
        """Naviagtes to the AI settings window"""
        self.config['Model']['ai'] = str(True)
        self.save_preferences()
        ai_win = AIDifficultyIWindow(self)
        ai_win.focus_force()
        self.withdraw()

    def open_settings_options(self):
        """Naviagtes to the settings preference window"""
        self.config['Model']['ai'] = str(False)
        self.config['Model']['mode'] = 'local'
        self.save_preferences()
        settings_options_win = SettingsWindow(self)
        settings_options_win.focus_force()
        self.withdraw()

    def save_preferences(self) -> bool:
        """
        Stores the desired settings dict as a yaml file at `settings_path`
        :return: success of operation
        """
        with open(settings_path, 'w') as f:
            self.config.write(f)
            return True
