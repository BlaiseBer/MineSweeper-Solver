from grid.Found import Found
from grid.Values import Values
from utilities.Ordlist import Ordlist
from utilities.Zone import Zone
from utilities.Play import Play
from Window.Fenetre import Fenetre

class Game:

    def __init__(self, n, N, type):
        self.list = {}
        self.links = {}
        self.N = N
        self.n = n
        self.values = Values(n, N, type)
        self.found = Found(self.values)
        self.pile = []

        #on initialise la première zone
        temp = Play('', 0,0)
        a = Zone(self.found, temp, True)
        self.list[a.number] = a
        self.links[a.number] = []

        #On ajoute le premier coup à la pile
        self.pile.append(Play("Del", N//2,N//2))

        self.fen = Fenetre(self.n,  self.N, self)
        self.fen.title("MineSweeper_Solver")

    def start(self):
        self.fen.mainloop()

    def step(self):

        # on prend le premier coup qui n'a pas déjà été joué
        play = self.pile.pop(0)
        while self.found.grid.grid[play.pos[0]][play.pos[1]] != -2:
            if len(self.pile) <=0 :
                return
            play = self.pile.pop(0)

        print("--------------------------------------------------------")

        #je print le play
        print(play.pos, play.nom)

        # JE PRINT LA GRID
        self.found.grid.printGrid()

        # JE PRINT LA PILE
        for p in self.pile:
            print(p.toString() + ", ")
        print("\n")

        # JE PRINT LES LINKS
        for key in self.list.keys():
            print(str(key) + " : " + self.list[key].toString() + "\n")

        l = []  # zones impactées
        for p in self.values.grid.getCircle(play.pos[0], play.pos[1]):
            # on cherche la première zone qui contient la case ou le drapeau a été joué.
            zone = None
            for key in self.list.keys():
                zone = self.list[key]
                if zone.cells.isInside(play.pos) and not(key in l):
                    l.append(zone.number)
                    break

            # ensuite seule les zones connectées à cette zone peuvent contenir la case jouée
            if zone != None:
                for num in self.links[zone.number]:
                    if self.list[num].cells.isInside(play.pos) and not(num in l):
                        l.append(num)

        for i in range(len(l) - 1, -1, -1):  # on modifie les zones impactées directement
            zone = self.list[l[i]]
            if zone.cells.isInside(play.pos):
                zone.cells.remove(play.pos)
                if play.nom == "Flag":
                    zone.bombs -= 1
                if self.nettoyer(zone):
                    l.remove(l[i])

        if play.nom == "Flag":
            # On met un drapeau à la bonne position
            self.found.grid.update(play.pos[0], play.pos[1], -1)

        elif play.nom == "Del":
            self.found.grid.update(play.pos[0], play.pos[1], self.values.grid.get(play.pos[0], play.pos[1]))

            if self.values.grid.grid[play.pos[0]][play.pos[1]] == -1:
                print("T'as cliqué sur une bombe !")
                self.pile = []
                return

            # Puis, on crée une nouvelle zone
            tempZone = Zone(self.found, play)
            self.list[tempZone.number] = tempZone
            # on ajoute ses arêtes
            self.links[tempZone.number] = []
            for e in tempZone.cells.list:  #Optimisable ???
                for num in self.list.keys():
                    zone = self.list[num]
                    if zone.cells.isInside(e) and (zone != tempZone):
                        if not (tempZone.number in self.links[zone.number]):
                            self.links[zone.number].append(tempZone.number)
                            self.links[tempZone.number].append(zone.number)

            if self.nettoyer(tempZone):
                return

            #il faut ensuite vérifier l'intersection avec chaque zone qui recouvre la nouvelle zone
            for num in self.links[tempZone.number]:
                zone = self.list[num]
                L1_exclude_L2, L1_inter_L2, L2_exclude_L1 = tempZone.intersect(zone)

                #cas ou l'un est inclus dans l'autre (facile)
                if len(L1_exclude_L2) == 0:
                    zone.cells = Ordlist(self.N, liste=L2_exclude_L1)
                    zone.bombs -= tempZone.bombs
                    self.nettoyer(zone)
                elif len(L2_exclude_L1) == 0:
                    tempZone.cells = Ordlist(self.N, liste=L1_exclude_L2)
                    tempZone.bombs -= zone.bombs
                    self.nettoyer(tempZone)

                # Sinon, il y a certain(s) cas particulier où l'on peut quand même simplifier
                elif tempZone.bombs - len(L1_exclude_L2) == zone.bombs:
                    for e in L2_exclude_L1:
                        self.pile.append(Play('Del', e[0], e[1]))
                    for e in L1_exclude_L2:
                        self.pile.append(Play('Flag', e[0], e[1]))
                elif zone.bombs - len(L2_exclude_L1) == tempZone.bombs:
                    for e in L1_exclude_L2:
                        self.pile.append(Play('Del', e[0], e[1]))
                    for e in L2_exclude_L1:
                        self.pile.append(Play('Flag', e[0], e[1]))

    def nettoyer(self, zone):
        if zone.bombs <=0 and len(zone.cells.list) <= 1:
            for e in zone.cells.list:
                self.pile.append(Play("Del", e[0], e[1]))
            self.delZone(zone.number)
            return True
        elif zone.bombs <= 0:
            for e in zone.cells.list:
                self.pile.append(Play("Del", e[0], e[1]))
            return True
        elif len(zone.cells.list) == zone.bombs:
            for e in zone.cells.list:
                self.pile.append(Play('Flag', e[0], e[1]))
            self.delZone(zone.number)
            return True
        return False

    def delZone(self, num):
        if num in self.list.keys():
            self.list.pop(num)
            self.links.pop(num)
            for key in self.links.keys():
                for i in range(len(self.links[key])-1, -1, -1):
                    num2 = self.links[key][i]
                    if num2 == num:
                        del self.links[key][i] #à optimiser avec les listes croissantes