import sys
import numpy as np
import matplotlib.pyplot as plt
from timeit import repeat as rep
from maze import get_maze

##########################################################
                                                        ##
# NOTE: change this if any more algorithm is added      ##
                                                        ##
# importing the implemented algorithms as modules       ##
# (making sure that each of them has RUN defined)       ##
import simple, simulatedannealing, steepestascent       ##
                                                        ##
algorithms = (                                          ## 
    simple,                                             ##
    simulatedannealing,                                 ##
    steepestascent                                      ##
)                                                       ##
ticklables = [                                          ##
    'simple',                                           ##
    'steepest ascent',                                  ##
    'simulated annealing'                               ##
]                                                       ##
                                                        ##
##########################################################

def check_running_time(fun, maze, reptimes = 1000):
    def check_func():
        fun(maze)
    tests = rep(check_func, number = 1, repeat = reptimes)
    return np.mean(tests) * 1000

def check_maze(maze):
    global algorithms
    for module in algorithms:
        yield check_running_time(module.RUN, maze)

def main(mazes):
    times = []
    mazes = [get_maze(filename) for filename in mazes]
    while None in mazes:
        mazes.remove(None)
    for maze in mazes:
        times.append(list(check_maze(maze)))
    return times

def Colors():
    while True:
        yield 'r'
        yield 'g'
        yield 'b'

def BarGraph(data):
    global ticklables
    fig = plt.figure()
    subfig = fig.add_subplot(111)
    colors = Colors()
    indices = np.arange(0, len(ticklables))
    rects = []
    width = 0.90 / len(data)
    c = - (len(data) / 2)
    for i in data:
        rects.append(subfig.bar(indices + width * c, i, width, color = next(colors)))
        c += 1
    subfig.set_ylabel("running time (miliseconds)")
    subfig.set_xlabel("algorithms")
    subfig.set_xticks(indices - width / 2)
    subfig.set_xticklabels(tuple(ticklables))
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    BarGraph(np.array(main(sys.argv[1:])))

