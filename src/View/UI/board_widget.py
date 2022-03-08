import tkinter as tk


class BoardWidget(tk.Frame):
    def __init__(self, parent, board_size=3):
        super().__init__(parent)

        for i in range(board_size):
            self.rowconfigure(i, minsize=75)
            self.columnconfigure(i, minsize=75)

        for i in range(board_size):
            for j in range(board_size):
                button = tk.Button(self, text=f'({i},{j})',
                                   command=lambda arg=(i, j): self.button_clicked(arg))
                button.grid(row=i, column=j, sticky='nsew')

    def button_clicked(self, arg):
        print(f'clicked {arg}')
