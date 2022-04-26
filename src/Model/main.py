from human_player import HumanPlayer
from ai_player import AIPlayer
from game import Game
from move import Move
from Controller.game_controller import GameController
from View.UI.gui_board import GuiBoard
from View.textual_view import TextualView
from Model.game_decorator_ai import GameDecoratorAI


def main():
    player1 = HumanPlayer("Steve")
    player2 = AIPlayer("Jill", 3)

    game = Game(player1, player2)
    dec = GameDecoratorAI(game)
    game.start()
    player2.add_simulator(dec)
    player2.add_opp(player1)
    moves = game.get_valid_moves(player2)
    view = TextualView(game, 'red', 'blue')
    # print(dec.valid_moves_avail([Move(5,4)], player2))
    # print(game.get_active_player())
    #print(player2.make_move(0,0))
    view.display_board(moves)
    # #print(game.board)

    control = GameController(player1, player2, True)

if __name__ == "__main__":
    main()
