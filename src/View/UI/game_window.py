import tkinter as tk
from board_widget import BoardWidget
from player_status_widget import PlayerStatusWidget
from player_scores import PlayerScores

class GameWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Game')

        # gameboard
        self.board = BoardWidget(self)
        self.board.pack()

        # current player
        self.current = PlayerStatusWidget(self)
        self.current.pack()

        # current scores
        self.scores = PlayerScores(self)
        self.scores.pack()

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Place window in the center of the screen
        self.master.eval(f'tk::PlaceWindow {str(self)} center')

    def close_window(self):
        self.destroy()
        self.master.deiconify()  # show the root window