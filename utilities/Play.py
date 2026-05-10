class Play:
    nom = ""
    pos = (0, 0)

    def __init__(self, nom, x : int, y : int):
        self.nom = nom
        self.pos = (x,y)

    def toString(self):
        return self.nom + '( ' + str(self.pos[0]) + ", " + str(self.pos[1]) + ' )'