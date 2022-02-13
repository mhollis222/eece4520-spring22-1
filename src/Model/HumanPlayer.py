from AbstractPlayer import AbstractPlayer
from Model.Move import Move


class HumanPlayer(AbstractPlayer):

    def getMove(self) -> Move:
        valid = False
        while not valid:
            x = input(str(self) + ' pick the desired x coordinate, or enter \'pass\' to skip:\n')
            if x.lower() == 'pass':
                return Move(0, 0, True)
            valid = int(x) > 0
        valid = False
        while not valid:
            y = input(str(self) + ' pick the desired y coordinate:\n')
            valid = int(y) > 0

        return Move(int(x), int(y))
