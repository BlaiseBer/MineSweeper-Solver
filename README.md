By executing Main, you will have a 10 by 10 grid of MineSweeper randomly created with 10 mines. The program will then attempt to solve it. In the Output, you will see each play that the program does. You can modify N and n to change the size of the grid and the number of bombs respectively. This is still a work in progress, the program gets stuck regularly and the code is highly unoptimised.

The principle of the algorithm is to create "zones" that keep the coordinates of multiple boxes and the number of bombs in them. A zone is created each time a new number is unveiled. Then operations between overlapping zones are made to "reduce" zones and be able to choose where to play next.

A queue ("file") is used to keep in memory all moves that were added and play them one after the other (breadth first search).

problems to solve:
- In some cases, the solver miss some plays that it could do and get stuck

to implement :
- Improve the appearance of the window

Future optimizations :
- Instead of using a linked graph that links each zones to overlapping zones, it would be better to use a dictionnary that links boxes to the zones by wich they are contained.
- reducing operations between the intersection of zones (by keeping them ordered, thus making the intersection linear between two orderd list)
