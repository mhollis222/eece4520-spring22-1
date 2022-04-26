import tkinter as tk
from board_widget import BoardWidget


class GameWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Game')

        self.board = BoardWidget(self)
        self.board.pack()

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Place window in the center of the screen
        self.master.eval(f'tk::PlaceWindow {str(self)} center')

    def close_window(self):
        """Navigates to the previous window"""
        self.destroy()
        self.master.deiconify()  # show the root window


