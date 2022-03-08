import tkinter as tk
from PIL import Image, ImageTk
from player_color import ChoosePlayerColor
from board_size import TempWindow
from board_align import AlignmentWindow


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings Window")
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
        self.label1 = tk.Label(self, text='Settings', fg='white', font=("Arial", 55, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)

        # board size
        self.size_image = Image.open('dimension.png')
        self.size_image = self.size_image.resize((220, 165))
        self.size_image = ImageTk.PhotoImage(self.size_image)
        self.size_button = tk.Button(self, width=400, height=250, text="Board Size", image=self.size_image,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17), command=self.board_size)
        self.size_button.grid(row=1, column=0, padx=50, sticky='s')

        # color button
        self.color_image = Image.open('color.png')
        self.color_image = self.color_image.resize((175, 175))
        self.color_image = ImageTk.PhotoImage(self.color_image)
        self.color_button = tk.Button(self, width=400, height=250, text="Color",
                                      image=self.color_image, bg='#41ab24',
                                      activebackground='green', compound=tk.TOP, fg='white',
                                      font=("Arial", 17), command=self.open_colors)
        self.color_button.grid(row=1, column=1, padx=50, sticky='s')

        # board alignment
        self.board_image = Image.open('startboard.jpg')
        self.board_image = self.board_image.resize((170, 170))
        self.board_image = ImageTk.PhotoImage(self.board_image)
        self.board_button = tk.Button(self, width=400, height=250, text="Alignment", image=self.board_image,
                                      bg='#41ab24', activebackground='green', compound=tk.TOP, fg='white',
                                      font=("Arial", 17), command=self.board_alignment)
        self.board_button.grid(row=1, column=2, padx=50, sticky='s')

    def open_login(self):
        self.destroy()
        self.master.deiconify()

    def board_size(self):
        board = TempWindow(self)
        board.focus_force()
        self.withdraw()

    def open_colors(self):
        color_win = ChoosePlayerColor(self)
        color_win.focus_force()
        self.withdraw()

    def board_alignment(self):
        board = AlignmentWindow(self)
        board.focus_force()
        self.withdraw()