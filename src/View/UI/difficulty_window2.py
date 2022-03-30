import tkinter as tk
from PIL import Image, ImageTk
import configparser

from settings_window import SettingsWindow

from pathlib import Path
path_parent = Path(__file__).resolve().parents[3]
settings_path = path_parent.joinpath('settings.ini').as_posix()
preference_path = path_parent.joinpath('preferences.ini').as_posix()


class AIDifficultyIIWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AI Difficulty II Options")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)
        self.configure(bg='green')
        self.preference_config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.preference_config.read(preference_path)

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_home_window)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        #title
        self.guest_title = tk.Label(self, text='Select a Level of Difficulty',
                                    font=("Arial", 35, "bold"), bg='green', fg='white')
        self.guest_title.grid(row=1, column=0, columnspan=3, sticky=tk.N)
        # easy button
        self.easy_image = Image.open('../View/UI/images/easy.png')
        self.easy_image = self.easy_image.resize((175, 175))
        self.easy_image = ImageTk.PhotoImage(self.easy_image)
        self.easy_button = tk.Button(self, width=400, height=250, text="Easy", image=self.easy_image,
                                       compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                       font=("Arial", 17), command=self.easy_play)
        self.easy_button.grid(row=1, column=0, padx=50, sticky='s')
        # medium button
        self.medium_image = Image.open('../View/UI/images/medium.png')
        self.medium_image = self.medium_image.resize((175, 175))
        self.medium_image = ImageTk.PhotoImage(self.medium_image)
        self.medium_button = tk.Button(self, width=400, height=250, text="Medium",
                                         image=self.medium_image, bg='#41ab24',
                                         activebackground='green', compound=tk.TOP, fg='white', font=("Arial", 17),
                                       command=self.medium_play)
        self.medium_button.grid(row=1, column=1, padx=50, sticky='s')
        # hard button
        self.hard_image = Image.open('../View/UI/images/hard.png')
        self.hard_image = self.hard_image.resize((175, 175))
        self.hard_image = ImageTk.PhotoImage(self.hard_image)
        self.hard_button = tk.Button(self,  width=400, height=250, text="Hard", image=self.hard_image,
                                          bg='#41ab24', activebackground='green', compound=tk.TOP, fg='white',
                                          font=("Arial", 17),  command=self.hard_play)
        self.hard_button.grid(row=1, column=2, padx=50, sticky='s')

    def open_home_window(self):
        """Naviagtes to the home page"""
        self.destroy()
        self.master.deiconify()  # show the root window

    def easy_play(self):
        self.config['Model']['ai_difficulty'] = str(1)
        self.save_preferences()
        self.open_settings()

    def medium_play(self):
        self.config['Model']['ai_difficulty'] = str(3)
        self.save_preferences()
        self.open_settings()

    def hard_play(self):
        self.config['Model']['ai_difficulty'] = str(5)
        self.save_preferences()
        self.open_settings()

    def open_settings(self):
        """Naviagtes to the settings preference window"""
        settings_options_win = SettingsWindow(self)
        settings_options_win.focus_force()
        self.withdraw()

    def save_preferences(self) -> bool:
        """
        Stores the desired settings dict as a yaml file at `settings_path`
        :param settings: the settings to be stored.
        :return: success of operation
        """
        with open(settings_path, 'w') as f:
            self.config.write(f)