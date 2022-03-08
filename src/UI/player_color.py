import tkinter as tk
from PIL import Image, ImageTk
from p1_color_options import Player1ColorOptionsWindow
from p2_color_options import Player2ColorOptionsWindow


class ChoosePlayerColor(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Guest Play Options")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.columnconfigure([0, 1], minsize=50, weight=1)
        self.configure(bg='green')

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        # title
        self.guest_title = tk.Label(self, text='Choose your Colors',
                                    font=("Arial", 35, "bold"), bg='green', fg='white')
        self.guest_title.grid(row=1, column=0, columnspan=2, sticky=tk.N)

        # play person button
        self.person_image = Image.open('user.png')
        self.person_image = self.person_image.resize((175, 175))
        self.person_image = ImageTk.PhotoImage(self.person_image)
        self.person_button = tk.Button(self, width=400, height=230, text="Player 1", image=self.person_image,
                                       compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                       font=("Arial", 17), command=self.player_1)
        self.person_button.grid(row=1, column=0, padx=50, sticky='s')

        # play computer button
        self.computer_image = Image.open('user.png')
        self.computer_image = self.computer_image.resize((175, 175))
        self.computer_image = ImageTk.PhotoImage(self.computer_image)
        self.computer_button = tk.Button(self, width=400, height=230, text="Player 2",
                                         image=self.computer_image, bg='#41ab24',
                                         activebackground='green', compound=tk.TOP, fg='white',
                                         font=("Arial", 17), command=self.player_2)
        self.computer_button.grid(row=1, column=1, padx=50, sticky='s')

    def player_1(self):
        player1 = Player1ColorOptionsWindow(self)
        player1.focus_force()
        self.withdraw()

    def player_2(self):
        player2 = Player2ColorOptionsWindow(self)
        player2.focus_force()
        self.withdraw()

    def open_login(self):
        self.destroy()
        self.master.deiconify()  # show the root window
