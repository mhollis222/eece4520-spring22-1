from human_player import HumanPlayer
from game import Game
from View.UI.gui_view import GUIView
from Controller.game_controller import GameController


def main():
    player1 = HumanPlayer("Steve")
    player2 = HumanPlayer("Jill")

#     game = Game(player1, player2)
#     text = GUIView(game)

    control = GameController(player1, player2)
    control.play_game()


if __name__ == "__main__":
    main()
