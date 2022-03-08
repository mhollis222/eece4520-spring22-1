import tkinter as tk
from PIL import Image, ImageTk


class AIDifficultyIWindow(tk.Toplevel):
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
        #title
        self.guest_title = tk.Label(self, text='Select a Level of Difficulty',
                                    font=("Arial", 35, "bold"), bg='green', fg='white')
        self.guest_title.grid(row=1, column=0, columnspan=3, sticky=tk.N)
        # easy button
        self.easy_image = Image.open('easy.png')
        self.easy_image = self.easy_image.resize((175, 175))
        self.easy_image = ImageTk.PhotoImage(self.easy_image)
        self.easy_button = tk.Button(self, width=400, height=250, text="Easy", image=self.easy_image,
                                       compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                       font=("Arial", 17))
        self.easy_button.grid(row=1, column=0, padx=50, sticky='s')
        # medium button
        self.medium_image = Image.open('medium.png')
        self.medium_image = self.medium_image.resize((175, 175))
        self.medium_image = ImageTk.PhotoImage(self.medium_image)
        self.medium_button = tk.Button(self, width=400, height=250, text="Medium",
                                         image=self.medium_image, bg='#41ab24',
                                         activebackground='green', compound=tk.TOP, fg='white', font=("Arial", 17))
        self.medium_button.grid(row=1, column=1, padx=50, sticky='s')
        # hard button
        self.hard_image = Image.open('hard.png')
        self.hard_image = self.hard_image.resize((175, 175))
        self.hard_image = ImageTk.PhotoImage(self.hard_image)
        self.hard_button = tk.Button(self,  width=400, height=250, text="Hard", image=self.hard_image,
                                          bg='#41ab24', activebackground='green', compound=tk.TOP, fg='white',
                                          font=("Arial", 17))
        self.hard_button.grid(row=1, column=2, padx=50, sticky='s')

    def open_login(self):
        self.destroy()
        self.master.deiconify()