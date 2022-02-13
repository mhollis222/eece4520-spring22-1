from AbstractPlayer import AbstractPlayer
from Model.Move import Move


class HumanPlayer(AbstractPlayer):

    def getMove(self) -> Move:
        valid = False
        while not valid:
            x = input(str(self) + ' pick the desired x coordinate, or enter \'pass\' to skip:\n')
            valid = True
            if x.lower() == 'pass':
                print(str(self) + ' skipped their turn!')
                return Move(0, 0, True)
            if int(x) < 0:
                valid = False
                print('Coordinates must be > 0')
        valid = False
        while not valid:
            y = input(str(self) + ' pick the desired y coordinate:\n')
            valid = True
            if int(y) < 0:
                valid = False
                print('Coordinates must be > 0')

        return Move(int(x), int(y))
