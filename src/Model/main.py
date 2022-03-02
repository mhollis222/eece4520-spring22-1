from human_player import HumanPlayer
from game import Game
from View.textual_view import TextualView
from Controller.game_controller import GameController
from View.UI.gui_board import gui_board
import tkinter as tk

def main():
    player1 = HumanPlayer("Steve")
    player2 = HumanPlayer("Jill")
    game = Game(player1, player2)
    text = TextualView(game)
    control = GameController(game, text)
    # control.play_game()
    view = gui_board(game)
    view.display_board(control.model.get_valid_moves(player1))
    view.display_current_player(player1)
    view.root.mainloop()


if __name__ == "__main__":
    main()
