import tkinter as tk


class MatchmakingErrorWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Matchmaking Error Page')
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.columnconfigure([0, 1], minsize=50, weight=1)
        self.configure(bg='green')

        # title
        self.title = tk.Label(self,
                              text='Unfortunately, we were unable to connect you to someone. Please try again later.',
                              fg='white', font=("Arial", 55, "bold"), bg='green')
        self.title.grid(row=1, columnspan=2, sticky=tk.S)
        # cancel button
        self.cancel_button = tk.Button(self, text='OK', width=30, height=2, font=("Arial", 15),
                                       command=self.cancel)
        self.cancel_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def cancel(self):
        self.withdraw()
