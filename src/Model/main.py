from human_player import HumanPlayer
from game import Game
from View.textual_view import TextualView
from Controller.game_controller import GameController
from View.UI.gui_board import GuiBoard
import tkinter as tk

def main():
    player1 = HumanPlayer("Steve")
    player2 = HumanPlayer("Jill")
    game = Game(player1, player2)
    text = TextualView(game)
    control = GameController(game, text)
    # control.play_game()
    view = GuiBoard(game)
    view.display_board(control.model.get_valid_moves(player1))
    view.display_current_player(player1)
    view.display_score()
    # view.display_end_of_game()
    # view.display_winner(3)
    view.root.mainloop()


if __name__ == "__main__":
    main()
