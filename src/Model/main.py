from HumanPlayer import HumanPlayer
from Game import Game


def main():
    player1 = HumanPlayer("steve")
    player2 = HumanPlayer("jill")
    game = Game(player1, player2)

    game.start()


if __name__ == "__main__":
    main()
