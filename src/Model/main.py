from human_player import HumanPlayer
from game import Game
from Controller.game_controller import GameController


def main():
    player1 = HumanPlayer("Steve")
    player2 = HumanPlayer("Jill")

    game = Game(player1, player2)

    control = GameController(player1, player2)

if __name__ == "__main__":
    main()
