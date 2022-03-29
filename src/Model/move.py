class Move:
    def __init__(self, x: int, y: int, skip:bool = False):
        self.x = x
        self.y = y
        self.skip = skip

    def get_coords(self) -> (int, int):
        """
        :return: the x and y coordinates representative of the location of the desired cell (int, int)
        """
        return self.x, self.y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
