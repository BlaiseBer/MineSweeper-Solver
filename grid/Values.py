import grid.Grid
import random as rd
class Values:

    def __init__(self, n, N, type):
        self.grid = grid.Grid.Grid(n, N, 0)

        #On dispose les bombes
        L = []
        for i in range(self.grid.N):
            for j in range(self.grid.N):
                L.append((i, j))

        if type == "GoodStart":
            L.remove((N//2,N//2))
            for e in self.grid.getCircle(N//2, N//2):
                L.remove(e)
        while n > 0:
            n -= 1
            e = rd.randint(0, len(L) - 1)
            (x, y) = L[e]
            L.pop(e)
            self.grid.update(x,y,-1)

        # On met les bons nombres à chaques endroits
        for i in range(self.grid.N):
            for j in range(self.grid.N):
                if self.isBomb(i, j):
                    for e in self.grid.getCircle(i, j):
                        if self.grid.get(e[0], e[1]) != -1:
                            self.grid.grid[e[0]][e[1]] += 1

    def isBomb(self, i, j):
        return -1 == self.grid.get(i, j)