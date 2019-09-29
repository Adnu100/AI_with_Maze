import sys
import numpy as np
import matplotlib.pyplot as plt
from timeit import repeat as rep
from maze import get_maze

# importing the implemented algorithms as modules (making sure that each of them has RUN defined)
import simple, simulatedannealing, steepestascent

def check_running_time(fun, maze, reptimes = 5000):
    def check_func():
        fun(maze)
    tests = rep(check_func, number = 1, repeat = reptimes)
    return np.mean(tests) * 1000

def check_maze(maze):
    for module in (simple, steepestascent, simulatedannealing):
        yield check_running_time(module.RUN, maze)

def main(mazes):
    times = []
    mazes = [get_maze(filename) for filename in mazes]
    for maze in mazes:
        times.append(list(check_maze(maze)))
    return times

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    times = np.array(main(sys.argv[1:]))
    indices = np.arange(0, 6, 2)
    width = 0.27
    fig = plt.figure()
    subfig = fig.add_subplot(111)
    c = -2
    ticklables = ['simple\nhill\nclimbing', 'steepest\nascent\nhill climbing', 'simulated\nannealing']
    colors = ['r', 'g', 'b', 'r', 'g', 'b']
    rects = []
    for i in times:
        rects.append(subfig.bar(indices + width * c, i, width, color = colors[c + 2]))
        c += 1
    subfig.set_ylabel("running time (miliseconds)")
    subfig.set_xticks(indices + width)
    subfig.set_xticklabels(tuple(ticklables))
    plt.show()

