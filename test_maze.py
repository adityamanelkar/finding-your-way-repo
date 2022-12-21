import numpy

n = 1
p = 0.7
rows = 19
cols = 19
grid = numpy.random.binomial(n,p, size=(rows, cols))

grid = grid.tolist()

maze = [["_" for _ in range(rows)]]

print(grid)