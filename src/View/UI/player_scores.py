import tkinter as tk

class PlayerScores(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # self.rowconfigure(2, minsize=75)
        # self.columnconfigure(2, minsize=75)

        self.current = tk.Label(self, text="Jill's Score: 10")
        self.current.grid(row=8, column=5, sticky=tk.NE, padx=5, pady=5)

        self.current = tk.Label(self, text="Steve's Score: 20")
        self.current.grid(row=8, column=6, sticky=tk.E, padx=5, pady=5)