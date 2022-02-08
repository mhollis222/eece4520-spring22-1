from Player import Player
from Game import Game


def main():
    player1 = Player("steve")
    player2 = Player("jill")
    game = Game(player1, player2)

    game.start()


if __name__ == "__main__":
    main()
