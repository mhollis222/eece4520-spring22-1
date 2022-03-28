from Model.abstract_player import AbstractPlayer
from Model.game import Game

class AIPLayer(AbstractPlayer):
    def __init__(self, model: Game):


    # call recursively with a list of previous moves?
    def make_move(self, row, column):
        # initialize mock game with current state

        # get the current possible moves

        # up until depth `ai_difficulty`
            # for each possible move
                # play out current moves + new move and get utility value

        # when depth has been reached, reverse up the stack, alternating from min -> max
        # pick the move with the highest utility function for the agent and return


