import tkinter as tk
from member_play_options_window import MemberPlayOptionsWindow


class HomeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title('Home Page')
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.configure(bg='green')

        # Welcome header
        self.frame1 = tk.Frame(self, bg='black', width=2000, height=70)
        self.frame1.grid(row=0, column=0, columnspan=5, padx=0, sticky='nw')
        # settings button
        self.settings_button = tk.Button(self, text='Settings', width=10, height=2, font=("Arial", 12),
                                         activebackground='black', bg='black', fg='white', relief='flat',
                                         command=self.open_settings, pady=10)
        self.settings_button.grid(row=0, column=0, padx=0, sticky='nw')
        # logout button
        self.back_button = tk.Button(self, text='Log Out', width=10, height=2, font=("Arial", 12),
                                     activebackground='black', bg='black', fg='white', relief='flat',
                                     command=self.close_window, pady=10)
        self.back_button.grid(row=0, column=3, padx=0, sticky='ne')
        # title
        self.frame1.welcome_label = tk.Label(self, text='Welcome, User!', fg='white',
                                             font=("Arial", 20, "bold"), bg='black', pady=15)
        self.frame1.welcome_label.grid(row=0, column=0, columnspan=4, sticky='n')
        # Leaderboard
        self.frame2 = tk.Frame(self, width=550, height=2000, bg='#066b28')
        self.frame2.grid(row=1, column=0, rowspan=6, columnspan=2, sticky='w')
        self.frame2.leaderboard_label = tk.Label(self, text='Leaderboard', fg='white', font=("Arial", 25, "bold"),
                                          bg='#066b28', padx=125)
        self.frame2.leaderboard_label.grid(row=1, column=0)
        self.frame2.first_player = tk.Label(self, text='1. Bob: 98', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.first_player.grid(row=2, column=0, sticky='n')
        self.frame2.second_player = tk.Label(self, text='2. Casey: 84', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.second_player.grid(row=2, column=0)
        self.frame2.third_player = tk.Label(self, text='3. Will: 82', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.third_player.grid(row=3, column=0, sticky='n')
        self.frame2.fourth_player = tk.Label(self, text='4. Brad: 75', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.fourth_player.grid(row=3, column=0)
        self.frame2.fifth_player = tk.Label(self, text='5. Fred: 70', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.fifth_player.grid(row=4, column=0, sticky='n')
        self.frame2.sixth_player = tk.Label(self, text='6. Suzanne: 70', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.sixth_player.grid(row=4, column=0)
        self.frame2.seventh_player = tk.Label(self, text='7.Daphne: 69', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.seventh_player.grid(row=5, column=0, sticky='n')
        self.frame2.eighth_player = tk.Label(self, text='8. Michael: 53', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.eighth_player.grid(row=5, column=0)
        self.frame2.ninth_player = tk.Label(self, text='9. Velma: 48', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.ninth_player.grid(row=6, column=0, sticky='n')
        self.frame2.tenth_player = tk.Label(self, text='10. Joe: 44', fg='white', font=("Arial", 15),
                                          bg='#066b28')
        self.frame2.tenth_player.grid(row=6, column=0)
        # ELO Rating
        self.frame3 = tk.Frame(self, width=925, height=350, bg='#343434')
        self.frame3.grid(row=1, column=1, rowspan=3, columnspan=3, pady=30, padx=40, sticky='e')
        self.frame3.elo_message = tk.Label(self, text='Your current ELO rating is', fg='white',
                                           font=("Arial", 25, "bold"), bg='#343434')
        self.frame3.elo_message.grid(row=1, column=1, columnspan=3, padx=40, pady=90, sticky='n')
        # ELO Score
        self.frame3.elo_message = tk.Label(self, text='98%', fg='white',
                                           font=("Arial", 25, "bold"), bg='#343434')
        self.frame3.elo_message.grid(row=1, column=1, columnspan=3, sticky='s', pady=30)
        # Wins
        self.frame3.wins = tk.Label(self, text='Wins: 10', fg='white', font=("Arial", 25, "bold"), bg='#343434')
        self.frame3.wins.grid(row=2, column=1, sticky='se')
        # Losses
        self.frame3.losses = tk.Label(self, text='Losses: 1', fg='white', font=("Arial", 25, "bold"), bg='#343434')
        self.frame3.losses.grid(row=2, column=3, sticky='sw')
        # Play Game Button
        self.member_play_button = tk.Button(self, text='Play Game', width=30, height=2, fg='black', font=("Arial", 15),
                                            command=self.open_member_options)
        self.member_play_button.grid(row=4, column=2, pady=0, sticky='s')

    def close_window(self):
        self.destroy()
        self.master.deiconify()  # show the root window

    def open_settings(self):
        print("You hit settings!")

    def open_member_options(self):
        member_options_win = MemberPlayOptionsWindow(self)
        member_options_win.focus_force()
        self.withdraw()
