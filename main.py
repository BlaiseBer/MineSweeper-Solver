import random as rd
from Game import Game

N = 5
n = 3

game = Game(n, N, "GoodStart")

game.values.grid.printGrid()
game.start()
game.values.grid.printGrid()
game.found.grid.printGrid()
