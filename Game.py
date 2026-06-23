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
        self.pile_coup = []
        self.pile_zone = []

        #on initialise la première zone
        temp = Play('', 0,0)
        a = Zone(self.found, temp, True)
        self.list[a.number] = a
        self.links[a.number] = []

        #On ajoute le premier coup à la pile
        self.pile_coup.append(Play("Del", N // 2, N // 2))

        self.fen = Fenetre(self.n,  self.N, self)
        self.fen.title("MineSweeper_Solver")

    def start(self):
        self.fen.mainloop()

    def step(self):

        # on prend le premier coup qui n'a pas déjà été joué
        play = self.pile_coup.pop(0)
        while self.found.grid.grid[play.pos[0]][play.pos[1]] != -2:
            if len(self.pile_coup) <=0 :
                return
            play = self.pile_coup.pop(0)

        print("--------------------------------------------------------")

        #je print le play
        print(play.pos, play.nom)

        # JE PRINT LA GRID
        self.found.grid.printGrid()

        # JE PRINT LA PILE
        for p in self.pile_coup:
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
                self.pile_coup = []
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
                        self.pile_coup.append(Play('Del', e[0], e[1]))
                    for e in L1_exclude_L2:
                        self.pile_coup.append(Play('Flag', e[0], e[1]))
                elif zone.bombs - len(L2_exclude_L1) == tempZone.bombs:
                    for e in L1_exclude_L2:
                        self.pile_coup.append(Play('Del', e[0], e[1]))
                    for e in L2_exclude_L1:
                        self.pile_coup.append(Play('Flag', e[0], e[1]))

    def jouer_les_coups(self):

        # JE PRINT LA GRID
        self.found.grid.printGrid()

        # JE PRINT LA PILE
        for p in self.pile_coup:
            print(p.toString() + ", ")
        print("\n")

        # JE PRINT LES LINKS
        for key in self.list.keys():
            print(str(key) + " : " + self.list[key].toString() + "\n")


        while len(self.pile_coup) >0:
            # on prend le premier coup qui n'a pas déjà été joué
            play = self.pile_coup.pop(0)
            if self.found.grid.grid[play.pos[0]][play.pos[1]] != -2:
                pass
            else:
                print(play.pos, play.nom)
                l = []  # zones impactées
                # on cherche les zones qui contiennent la case ou le coup a été joué et on les modifie en accord
                for zone in self.list.values():
                    if zone.cells.isInside(play.pos):
                        l.append(zone.number)
                        zone.cells.remove(play.pos)
                        if play.nom == "Flag":
                            zone.bombs -= 1

                if play.nom == "Flag":
                    # On met un drapeau à la bonne position
                    self.found.grid.update(play.pos[0], play.pos[1], -1)

                elif play.nom == "Del":
                    self.found.grid.update(play.pos[0], play.pos[1], self.values.grid.get(play.pos[0], play.pos[1]))

                    if self.values.grid.grid[play.pos[0]][play.pos[1]] == -1:
                        print("T'as cliqué sur une bombe !")
                        self.pile_coup = []
                        return

                    # Puis, on crée une nouvelle zone
                    tempZone = Zone(self.found, play)
                    self.list[tempZone.number] = tempZone
                    # on ajoute ses arêtes
                    self.links[tempZone.number] = []
                    for e in tempZone.cells.list:  # Optimisable ???
                        for num in self.list.keys():
                            zone = self.list[num]
                            if zone.cells.isInside(e) and (zone != tempZone):
                                if not (tempZone.number in self.links[zone.number]):
                                    self.links[zone.number].append(tempZone.number)
                                    self.links[tempZone.number].append(zone.number)
                    l.append(tempZone.number)

                # Ensuite, toutes ces zones ont étés impactés par ce coup, donc elles sont toutes susceptible de créer des nouveaux coups quand elles sont comparées les unes aux autres
                # donc :
                l.sort()
                print(l)
                if len(l)==1:
                    self.pile_zone.append((l[0], l[0]))
                    l = []
                else :
                    for i in range(len(l) - 1):
                        for j in range(i + 1, len(l)):
                            if not (l[i], l[j]) in self.pile_zone:
                                self.pile_zone.append((l[i], l[j]))
                for num1 in l:
                    for num2 in self.links[num1]:
                        e = tuple(sorted((num1, num2)))
                        if not e in self.pile_zone:
                            self.pile_zone.append(e)

        #Quand tous les coups ont été joués, on étudie les nouveaux coups qui peuvent être trouvé à partir de pile_zone
        self.etudier_les_zones()

    def etudier_les_zones(self):
        print(self.pile_zone)
        print("-------------------------------------- Coup suivant")
        while len(self.pile_zone)>0:
            (num1, num2) = self.pile_zone.pop()
            if num1==num2:
                self.nettoyer(self.list[num1])
            else:
                a = True
                if self.nettoyer(self.list[num1]):
                    a = False
                    for i in range(len(self.pile_zone)-1, -1, -1):
                        if self.pile_zone[i][0]==num1 or self.pile_zone[i][1]==num1:
                            self.pile_zone.pop(i)
                if self.nettoyer(self.list[num2]):
                    a=False
                    for i in range(len(self.pile_zone)-1, -1, -1):
                        if self.pile_zone[i][0]==num2 or self.pile_zone[i][1]==num2:
                            self.pile_zone.pop(i)
                if a:
                    zone1 = self.list[num1]
                    zone2 = self.list[num2]
                    L1_exclude_L2, L1_inter_L2, L2_exclude_L1 = zone1.intersect(zone2)

                    # cas ou l'un est inclus dans l'autre (facile)
                    if len(L1_exclude_L2) == 0:
                        zone2.cells = Ordlist(self.N, liste=L2_exclude_L1)
                        zone2.bombs -= zone1.bombs
                        if self.nettoyer(zone2):
                            for i in range(len(self.pile_zone)-1, -1, -1):
                                if self.pile_zone[i][0] == num2 or self.pile_zone[i][1] == num2:
                                    self.pile_zone.pop(i)
                    elif len(L2_exclude_L1) == 0:
                        zone1.cells = Ordlist(self.N, liste=L1_exclude_L2)
                        zone1.bombs -= zone2.bombs
                        if self.nettoyer(zone1):
                            for i in range(len(self.pile_zone)-1, -1, -1):
                                if self.pile_zone[i][0] == num1 or self.pile_zone[i][1] == num1:
                                    self.pile_zone.pop(i)

                    # Sinon, il y a certain(s) cas particulier où l'on peut quand même simplifier
                    elif zone1.bombs - len(L1_exclude_L2) == zone2.bombs:
                        for e in L2_exclude_L1:
                            self.pile_coup.append(Play('Del', e[0], e[1]))
                        for e in L1_exclude_L2:
                            self.pile_coup.append(Play('Flag', e[0], e[1]))
                    elif zone2.bombs - len(L2_exclude_L1) == zone1.bombs:
                        for e in L1_exclude_L2:
                            self.pile_coup.append(Play('Del', e[0], e[1]))
                        for e in L2_exclude_L1:
                            self.pile_coup.append(Play('Flag', e[0], e[1]))

    def nettoyer(self, zone):
        if zone.bombs <= 0:
            for e in zone.cells.list:
                self.pile_coup.append(Play("Del", e[0], e[1]))
            self.delZone(zone.number)
            return True
        elif len(zone.cells.list) == zone.bombs:
            for e in zone.cells.list:
                self.pile_coup.append(Play('Flag', e[0], e[1]))
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