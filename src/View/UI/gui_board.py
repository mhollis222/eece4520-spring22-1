from View.abstract_view import AbstractView
from Model.game import Game
from Model.abstract_player import AbstractPlayer
import tkinter as tk

class gui_board(AbstractView):

    def __init__(self, model: Game):
        super().__init__(model)
        self.model = model

    root = tk.Tk()
    root.mainloop()