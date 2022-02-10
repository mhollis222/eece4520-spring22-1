class Move:
    def __init__(self, x: int, y: int, skip:bool = False):
        self.x = x
        self.y = y
        self.skip = skip

    def getCoords(self) -> (int, int):
        return self.x, self.y
