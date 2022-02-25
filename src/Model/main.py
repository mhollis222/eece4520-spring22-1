from human_player import HumanPlayer
from game import Game
from View.textual_view import TextualView
from Controller.game_controller import GameController


def main():
    player1 = HumanPlayer("Steve")
    player2 = HumanPlayer("Jill")
    # game = Game(player1, player2)
    # text = TextualView(game)
    control = GameController(player1, player2)
    control.play_game()


if __name__ == "__main__":
    main()
