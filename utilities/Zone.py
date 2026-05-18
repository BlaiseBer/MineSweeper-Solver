class Zone:
    NUMBER = 0
    N = 0

    def __init__(self, found, play, init : bool = False):
        if init:
            self.cells = []
            self.N = found.grid.N
            self.number = 0
            Zone.NUMBER = 1
            self.bombs = found.grid.n
            for i in range(found.grid.N):
                for j in range(found.grid.N):
                    self.cells.append((i, j))
        else:
            self.cells = []
            self.number = Zone.NUMBER
            Zone.NUMBER += 1
            self.bombs = found.grid.get(play.pos[0], play.pos[1])

            #les zones déjà révélées ne doivent pas êtres ajoutés à la zone
            for e in found.grid.getCircle(play.pos[0], play.pos[1]):
                if found.grid.get(e[0], e[1]) == -2:
                    self.cells.append(e)
                if found.grid.get(e[0], e[1]) == -1:
                    self.bombs -=1

    def intersect(self, other):       #à optimiser avec les listes croissantes
        L1 = self.cells
        L2 = other.cells
        L1_exclude_L2 = L1.copy()
        L1_inter_L2 = []
        L2_exclude_L1 = []

        for e in L2 :
            if e in L1:
                L1_inter_L2.append(e)
                L1_exclude_L2.remove(e)
            else:
                L2_exclude_L1.append(e)
        return (L1_exclude_L2, L1_inter_L2, L2_exclude_L1)

    def toString(self):
        return str(self.cells) + ' ' + str(self.bombs)