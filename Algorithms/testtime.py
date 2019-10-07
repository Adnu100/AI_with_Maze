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
                                                        ##
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
    '''returns the average running time of fun(maze) after trial number of runs (reptimes)'''
    def check_func():
        fun(maze)
    tests = rep(check_func, number = 1, repeat = reptimes)
    return np.mean(tests) * 1000

def check_maze(maze):
    '''checks the running time of all algorithms to solve the maze 'maze'
    yields running time for each algorithm'''
    global algorithms
    for module in algorithms:
        yield check_running_time(module.RUN, maze)

def main(mazes):
    '''takes input as a list of filenames as mazes, converts them to maze.maze_t type and checks 
    the time for solving maze for each available algorithm
    returns a list containing the list of average running time for each maze for an algorithm'''
    times = []
    mazes = [get_maze(filename) for filename in mazes]
    while None in mazes:
        mazes.remove(None)
    for maze in mazes:
        times.append(list(check_maze(maze)))
    return times

def Colors():
    '''infinite alternating RGB colors for bars'''
    while True:
        yield 'r'
        yield 'g'
        yield 'b'

def BarGraph(data):
    '''plots a bar graph obtained by the given data'''
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

