from grid.Grid import Grid


class Found:
    def __init__(self, values):
        self.grid = Grid(values.grid.n, values.grid.N, -2)