from Game import Game
from utilities.Ordlist import Ordlist
N = 10
n = 20

game = Game(n, N, "GoodStart")
game.start()


#test

coup = (4,7)

liste = Ordlist(N, [(4, 7), (4, 8), (5, 8), (6, 8)])
print(liste.toString())
print(liste.isInside(coup))
liste.remove(coup)
print(liste.toString())
