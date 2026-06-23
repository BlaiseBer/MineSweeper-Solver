from utilities.Ordlist import Ordlist

class Zone:
    NUMBER = 0
    N = 0

    def __init__(self, found, play, init : bool = False):
        if init:
            self.N = found.grid.N
            self.cells = Ordlist(self.N)
            self.number = 0
            Zone.NUMBER = 1
            self.bombs = found.grid.n
            for i in range(self.N):
                for j in range(self.N):
                    self.cells.add((i, j))
        else:
            self.N = found.grid.N
            self.cells = Ordlist(self.N)
            self.number = Zone.NUMBER
            Zone.NUMBER += 1
            self.bombs = found.grid.get(play.pos[0], play.pos[1])

            #les zones déjà révélées ne doivent pas êtres ajoutés à la zone
            for e in found.grid.getCircle(play.pos[0], play.pos[1]):
                if found.grid.get(e[0], e[1]) == -2:
                    self.cells.add(e)
                if found.grid.get(e[0], e[1]) == -1:
                    self.bombs -=1

    def intersect(self, other):
        return self.cells.intersect(other.cells)

    def toString(self):
        return self.cells.toString() + ' ' + str(self.bombs)