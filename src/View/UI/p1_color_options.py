import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import configparser


from pathlib import Path
path_parent = Path(__file__).resolve().parents[3]
settings_path = path_parent.joinpath('settings.ini').as_posix()


class Player1ColorOptionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # special options to save comments on writes (i hope)
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)
        self.title("Player One Color Options")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')
        self.current = ""

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        # title
        self.label1 = tk.Label(self, text='Player 1 Color', fg='white', font=("Arial", 30, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)
        # color 1
        self.color1 = Image.open(apply_path('images/black.png'))
        self.color1 = self.color1.resize((150, 150))
        self.color1 = ImageTk.PhotoImage(self.color1)
        self.size_button = tk.Button(self, width=200, height=200, text="Black", image=self.color1,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.save_black)
        self.size_button.grid(row=1, column=0, padx=50, sticky='s')

        # color 2
        self.color2 = Image.open(apply_path('images/red.png'))
        self.color2 = self.color2.resize((150, 150))
        self.color2 = ImageTk.PhotoImage(self.color2)
        self.size_button = tk.Button(self, width=200, height=200, text="Red", image=self.color2,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.save_red)
        self.size_button.grid(row=1, column=2, padx=50, sticky='s')

        # color 3
        self.color3 = Image.open(apply_path('images/pink.png'))
        self.color3 = self.color3.resize((150, 150))
        self.color3 = ImageTk.PhotoImage(self.color3)
        self.size_button = tk.Button(self, width=200, height=200, text="Magenta", image=self.color3,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.save_magenta)
        self.size_button.grid(row=1, column=1, padx=50, sticky='s')

        # color 4
        self.color4 = Image.open(apply_path('images/white.png'))
        self.color4 = self.color4.resize((150, 150))
        self.color4 = ImageTk.PhotoImage(self.color4)
        self.size_button = tk.Button(self, width=200, height=200, text="White", image=self.color4,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.save_white)
        self.size_button.grid(row=2, column=1, padx=50, sticky='s')

        # color 5
        self.color5 = Image.open(apply_path('images/blue.png'))
        self.color5 = self.color5.resize((150, 150))
        self.color5 = ImageTk.PhotoImage(self.color5)
        self.size_button = tk.Button(self, width=200, height=200, text="Blue", image=self.color5,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.save_blue)
        self.size_button.grid(row=2, column=0, padx=50, sticky='s')

        # color 6
        self.size_image = Image.open(apply_path('images/cyan.png'))
        self.size_image = self.size_image.resize((150, 150))
        self.size_image = ImageTk.PhotoImage(self.size_image)
        self.size_button = tk.Button(self, width=200, height=200, text="Cyan", image=self.size_image,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.save_cyan)
        self.size_button.grid(row=2, column=2, padx=50, sticky='s')

    def open_login(self):
        """Naviagtes to the login page"""
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

    def save_black(self):
        """Saves player one's color to black"""
        self.config['View']['p1_color'] = 'black'
        self.save_preferences()
        messagebox.showerror("", "Player One's color successfully updated")

    def save_red(self):
        """Saves player one's color to red"""
        self.config['View']['p1_color'] = 'red'
        self.save_preferences()
        messagebox.showerror("", "Player One's color successfully updated")

    def save_magenta(self):
        """Saves player one's color to magenta"""
        self.config['View']['p1_color'] = 'magenta'
        self.save_preferences()
        messagebox.showerror("", "Player One's color successfully updated")

    def save_blue(self):
        """Saves player one's color to blue"""
        self.config['View']['p1_color'] = 'blue'
        self.save_preferences()
        messagebox.showerror("", "Player One's color successfully updated")

    def save_cyan(self):
        """Saves player one's color to cyan"""
        self.config['View']['p1_color'] = 'cyan'
        self.save_preferences()
        messagebox.showerror("", "Player One's color successfully updated")

    def save_white(self):
        """Saves player one's color to white"""
        self.config['View']['p1_color'] = 'white'
        self.save_preferences()
        messagebox.showerror("", "Player One's color successfully updated")