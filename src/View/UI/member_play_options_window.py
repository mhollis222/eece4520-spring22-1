import tkinter as tk
from PIL import Image, ImageTk
from difficulty_window2 import AIDifficultyIIWindow
from difficulty_window2 import AIDifficultyIIWindow
from settings_window import SettingsWindow


class MemberPlayOptionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Member Play Options")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.configure(bg='green')


        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')
        #title
        self.guest_title = tk.Label(self, text='Who do you want to play?',
                                    font=("Arial", 35, "bold"), bg='green', fg='white')
        self.guest_title.grid(row=1, column=1, columnspan=2, sticky=tk.N)
        # play person button
        self.person_image = Image.open('../View/UI/images/user.png')
        self.person_image = self.person_image.resize((175, 175))
        self.person_image = ImageTk.PhotoImage(self.person_image)
        self.person_button = tk.Button(self, width=400, height=250, text="Local Player", image=self.person_image,
                                       compound=tk.TOP, activebackground='green', bg='#41ab24', fg='white',
                                       font=("Arial", 17), command=self.open_settings_options)
        self.person_button.grid(row=1, column=0, padx=50, sticky='s')
        # play computer button
        self.computer_image = Image.open('../View/UI/images/computer.png')
        self.computer_image = self.computer_image.resize((175, 175))
        self.computer_image = ImageTk.PhotoImage(self.computer_image)
        self.computer_button = tk.Button(self, width=400, height=250, text="Computer",
                                         image=self.computer_image, bg='#41ab24',
                                         activebackground='green', compound=tk.TOP, fg='white', font=("Arial", 17),
                                         command=self.open_ai)
        self.computer_button.grid(row=1, column=1, padx=50, sticky='s')
        # matchmake button
        self.matchmake_image = Image.open('../View/UI/images/boxing-gloves.png')
        self.matchmake_image = self.matchmake_image.resize((175, 175))
        self.matchmake_image = ImageTk.PhotoImage(self.matchmake_image)
        self.matchmake_button = tk.Button(self,  width=400, height=250, text="Matchmake", image=self.matchmake_image,
                                          bg='#41ab24', activebackground='green', compound=tk.TOP, fg='white',
                                          font=("Arial", 17))
        self.matchmake_button.grid(row=1, column=2, padx=50, sticky='s')
        # challenge player online button
        self.online_image = Image.open('../View/UI/images/online.png')
        self.online_image = self.online_image.resize((175, 175))
        self.online_image = ImageTk.PhotoImage(self.online_image)
        self.online_button = tk.Button(self,  width=400, height=250, text="Online Player", image=self.online_image,
                                       bg='#41ab24', activebackground='green', compound=tk.TOP, fg='white',
                                       font=("Arial", 17))
        self.online_button.grid(row=1, column=3, padx=50, sticky='s')

    def open_login(self):
        """Naviagtes to the login page"""
        self.destroy()
        self.master.deiconify()  # show the root window

    def open_ai(self):
        """Naviagtes to the AI settings window"""
        ai_win = AIDifficultyIIWindow(self)
        ai_win.focus_force()
        self.withdraw()

    def open_settings_options(self):
        """Naviagtes to the game settings page"""
        settings_options_win = SettingsWindow(self)
        settings_options_win.focus_force()
        self.withdraw()