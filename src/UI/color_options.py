import tkinter as tk
from PIL import Image, ImageTk


class ColorOptionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("AI Difficulty I Options")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')

        # color 1
        self.color1 = Image.open('black.png')
        self.color1 = self.color1.resize((150, 150))
        self.color1 = ImageTk.PhotoImage(self.color1)
        self.size_button = tk.Button(self, width=200, height=200, text="Black", image=self.color1,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17))
        self.size_button.grid(row=0, column=0, padx=50, sticky='s')

        # color 2
        self.color2 = Image.open('red.png')
        self.color2 = self.color2.resize((150, 150))
        self.color2 = ImageTk.PhotoImage(self.color2)
        self.size_button = tk.Button(self, width=200, height=200, text="Red", image=self.color2,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17))
        self.size_button.grid(row=0, column=2, padx=50, sticky='s')

        # color 3
        self.color3 = Image.open('yellow.png')
        self.color3 = self.color3.resize((150, 150))
        self.color3 = ImageTk.PhotoImage(self.color3)
        self.size_button = tk.Button(self, width=200, height=200, text="Yellow", image=self.color3,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17))
        self.size_button.grid(row=1, column=1, padx=50, sticky='s')

        # color 4
        self.color4 = Image.open('white.png')
        self.color4 = self.color4.resize((150, 150))
        self.color4 = ImageTk.PhotoImage(self.color4)
        self.size_button = tk.Button(self, width=200, height=200, text="White", image=self.color4,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17))
        self.size_button.grid(row=0, column=1, padx=50, sticky='s')

        # color 5
        self.color5 = Image.open('blue.png')
        self.color5 = self.color5.resize((150, 150))
        self.color5 = ImageTk.PhotoImage(self.color5)
        self.size_button = tk.Button(self, width=200, height=200, text="Blue", image=self.color5,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17))
        self.size_button.grid(row=1, column=0, padx=50, sticky='s')

        # color 6
        self.size_image = Image.open('green.png')
        self.size_image = self.size_image.resize((150, 150))
        self.size_image = ImageTk.PhotoImage(self.size_image)
        self.size_button = tk.Button(self, width=200, height=200, text="Green", image=self.size_image,
                                     compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                     font=("Arial", 17))
        self.size_button.grid(row=1, column=2, padx=50, sticky='s')

    def open_login(self):
        self.destroy()
        self.master.deiconify()  # show the root window