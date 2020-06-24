import sys
from timeit import repeat as rep
import numpy as np
import matplotlib.pyplot as plt
from algorithms import *
from algorithms.utilities.maze import get_maze

##########################################################
                                                        ##
# NOTE: change this if any more algorithm is            ##
#       added or wanted to be removed                   ##
#       (must comment the below part which overwrites   ##
#        these 2 variables)                             ##
                                                        ##
algorithms = (                                          ## 
    simple,                                             ##
    simulatedannealing,                                 ##
    steepestascent,                                     ##
    astar                                               ##
)                                                       ##
ticklables = [                                          ##
    'simple',                                           ##
    'steepest\nascent',                                 ##
    'simulated\nannealing',                             ##
    'A* algorithm'                                      ##
]                                                       ##
                                                        ##
##########################################################

# To compare all the algorithms available, use this, otherwise comment this
algorithms = tuple(all_list)
ticklables_long = tuple(i.name for i in algorithms)
ticklables = tuple('\n'.join(i.name.split(' ')) for i in algorithms)

std_reptimes = 1000

def check_running_time(fun, maze, reptimes = 500):
    '''returns the average running time of fun(maze) after trial number 
    of runs (reptimes)'''
    def check_func():
        fun(maze)
    tests = rep(check_func, number = 1, repeat = reptimes)
    return np.mean(tests) * 1000

def check_maze(maze):
    '''checks the running time of all algorithms to solve the maze 'maze'
    yields running time for each algorithm'''
    for module in algorithms:
        yield check_running_time(module.RUN, maze, reptimes = std_reptimes)

def main(mazes):
    '''takes input as a list of filenames as mazes, converts them to 
    maze.maze_t type and checks 
    the time for solving maze for each available algorithm
    returns a list containing the list of average running time 
    for each maze for an algorithm'''
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

def ask():
    for i in range(len(ticklables)):
        if input("include %s? (y/n): " %ticklables_long[i]) == "y":
            yield i

def ask_n_add():
    global algorithms, ticklables
    a = list(ask())
    algorithms = [algorithms[i] for i in a]
    ticklables = [ticklables[i] for i in a]
    print("running selected algorithms on given mazes and computing time...")

if __name__ == '__main__':
    #skipping argparse module because of less number of argumnets
    if len(sys.argv) < 2:
        print('usage: testtime.py [-a] [-r] mazefile', file = sys.stderr)
        sys.exit()
    if "-a" in sys.argv:
        ask_n_add()
    if "-r" in sys.argv:
        std_reptimes = int(sys.argv[sys.argv.index("-r") + 1])
    if "--help" in sys.argv or "-h" in sys.argv:
        print('usage: testtime.py [-a] [-r] mazefile')
        print('use this program to compare times taken by algorithms')
        print('use -a to add algorithms to compare interactively\n\
use -r to give custom repeate time (for small and fast algorithms \
a larger repeat time is preferable)')
        sys.exit(0)
    BarGraph(np.array(main(sys.argv[1:])))
