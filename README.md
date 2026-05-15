By executing Main, you will have a 10 by 10 grid of MineSweeper randomly created with 10 mines. The program will then attempt to solve it. In the Output, you will see each play that the program does. You can modify N and n to change the size of the grid and the number of bombs respectively. This is still a work in progress, the program gets stuck regularly and the code is highly unoptimised.

The principle of the algorithm is to create "zones" that keep the coordinates of multiple boxes and the number of bombs in them. A zone is created each time a new number is unveiled. Then operations between overlapping zones are made to "reduce" zones and be able to choose where to play next.

A queue ("file") is used to keep in memory all moves that were added and play them one after the other (breadth first search).

problems to solve:

Some move added by the algorithm are wrong (place a flag where there isn't a bomb or remove a boxe where there is a bomb (the last one is rarer)) -> bugs in the code probably
the queue gets sometimes cleared before all the boxes are cleared -> problem in the algorithm ?
to implement :

better visulization (with a dedicated pop-up)
buttons
Future optimizations :

Instead of using a linked graph that links each zones to overlapping zones, it would be better to use a dictionnary that links boxes to the zones by wich they are contained.
reducing operations between the intersection of zones (by keeping them ordered, thus making the intersection linear between two orderd list)
