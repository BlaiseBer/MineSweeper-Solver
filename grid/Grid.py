class Grid:
    N=0
    n=0
    grid = []

    def __init__(self,n, N, x):
        self.N = N
        self.n = n
        self.grid = [[x for _ in range(N)] for _ in range(N)]

    def getCircle(self, i, j):
        m = self.N - 1
        l = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i + 1, j),
            (i + 1, j + 1)]
        for e in range(len(l) - 1, -1, -1):
            if l[e][0] < 0 or l[e][0] > m or l[e][1] < 0 or l[e][1] > m:
                l.pop(e)
        return l

    def printGrid(self):
        for i in range(self.N):
            l = ""
            for j in range(self.N):
                if self.grid[i][j] == -2:
                    l += "🟦" + " "
                elif self.grid[i][j] == -1:
                    l += "⚑" + " "
                else:
                    l += str(self.grid[i][j]) + " "

            print(l + "\n")
        print("\n")

    def get(self, i,j):
        return self.grid[i][j]

    def update(self, i, j, x):
        self.grid[i][j] = x