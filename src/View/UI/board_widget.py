import tkinter as tk

class BoardWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(width=5000, height=5000)
        self.board_frame = tk.Frame(self, width=2200, height=2200)
        # self.board_frame.grid(row=1, column=0)

        for i in range(8):
            self.board_frame.rowconfigure(i, minsize=75)
            self.board_frame.columnconfigure(i, minsize=75)

        for i in range(8):
            for j in range(8):
                # if # empty

                # elif # player 1

                # else # player 2
                # self.black_dot = Image.open('black-circle.png')
                # self.black_dot = self.black_dot.resize((175, 175))
                # self.black_dot = ImageTk.PhotoImage(self.black_dot)
                # self.button = tk.Button(self, bg='green', image=self.black_dot, text=f'({i},{j})',
                #                    command=lambda arg=(i, j): self.button_clicked(arg))
                self.board_frame.button = tk.Button(self, bg='black', text=f'({i},{j})',
                                                    command=lambda arg=(i, j): self.button_clicked(arg))
                self.board_frame.button.grid(row=i, column=j, sticky='nsew')

    def button_clicked(self, arg):
        print(f'clicked {arg}')