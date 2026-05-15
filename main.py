import random as rd
from Game import Game

N = 10
n = 10

game = Game(n, N, "GoodStart")

game.values.grid.printGrid()
game.start()
game.values.grid.printGrid()
game.found.grid.printGrid()
