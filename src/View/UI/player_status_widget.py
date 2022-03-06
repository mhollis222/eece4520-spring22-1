import tkinter as tk
import current_player_status

class PlayerStatusWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure(5, minsize=75)
        self.columnconfigure(2, minsize=75)

        self.current = tk.Label(self, text='Current Player: Jill' )
        self.current.grid(row=10, column=3, sticky=tk.W, padx=5, pady=5)