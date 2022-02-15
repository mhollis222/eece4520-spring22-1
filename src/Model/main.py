from HumanPlayer import HumanPlayer
from Game import Game
from View.text_view import TextView
from Controller.game_controller import GameController


def main():
    player1 = HumanPlayer("steve")
    player2 = HumanPlayer("jill")
    game = Game(player1, player2)
    text = TextView(game)
    control = GameController(game, text)

    control.play_game()


if __name__ == "__main__":
    main()
